# Local setup

## Prerequisites
Python, pip and a virtual environment are sufficient to inspect the Flask dashboard locally. Docker and Google Cloud CLI are separate prerequisites for container/cloud experiments; neither is required to view the showcase.

## Install
From the repository root:
```sh
python -m venv .venv
```
Activate the environment (`source .venv/bin/activate` on Unix; `.venv\Scripts\Activate.ps1` on PowerShell), then:
```sh
python -m pip install -r requirements.txt
python create_db.py
python run.py
```
Open http://127.0.0.1:5000. Register a disposable local account and inspect the dashboard. `create_db.py` creates tables but is not a schema migration system.

## Configuration
The existing configuration contains a fixed development session key and a local SQLite URI. Treat that key as public. Replace it with an environment-provided secret before any shared deployment. The application does not currently load a `.env` file; do not assume copying an example file configures it.

## Container experiment
Read `docker/Dockerfile` and `docker/startup.sh` first. The Docker build context must be `docker/` so that `COPY startup.sh` resolves. The startup script expects `GITHUB_REPO` as `owner/repository`, whereas the dashboard accepts a URL; normalizing these formats is a remaining integration task.

The current startup disables code-server authentication. **Do not expose this container publicly or use it for sensitive code.** If experimenting locally, bind any published port to 127.0.0.1 and use a disposable workspace.

## Cloud integration
Do not click deployment controls until the cloud path has been reviewed and configured. Source contains project/image placeholders, CLI dependencies and an older helper with a machine-specific service-account path. The guide does not create a key, deploy a service or authorize paid cloud usage.

## Verification and limitations
Verify registration, login and dashboard rendering locally. `GET /healthz` provides a lightweight liveness response without accessing a database or invoking a cloud command. Run `python -m unittest discover -s tests` to check that boundary. Liveness does not mean the database or cloud integration is ready.

Cloud deployment is not covered by these checks. Before hosting the app, address deployment-route authentication, ownership checks, CSRF, shell command construction, private editor access and durable storage.
