from logging import getLogger

import gpiozero
from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Label, Input, Switch
from textual.containers import Vertical, Horizontal
from textual.validation import Validator, ValidationResult
from textual.worker import Worker, WorkerState

from src.config import CONFIG


logger = getLogger(__name__)


class LEDPWMValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        try:
            pwm = int(value)
        except ValueError:
            return self.failure("Value must be an integer.")
        if not (0 <= pwm <= 100):
            return self.failure("PWM must be between 0 and 100.")
        else:
            return self.success()


class LedScreen(Screen):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("Start", classes="tab")
            yield Label("Tilt Switch", classes="tab")
            yield Label("Heartbeat", classes="tab")
            yield Label("RGB LED", classes="tab", id="selected")
            yield Label("Tilt & LED", classes="tab")
            yield Label("Heartbeat & LED", classes="tab")
            yield Label("Logging", classes="tab")
        with Horizontal():
            with Vertical():
                with Horizontal(classes="ledRow"):
                    yield Label("Channels:", classes="ledLabel")
                with Horizontal(classes="ledRow"):
                    yield Label("Red:", classes="ledLabel")
                    yield Switch(classes="ledSwitch", id="redSwitch")
                with Horizontal(classes="ledRow"):
                    yield Label("Green:", classes="ledLabel")
                    yield Switch(classes="ledSwitch", id="greenSwitch")
                with Horizontal(classes="ledRow"):
                    yield Label("Blue:", classes="ledLabel")
                    yield Switch(classes="ledSwitch", id="blueSwitch")
        yield Footer()


    def on_mount(self) -> None:
        self.led = gpiozero.RGBLED(
            red=CONFIG.interfaces.redPin,
            green=CONFIG.interfaces.greenPin,
            blue=CONFIG.interfaces.bluePin,
            initial_value=(False, False, False),
            pwm=False
        )


    def on_switch_changed(self, event: Switch.Changed) -> None:
        if self.led is None:
            logger.error("LED not initialized.")
            return
        if event.switch.id in ("redSwitch", "greenSwitch", "blueSwitch"):
            logger.info(f"{event.switch.id} turned {'ON' if event.value else 'OFF'}")
            if event.switch.id == "redSwitch":
                i = 0
            elif event.switch.id == "greenSwitch":
                i = 1
            else:
                i = 2
            values = list(self.led.value)
            values[i] = event.value
            self.led.value = tuple(values)
        else:
            logger.debug(f"Unknown switch changed: {event.switch.id}")


    def on_screen_resume(self) -> None:
        self.on_mount()


    def on_screen_suspend(self) -> None:
        self.led = None