import logging
import sys
from pathlib import Path

import setuptools_scm
from fastapi import FastAPI

# Exposed variables for easy short imports directly from fairyjoke package

FAIRYJOKE_PATH = Path(__file__).parent.relative_to(Path.cwd())
APP_NAME = "FairyJoke"
VAR_PATH = Path("var")

__version__ = setuptools_scm.get_version(
    root=Path.cwd(),
    local_scheme=lambda x: f"+branch={x.branch},commit={x.node}",
)

log = logging.getLogger(__name__)
# set console handler format to [LEVEL] module: message
console = logging.StreamHandler()
console.setFormatter(
    logging.Formatter("[%(levelname)s] %(filename)s: %(message)s")
)
log.addHandler(console)
log.setLevel(logging.DEBUG)


sys.path.append(str(FAIRYJOKE_PATH.parent))

VAR_PATH.mkdir(exist_ok=True)

app = FastAPI(redirect_slashes=True)


def create_app():
    from . import plugin

    log.info(f"Starting {APP_NAME} v{__version__}")
    plugins = plugin.load_plugins()
    for p in plugins:
        print(p, p.router.routes)
        app.include_router(p.router, prefix=f"/{p.id}")
    return app
