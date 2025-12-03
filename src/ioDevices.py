from logging import getLogger

import gpiozero
import spidev

from src.config import CONFIG


logger = getLogger(__name__)

tiltSens = gpiozero.InputDevice(CONFIG.interfaces.tiltPin, pull_up=False)
redLed = gpiozero.PWMLED(CONFIG.interfaces.redPin, initial_value=0)
greenLed = gpiozero.LED(CONFIG.interfaces.greenPin, initial_value=True)
blueLed = gpiozero.LED(CONFIG.interfaces.bluePin, initial_value=True)
heartbeatLed = gpiozero.LED(CONFIG.interfaces.heartbeatPin, initial_value=False)
spi = spidev.SpiDev()


def openSPI() -> spidev.SpiDev:
    path = "/dev/" + CONFIG.interfaces.spiInterface
    logger.info(f"Opening SPI interface on {path}")
    spi.open_path(path)
    spi.max_speed_hz = 5000
    spi.mode = 0b00
    return spi
