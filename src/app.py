from logging import getLogger

from textual import on
from textual.app import App, ComposeResult, ScreenError
from textual.reactive import reactive
from textual.widgets import Footer, Header, Label
from textual.events import Click

from src.textualLogging import RichLogHandler
from src.screens import *


logger = getLogger(__name__)
rootLogger = getLogger()


class GPIOApp(App):
    CSS_PATH = "dom.tcss"
    BINDINGS = [
        ("a", "switchTabLeft", "Previous Tab"),
        ("d", "switchTabRight", "Next Tab"),
    ]
    SCREENS = {
        "start": StartScreen,
        "tiltswitch": TiltScreen,
        "heartbeat": HeartbeatScreen,
        "rgbled": LedScreen,
        "tiltled": TiltLedScreen,
        "heartbeatled": HeartbeatLedScreen,
        "logging": LogScreen,
    }
    ENABLE_LOGGING = False

    tab = reactive(0, bindings=True)


    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()


    def on_mount(self) -> None:
        self.push_screen(tuple(self.SCREENS.keys())[0])
        self.richLogHandler = RichLogHandler(app=self)
        self.richLogHandler.setFormatter(rootLogger.handlers[0].formatter)
        rootLogger.addHandler(self.richLogHandler)


    def action_switchTabLeft(self) -> None:
        self.tab -= 1
        self.switch_screen(tuple(self.SCREENS.keys())[self.tab])


    def action_switchTabRight(self) -> None:
        self.tab += 1
        self.switch_screen(tuple(self.SCREENS.keys())[self.tab])


    @on(Click, ".tab")
    def switchTabs(self, event: Click) -> None:
        if event.widget and event.widget.has_class("tab"):
            tabLabels = list(self.SCREENS.keys())
            if not isinstance(event.widget, Label):
                return
            if not isinstance(event.widget.content, str):
                return
            tabText = event.widget.content.lower().replace(" ", "").replace("&", "")
            if tabText in tabLabels:
                self.tab = tabLabels.index(tabText)
                self.switch_screen(tabText)
            else:
                logger.debug(f"Unknown tab clicked: {tabText}")


    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        if action == "switchTabRight" and self.tab == len(self.SCREENS.keys()) - 1:
            return None
        if action == "switchTabLeft" and self.tab == 0:
            return None
        return True
