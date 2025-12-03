from time import sleep
from logging import getLogger

import gpiozero
from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Label, Switch
from textual.containers import Horizontal
from textual.worker import Worker, WorkerState

from src.config import CONFIG


logger = getLogger(__name__)


class TiltScreen(Screen):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("Start", classes="tab")
            yield Label("Tilt Switch", classes="tab", id="selected")
            yield Label("Heartbeat", classes="tab")
            yield Label("RGB LED", classes="tab")
            yield Label("Tilt & LED", classes="tab")
            yield Label("Heartbeat & LED", classes="tab")
            yield Label("Logging", classes="tab")
        with Horizontal():
            yield Label("Tilt Switch State:")
            yield Switch(disabled=True, id="tiltSwitchState", animate=False)
        yield Footer()


    def on_mount(self) -> None:
        self.tiltSens = gpiozero.InputDevice(CONFIG.interfaces.tiltPin, pull_up=False)
        self.lastValue = not self.tiltSens.value
        self.updateGPIO()


    def changeSwitchState(self, state: bool) -> None:
        if state != self.lastValue:
            self.lastValue = state
            logger.info(f"Tilt Switch State changed to: {'ON' if state else 'OFF'}")
            self.query_one("#tiltSwitchState", Switch).disabled = False
            self.query_one("#tiltSwitchState", Switch).value = state
            self.query_one("#tiltSwitchState", Switch).disabled = True


    @work(thread=True)
    def updateGPIO(self) -> None:
        if self.tiltSens is None:
            logger.error("Tilt Sensor not initialized.")
            return
        state = self.tiltSens.value
        self.changeSwitchState(state)
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
        if self.tiltSens is not None:
            self.tiltSens.close()
            self.tiltSens = None