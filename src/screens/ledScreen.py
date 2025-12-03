from logging import getLogger

from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Label, Switch
from textual.containers import Vertical, Horizontal

from src.config import CONFIG
from src.ioDevices import redLed, greenLed, blueLed


logger = getLogger(__name__)


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
        self.redLed = redLed
        self.greenLed = greenLed
        self.blueLed = blueLed


    def on_switch_changed(self, event: Switch.Changed) -> None:
        if event.switch.id == "redSwitch":
            self.redLed.value = event.value
            logger.info(f"Red LED turned {'ON' if event.value else 'OFF'}")
        elif event.switch.id == "greenSwitch":
            self.greenLed.value = event.value
            logger.info(f"Green LED turned {'ON' if event.value else 'OFF'}")
        elif event.switch.id == "blueSwitch":
            self.blueLed.value = event.value
            logger.info(f"Blue LED turned {'ON' if event.value else 'OFF'}")
        else:
            logger.debug(f"Unknown switch changed: {event.switch.id}")


    def on_screen_resume(self) -> None:
        self.redLed.off()
        self.greenLed.off()
        self.blueLed.off()
