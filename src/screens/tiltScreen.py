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
            yield Switch(disabled=True, id="tiltSwitchState")
        yield Footer()


    def on_mount(self) -> None:
        self.tiltSens = gpiozero.InputDevice(CONFIG.interfaces.tiltPin, pull_up=True)
        self.tiltSens.when_activated = self.switchOff
        self.tiltSens.when_deactivated = self.switchOn


    def changeSwitchState(self, state: bool) -> None:
        logger.info(f"Tilt Switch State changed to: {'ON' if state else 'OFF'}")
        self.query_one("#tiltSwitchState", Switch).disabled = False
        self.query_one("#tiltSwitchState", Switch).value = state
        self.query_one("#tiltSwitchState", Switch).disabled = True


    def switchOn(self) -> None:
        self.changeSwitchState(True)


    def switchOff(self) -> None:
        self.changeSwitchState(False)
