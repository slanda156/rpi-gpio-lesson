# Empty Project Template
# Author: 		Christoph Heil (https://github.com/slanda156)
# Repository:	https://github.com/slanda156/python-templates
# License:		MIT License (https://github.com/slanda156/python-templates/blob/main/LICENSE)

# Import built-in modules
import datetime
import yaml
import logging
import logging.handlers
import logging.config
import traceback
from pathlib import Path
# Import third-party modules
from coloredlogs import install
import platform
import cpuinfo
import GPUtil

# Configer Logging
rootPath = Path(__file__).parent.parent
loggingConfigPath = rootPath / "logger.yaml"
with open(loggingConfigPath) as f:
    # Load config
    loggerConfig = yaml.safe_load(f.read())
# Check folder path
logPath = Path.cwd() / Path(loggerConfig["handlers"].get("rotating")["filename"])
logPathExists = logPath.exists()
logPath.parent.mkdir(parents=True, exist_ok=True)
# Configer logging
logging.config.dictConfig(loggerConfig)
# Get config for color logging
logFormat = loggerConfig.get("formatters", {}).get("simple", {}).get("format", None)
logDatefmt = loggerConfig.get("formatters", {}).get("simple", {}).get("datefmt", None)
logLevel = loggerConfig.get("root", {}).get("level", 0)
# Make logging colerfull in the terminal
install(level=logLevel, fmt=logFormat, datefmt=logDatefmt)

# Get logger
rootLogger = logging.getLogger()
# Do rollover only if a log file exists
if logPathExists:
    for handler in rootLogger.handlers:
        if isinstance(handler, logging.handlers.RotatingFileHandler):
            handler.doRollover()


def createCrashLog(e: Exception) ->  None:
    """
    Function to create a crash log.
    """
    crashLogPath = Path("logs/crash_logs/")
    crashLogPath.mkdir(parents=True, exist_ok=True)
    crashLogDateTime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    crashLogPath = crashLogPath / f"crash_{crashLogDateTime}.log"
    crashLog = ""
    crashLog += f"Crash log created at {crashLogDateTime}\n"
    cpuinfo_data = cpuinfo.get_cpu_info()
    crashLog += f"CPU: {cpuinfo_data['brand_raw']}\n"
    crashLog += f"Architecture: {str(platform.architecture()).replace('(', '').replace(')', '').replace('\'', '')}\n"
    crashLog += f"OS: {platform.system()} {platform.release()}\n"
    crashLog += f"OS build: {platform.version()}\n"
    crashLog += f"Python version: {platform.python_version()}\n"
    crashLog += f"Python implementation: {platform.python_implementation()}\n"
    gpus: list[GPUtil.GPU] = GPUtil.getGPUs()
    for gpu in gpus:
        crashLog += f"GPU: {gpu.name}\n"
        crashLog += f"GPU Driver: {gpu.driver}\n"
        crashLog += f"GPU Memory Total: {gpu.memoryTotal} MB\n"
        crashLog += f"GPU Memory Free: {gpu.memoryFree} MB\n"
        crashLog += f"GPU Memory Used: {gpu.memoryUsed} MB\n"
        crashLog += f"GPU Temperature: {gpu.temperature} °C\n"
        crashLog += f"GPU Load: {gpu.load * 100:.1f}%\n"
    longestLine = max(len(line) for line in crashLog.splitlines())
    crashLog += longestLine * "-" + "\n"
    crashLog += "Exception:\n"
    crashLog += f"\tType: {type(e).__name__}\n"
    crashLog += f"\tMessage: {str(e)}\n"
    crashLog += f"\n{traceback.format_exc()}"
    rootLogger.info(f"Creating crash log at {crashLogPath}")
    with open(crashLogPath, "w", encoding="utf-8") as f:
        f.write(crashLog)
