from time import sleep
from logging import getLogger

import gpiozero
from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Label
from textual.containers import Horizontal
from textual.worker import Worker, WorkerState

from src.config import CONFIG


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
        self.tiltSens = gpiozero.InputDevice(CONFIG.interfaces.tiltPin, pull_up=False)
        self.lastValue = not self.tiltSens.value
        self.led = gpiozero.RGBLED(
            red=CONFIG.interfaces.redPin,
            green=CONFIG.interfaces.greenPin,
            blue=CONFIG.interfaces.bluePin,
            initial_value=(False, False, False),
            pwm=False
        )
        self.updateGPIO()


    @work(thread=True)
    def updateGPIO(self) -> None:
        if self.led is None:
            logger.error("LED not initialized.")
            return
        state = self.tiltSens.value
        if state != self.lastValue:
            self.lastValue = state
            logger.info(f"Tilt Switch State changed to: {'ON' if state else 'OFF'}")
            if state:
                self.led.color = (True, False, False)
            else:
                self.led.color = (False, True, False)
        sleep(0.1)


    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.worker.state not in {WorkerState.RUNNING, WorkerState.SUCCESS}:
            logger.debug(f"Worker state changed: {event.worker.name} is now {event.worker.state.name}")
        if event.worker.name == "updateGPIO":
            if event.worker.state in {WorkerState.ERROR, WorkerState.SUCCESS}:
                self.updateGPIO()


    def on_screen_resume(self) -> None:
        self.on_mount()


    def on_screen_suspend(self) -> None:
        for worker in self.workers:
            worker.cancel()
        if self.led is not None:
            self.led.close()
            self.led = None
        if self.tiltSens is not None:
            self.tiltSens.close()
            self.tiltSens = None
