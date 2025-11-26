from time import sleep
from logging import getLogger
from random import randint

from colorama import init # ToDo Temporary import for testing

import spidev
import gpiozero
from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Label, Sparkline, Switch
from textual.containers import Horizontal
from textual.worker import Worker, WorkerState

from src.config import CONFIG


logger = getLogger(__name__)


class HeartbeatScreen(Screen):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("Start", classes="tab")
            yield Label("Tilt Switch", classes="tab")
            yield Label("Heartbeat", classes="tab", id="selected")
            yield Label("RGB LED", classes="tab")
            yield Label("Tilt & LED", classes="tab")
            yield Label("Heartbeat & LED", classes="tab")
            yield Label("Logging", classes="tab")
        with Horizontal(id="heartRow"):
            yield Label("Heartbeat Sensor")
            yield Switch(id="heartbeatSwitch")
        yield Sparkline(id="heartbeatSparkline")
        yield Footer()


    def on_mount(self) -> None:
        self.spi = spidev.SpiDev()
        self.spi.open_path(CONFIG.interfaces.spiInterface)
        self.spi.max_speed_hz = 5000
        self.spi.mode = 0b00
        self.heartLED = gpiozero.LED(CONFIG.interfaces.heartbeatPin, initial_value=False)


    def updateHeartbeat(self, value: int) -> None:
        logger.debug(f"New Heartbeat value: {value}")
        spark = self.query_one("#heartbeatSparkline", Sparkline)
        if spark.data is None:
            spark.data = [0] *100
        data = list(spark.data)
        data.append(value)
        while len(data) > 100:
            data.pop(0)
        spark.data = data


    @work(thread=True)
    def updateGPIO(self) -> None:
        heartbeatLEDState = self.query_one("#heartbeatSwitch", Switch).value
        self.heartLED.value = heartbeatLEDState
        if heartbeatLEDState:
            cmd = [0b00000001, 0b10000000, 0b00000000]
            rawValue = self.spi.xfer2(cmd)
            if len(rawValue) != 3:
                logger.error("Invalid SPI response length for Heartbeat Sensor")
                sleep(0.1)
                return
            bitValue = ((rawValue[1] & 3) << 8) | rawValue[2]
            value = int((bitValue / 1023) * 100)
            self.updateHeartbeat(value)
        else:
            self.updateHeartbeat(0)
        sleep(0.1)


    def on_switch_changed(self, event: Switch.Changed) -> None:
        if event.switch.id == "heartbeatSwitch":
            logger.info(f"Heartbeat Sensor Enabled: {event.value}")
            self.updateGPIO()


    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.worker.state not in {WorkerState.RUNNING, WorkerState.SUCCESS}:
            logger.debug(f"Worker state changed: {event.worker.name} is now {event.worker.state.name}")
        if event.worker.name == "updateGPIO":
            if event.worker.state in {WorkerState.ERROR, WorkerState.SUCCESS}:
                self.updateGPIO()


    def on_screen_resume(self) -> None:
        self.updateGPIO()


    def on_screen_suspend(self) -> None:
        for worker in self.workers:
            worker.cancel()
