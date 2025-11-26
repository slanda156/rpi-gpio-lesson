from collections import deque
import logging

from textual.app import App
from textual.widgets import RichLog
from textual.css.query import NoMatches
from textual._context import NoActiveAppError


class RichLogHandler(logging.Handler):
    def __init__(self, app: App, level=logging.NOTSET) -> None:
        super().__init__(level)
        self.app = app
        self.buffer = deque(maxlen=1000)
        self.richLog = None


    @property
    def richLog(self) -> RichLog | None:
        return self._richlog

    @richLog.setter
    def richLog(self, value: RichLog | None) -> None:
        self._richlog = value


    def emit(self, record: logging.LogRecord) -> None:
        logLevel = record.levelno
        match logLevel:
            case logging.DEBUG:
                logColor = "green"

            case logging.INFO:
                logColor = "gray"

            case logging.WARNING:
                logColor = "yellow"

            case logging.ERROR:
                logColor = "red"

            case logging.CRITICAL:
                logColor = "orange_red"

            case _:
                logColor = ""

        msg = self.format(record)
        msg = f"[{logColor}]{msg}[/{logColor}]"
        if self.richLog:
            try:
                self.richLog.write(msg)
            except NoActiveAppError:
                self.buffer.append(msg)
        else:
            if self.buffer:
                self.loadBuffer()
            self.buffer.append(msg)

    def loadBuffer(self) -> None:
        if not self.richLog:
            return
        while self.buffer:
            msg = self.buffer.popleft()
            self.richLog.write(msg)
