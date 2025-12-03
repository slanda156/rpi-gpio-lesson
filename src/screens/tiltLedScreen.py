from time import sleep
from logging import getLogger

from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Label
from textual.containers import Horizontal
from textual.worker import Worker, WorkerState

from src.config import CONFIG
from src.ioDevices import tiltSens, redLed, greenLed


logger = getLogger(__name__)


class TiltLedScreen(Screen):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("Start", classes="tab")
            yield Label("Tilt Switch", classes="tab")
            yield Label("Heartbeat", classes="tab")
            yield Label("RGB LED", classes="tab")
            yield Label("Tilt & LED", classes="tab", id="selected")
            yield Label("Heartbeat & LED", classes="tab")
            yield Label("Logging", classes="tab")
        yield Footer()


    def on_mount(self) -> None:
        self.tiltSens = tiltSens
        self.lastValue = not self.tiltSens.value
        self.redLed = redLed
        self.greenLed = greenLed
        self.updateGPIO()
        self.redLed.on()
        self.greenLed.off()


    @work(thread=True)
    def updateGPIO(self) -> None:
        state = self.tiltSens.value
        if state != self.lastValue:
            self.lastValue = state
            logger.info(f"Tilt Switch State changed to: {'ON' if state else 'OFF'}")
            if state:
                self.redLed.off()
                self.greenLed.on()
            else:
                self.redLed.on()
                self.greenLed.off()
        sleep(0.1)


    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.worker.state not in {WorkerState.RUNNING, WorkerState.SUCCESS}:
            logger.debug(f"Worker state changed: {event.worker.name} is now {event.worker.state.name}")
        if event.worker.name == "updateGPIO":
            if event.worker.state in {WorkerState.ERROR, WorkerState.SUCCESS}:
                self.updateGPIO()


    def on_screen_resume(self) -> None:
        self.updateGPIO()
        self.redLed.on()
        self.greenLed.off()


    def on_screen_suspend(self) -> None:
        for worker in self.workers:
            worker.cancel()