from logging import getLogger
from pathlib import Path

import yaml
from pydantic import BaseModel, Field


logger = getLogger(__name__)


class InterfaceConfigModel(BaseModel):
    redPin: int = 12
    greenPin: int = 13
    bluePin: int = 18
    tiltPin: int = 17
    heartbeatPin: int = 22
    spiInterface: str = Field(default="")


class ConfigModel(BaseModel):
    interfaces: InterfaceConfigModel = InterfaceConfigModel()


def saveConfig(config: ConfigModel) -> None:
    with CONFIGPATH.open("w") as configFile:
        yaml.safe_dump(config.model_dump(), configFile)
    logger.info("Configuration saved")


CONFIGPATH = Path("config.yaml")

if not CONFIGPATH.exists():
    logger.info(f"Configuration file {CONFIGPATH} does not exist. Creating with default values.")
    CONFIGPATH.touch()
if CONFIGPATH.is_dir():
    raise IsADirectoryError(f"{CONFIGPATH} is a directory, expected a file.")

with CONFIGPATH.open("r") as configFile:
    try:
        configData = yaml.safe_load(configFile) or {}
    except yaml.YAMLError as e:
        logger.error(f"Error loading configuration file: {e}")
        logger.info("Using default configuration values.")
        configData = {}

CONFIG = ConfigModel(**configData)
logger.info("Configuration loaded")
