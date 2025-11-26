# ESY

A small Python project providing a textual UI with multiple screens (heartbeat, tilt, LED and logging) and simple configuration and logging support.

**Project Overview**

This project contains a small application whose entry point is `main.py`. The app uses code under the `src/` package and provides several screens in `src/screens/` including heartbeat and tilt displays, LED controls, and a log viewer. Configuration is stored in `config.yaml`, and logging is configured with `logger.yaml`.

**Requirements**

- **Python**: 3.8+
- **Dependencies**: see `requirements.txt`.

**Installation**

- Create and activate a virtual environment (recommended):

```bat
python -m venv .venv
.venv\Scripts\activate
```

- Install dependencies:

```bat
pip install -r requirements.txt
```

On Unix/macOS use:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Configuration**

- `config.yaml`: main app configuration values. Edit this file to change runtime settings.
- `logger.yaml`: logging configuration used by the app; adjust handlers/levels as needed.

**Running the App**

From the project root run:

```bat
python main.py
```

Or on Unix/macOS:

```bash
python main.py
```

The app will read `config.yaml` and `logger.yaml` by default and write runtime logs to the `logs/` folder.

**Project Structure**

- `main.py`: application entry point.
- `config.yaml`: application configuration.
- `logger.yaml`: logging configuration.
- `requirements.txt` / `requirements.in`: Python dependencies.
- `src/`:
  - `app.py`: core application logic and initialization.
  - `config.py`: configuration helpers.
  - `textualLogging.py`: logging helpers/integration.
  - `dom.tcss`: styling or UI assets used by the textual UI.
  - `screens/`: screen modules for the UI (heartbeat, tilt, LED, logs, start screen).

**Logging**

Logs are located in the `logs/` folder. `logger.yaml` configures how logs are formatted and rotated. Check that file to change log levels, formatters, or handlers.

**Development**

- Run the app locally using the commands above.
- Modify code under `src/` and reload the app to test changes.
- Consider using an editor with proper Python support (type checking, formatting).

**Contributing**

If you want to contribute, please create a branch, add tests for new behavior, and open a PR with a clear description of your changes.

**License**

This repository does not currently include an explicit license. Add a `LICENSE` file if you want to make licensing clear.

**Contact / Notes**

If you need help running or extending the project, provide details and I'll help with setup, debugging, or adding features.
