import os
import glob
from logging import getLogger

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Label, Input, RadioSet, RadioButton
from textual.containers import Vertical, Horizontal
from textual.validation import Validator, ValidationResult

from src.config import CONFIG


logger = getLogger(__name__)


class LEDPinValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        try:
            pin = int(value)
        except ValueError:
            return self.failure("Value must be an integer.")
        allowedPins = (12, 13, 18, 19)
        if pin not in allowedPins:
            return self.failure(f"Pin must be one of: {', '.join(map(str, allowedPins))}.")
        else:
            return self.success()


class PinValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        try:
            pin = int(value)
        except ValueError:
            return self.failure("Value must be an integer.")
        allowedPins = (4, 5, 6, 12, 13, 16, 17, 22, 23,24, 25, 26, 27)
        if pin not in allowedPins:
            return self.failure(f"Pin must be one of: {', '.join(map(str, allowedPins))}.")
        else:
            return self.success()


class StartScreen(Screen):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("Start", classes="tab", id="selected")
            yield Label("Tilt Switch", classes="tab")
            yield Label("Heartbeat", classes="tab")
            yield Label("RGB LED", classes="tab")
            yield Label("Tilt & LED", classes="tab")
            yield Label("Heartbeat & LED", classes="tab")
            yield Label("Logging", classes="tab")
        with Vertical():
            yield Label("RGB LED Config:")
            with Horizontal():
                yield Label("Red Pin:")
                yield Input(type="integer", classes="startInput", id="redPin", validators=LEDPinValidator(), select_on_focus=True)
            with Horizontal():
                yield Label("Green Pin:")
                yield Input(type="integer", classes="startInput", id="greenPin", validators=LEDPinValidator(), select_on_focus=True)
            with Horizontal():
                yield Label("Blue Pin:")
                yield Input(type="integer", classes="startInput", id="bluePin", validators=LEDPinValidator(), select_on_focus=True)
        with Vertical():
            yield Label("Tilt Switch Config:")
            with Horizontal():
                yield Label("Tilt Switch Pin:")
                yield Input(type="integer", classes="startInput", id="tiltPin", validators=PinValidator(), select_on_focus=True)
        with Vertical():
            yield Label("Heartbeat Config:")
            with Horizontal():
                yield Label("Heartbeat LED Pin:")
                yield Input(type="integer", classes="startInput", id="heartbeatPin", validators=PinValidator(), select_on_focus=True)
            with Horizontal():
                yield Label("SPI Interface:")
                with RadioSet():
                    if os.name == "posix":
                        paths = glob.glob("/dev/spi*")
                        logger.debug(f"Avialbale paths: {paths}")
                        interfaces = [path for path in paths]
                        logger.debug(f"Available SPI interfaces: {interfaces}")
                        if len(interfaces) == 0:
                            raise Exception("No spi interfaces found")
                        for interface in interfaces:
                            interfaceName = interface.replace("/dev/", "")
                            interfaceId = interfaceName.replace(".", "")
                            yield RadioButton(interfaceName, classes="spiList", id=interfaceId)
                    else:
                        raise NotImplementedError("Only POSIX systems are supported.")
        yield Footer()


    def on_mount(self) -> None:
        self.query_one("#redPin", Input).value = str(CONFIG.interfaces.redPin)
        self.query_one("#greenPin", Input).value = str(CONFIG.interfaces.greenPin)
        self.query_one("#bluePin", Input).value = str(CONFIG.interfaces.bluePin)
        self.query_one("#tiltPin", Input).value = str(CONFIG.interfaces.tiltPin)
        self.query_one("#heartbeatPin", Input).value = str(CONFIG.interfaces.heartbeatPin)
        spiInterface = CONFIG.interfaces.spiInterface.lower().replace(".", "")
        if spiInterface == "":
            spiInterface = self.query_one(".spiList", RadioButton).id
            if spiInterface is None:
                raise Exception("No spi interface found")
        self.query_one(f"#{spiInterface}", RadioButton).value = True


    def on_input_blurred(self, event: Input.Changed) -> None:
        if not event.value.isdecimal():
            return
        if event.input.id == "redPin":
            CONFIG.interfaces.redPin = int(event.value)
        elif event.input.id == "greenPin":
            CONFIG.interfaces.greenPin = int(event.value)
        elif event.input.id == "bluePin":
            CONFIG.interfaces.bluePin = int(event.value)
        elif event.input.id == "tiltPin":
            CONFIG.interfaces.tiltPin = int(event.value)
        elif event.input.id == "heartbeatPin":
            CONFIG.interfaces.heartbeatPin = int(event.value)


    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        interface = event.pressed.id
        if not interface:
            logger.warning("No SPI interface selected.")
            return
        interface = interface[:-1] +  "." + interface[-1:]
        CONFIG.interfaces.spiInterface = interface
