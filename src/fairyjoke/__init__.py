import sys
from pathlib import Path

import setuptools_scm
from fastapi import FastAPI
from sqlalchemy_setup import Database

# Exposed variables

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
app = FastAPI()

from .plugin import Plugin


def main():
    def load_plugins(path: str):
        for plugin_path in Path(path).glob("*/"):
            plugin = Plugin.get(plugin_path)
            plugin.init()

    load_plugins(FAIRYJOKE_PATH / "plugins")
    load_plugins("plugins")


main()
