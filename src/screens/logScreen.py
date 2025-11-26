from logging import getLogger

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Label, RichLog
from textual.containers import Horizontal


logger = getLogger(__name__)


class LogScreen(Screen):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("Start", classes="tab")
            yield Label("Tilt Switch", classes="tab")
            yield Label("Heartbeat", classes="tab")
            yield Label("RGB LED", classes="tab")
            yield Label("Tilt & LED", classes="tab")
            yield Label("Heartbeat & LED", classes="tab")
            yield Label("Logging", classes="tab", id="selected")
        yield RichLog(id="log", markup=True)
        yield Footer()


    def on_mount(self) -> None:
        self.app.richLogHandler.richLog = self.query_one(RichLog) # type: ignore

    def on_screen_resume(self) -> None:
        self.app.richLogHandler.loadBuffer() # type: ignore
