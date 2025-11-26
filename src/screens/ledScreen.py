from logging import getLogger

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
            with Vertical():
                with Horizontal(classes="ledRow"):
                    yield Label("PWM:", classes="ledLabel")
                    yield Switch(classes="ledSwitch", id="pwmEnableSwitch")
                with Horizontal(classes="ledRow"):
                    yield Label("Red:", classes="ledLabel")
                    yield Input(type="integer", classes="ledInput", id="redPWM", validators=LEDPWMValidator(), value="0", select_on_focus=True, disabled=True)
                with Horizontal(classes="ledRow"):
                    yield Label("Green:", classes="ledLabel")
                    yield Input(type="integer", classes="ledInput", id="greenPWM", validators=LEDPWMValidator(), value="0", select_on_focus=True, disabled=True)
                with Horizontal(classes="ledRow"):
                    yield Label("Blue:", classes="ledLabel")
                    yield Input(type="integer", classes="ledInput", id="bluePWM", validators=LEDPWMValidator(), value="0", select_on_focus=True, disabled=True)
        yield Footer()


    def on_mount(self) -> None:
        # ToDo: Implement the I/O
        pass


    def on_input_blurred(self, event: Input.Changed) -> None:
        if not self.query_one("#pwmEnableSwitch", Switch).value:
            return
        if not event.value.isdecimal():
            return
        pwmValue = int(event.value)
        if event.input.id == "redPWM":
            logger.info(f"Set Red LED PWM to {pwmValue}%")
            self.updateGPIO(pin=CONFIG.interfaces.redPin, mode="PWM", value=pwmValue)
        elif event.input.id == "greenPWM":
            logger.info(f"Set Green LED PWM to {pwmValue}%")
            self.updateGPIO(pin=CONFIG.interfaces.greenPin, mode="PWM", value=pwmValue)
        elif event.input.id == "bluePWM":
            logger.info(f"Set Blue LED PWM to {pwmValue}%")
            self.updateGPIO(pin=CONFIG.interfaces.bluePin, mode="PWM", value=pwmValue)


    def on_switch_changed(self, event: Switch.Changed) -> None:
        if event.switch.id == "pwmEnableSwitch":
            self.query_one("#redPWM", Input).disabled = not event.value
            self.query_one("#greenPWM", Input).disabled = not event.value
            self.query_one("#bluePWM", Input).disabled = not event.value
        elif event.switch.id == "redSwitch":
            logger.info(f"Red LED turned {'ON' if event.value else 'OFF'}")
        elif event.switch.id == "greenSwitch":
            logger.info(f"Green LED turned {'ON' if event.value else 'OFF'}")
        elif event.switch.id == "blueSwitch":
            logger.info(f"Blue LED turned {'ON' if event.value else 'OFF'}")
        else:
            logger.debug(f"Unknown switch changed: {event.switch.id}")


    @work(thread=True)
    def updateGPIO(self, pin: int, mode: str, value: int) -> None:
        # ToDo: Implement the change to I/O
        pass


    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.worker.state not in {WorkerState.RUNNING, WorkerState.SUCCESS}:
            logger.debug(f"Worker state changed: {event.worker.name} is now {event.worker.state.name}")


    def on_screen_suspend(self) -> None:
        for worker in self.workers:
            worker.cancel()
