from time import sleep
from logging import getLogger

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
        # ToDo: Implement the I/O
        pass


    @work(thread=True)
    def updateGPIO(self) -> None:
        # ToDo: Implement the change to I/O
        sleep(0.1)


    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.worker.state not in {WorkerState.RUNNING, WorkerState.SUCCESS}:
            logger.debug(f"Worker state changed: {event.worker.name} is now {event.worker.state.name}")
        if event.worker.name == "updateGPIO":
            if event.worker.state in {WorkerState.ERROR, WorkerState.SUCCESS}:
                self.updateGPIO()


    def on_screen_resume(self) -> None:
        self.updateGPIO()


    def on_screen_suspend(self) -> None:
        for worker in self.workers:
            worker.cancel()
