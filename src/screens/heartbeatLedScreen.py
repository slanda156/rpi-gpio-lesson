from time import sleep
from logging import getLogger

from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Label
from textual.containers import Horizontal
from textual.worker import Worker, WorkerState

from src.config import CONFIG
from src.ioDevices import heartbeatLed, redLed, spi, openSPI


logger = getLogger(__name__)


class HeartbeatLedScreen(Screen):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("Start", classes="tab")
            yield Label("Tilt Switch", classes="tab")
            yield Label("Heartbeat", classes="tab")
            yield Label("RGB LED", classes="tab")
            yield Label("Tilt & LED", classes="tab")
            yield Label("Heartbeat & LED", classes="tab", id="selected")
            yield Label("Logging", classes="tab")
        yield Footer()


    def on_mount(self) -> None:
        self.led = redLed
        self.spi = openSPI()
        self.heartLED = heartbeatLed
        self.data = [0.0] * 100
        self.diffData = [0.0] * 100
        self.updateGPIO()
        self.led.off()


    @work(thread=True)
    def updateGPIO(self) -> None:
        cmd = [0b00000001, 0b00000000, 0b00000000]
        try:
            rawValue = self.spi.xfer2(cmd)
        except:
            return
        if len(rawValue) != 3:
            logger.error("Invalid SPI response length for Heartbeat Sensor")
            sleep(0.1)
            return
        bitValue = ((rawValue[1] & 3) << 8) | rawValue[2]
        value = int((bitValue / 1023) * 100)
        self.updateHeartbeat(value)
        sleep(0.1)


    def updateHeartbeat(self, value: int) -> None:
        logger.debug(f"New Heartbeat value: {value}")
        self.data.append(value)
        while len(self.data) > 100:
            self.data.pop(0)
        meanValue = sum(self.data) / len(self.data)
        diffValue = abs(value - meanValue)
        self.diffData.append(diffValue)
        while len(self.diffData) > 100:
            self.diffData.pop(0)
        minData = min(self.diffData)
        maxData = max(self.diffData)
        maxDiff = maxData - minData
        newValue = diffValue * (1 / maxDiff) if maxDiff != 0 else 0
        if newValue < CONFIG.heartbeatThreshold:
            self.led.off()
        else:
            self.led.on()


    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.worker.state not in {WorkerState.RUNNING, WorkerState.SUCCESS}:
            logger.debug(f"Worker state changed: {event.worker.name} is now {event.worker.state.name}")
        if event.worker.name == "updateGPIO":
            if event.worker.state in {WorkerState.ERROR, WorkerState.SUCCESS}:
                self.updateGPIO()


    def on_screen_resume(self) -> None:
        self.updateGPIO()
        self.led.off()


    def on_screen_suspend(self) -> None:
        for worker in self.workers:
            worker.cancel()
