import logging
import sys
from pathlib import Path

import setuptools_scm
from fastapi import APIRouter, FastAPI

# Exposed variables for easy short imports directly from fairyjoke package

FAIRYJOKE_PATH = Path(__file__).parent.relative_to(Path.cwd())
DATA_PATH = Path("data")
APP_NAME = "FairyJoke"
VAR_PATH = Path("var")
__version__ = setuptools_scm.get_version(
    root=Path.cwd(),
    local_scheme=lambda x: f"+branch={x.branch},commit={x.node}",
)

sys.path.append(str(FAIRYJOKE_PATH.parent))
VAR_PATH.mkdir(exist_ok=True)
app = FastAPI(redirect_slashes=True)

from .plugin import Plugin


def setup_logging():
    logging.basicConfig(
        format="[{levelname}] {module}: {message}",
        style="{",
        level=logging.DEBUG,
    )


def main():
    setup_logging()
    core_plugins = {}
    external_plugins = {}
    plugins = {}

    def load_plugins(path: str):
        plugins = []
        for plugin_path in Path(path).glob("*/"):
            plugin = Plugin.get(plugin_path)
            plugin.init()
            plugins.append(plugin)
        return plugins

    # Plugins in src directory are sourced first
    for plugin in load_plugins(FAIRYJOKE_PATH / "plugins"):
        core_plugins[plugin.id] = plugin
        plugins[plugin.id] = plugin
    # Then the plugins in the current working directory
    # for plugin in load_plugins("plugins"):
    #     external_plugins[plugin.id] = plugin
    #     plugins[plugin.id] = plugin
    # This ensures that any plugin in the current working directory will have
    # access to features exposed by the core plugins, if ever needed
    api_router = APIRouter(prefix="/api")
    for plugin in plugins.values():
        if plugin.api_router:
            api_router.include_router(plugin.api_router)
    app.include_router(api_router)
    logging.debug("Hello")


main()
