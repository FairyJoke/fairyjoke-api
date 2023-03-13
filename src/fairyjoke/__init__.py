import importlib
import inspect
import sys
from pathlib import Path

import setuptools_scm
from fastapi import FastAPI
from sqlalchemy_setup import Database

# Exposed variables

FAIRYJOKE_PATH = Path(__file__).parent
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

plugins_table = {}


class Plugin:
    def __init__(self, path: Path):
        if path.is_absolute():
            path = path.relative_to(Path.cwd())
        self.path = path
        self.id = module_str = self.idify(path)
        self.module = importlib.import_module(module_str)
        print("Found module", self.module.__name__)
        models_module_str = f"{module_str}.models"
        try:
            importlib.import_module(models_module_str)
            self.db = Database(
                f"sqlite:///{VAR_PATH / module_str}.sqlite", id=module_str
            )
        except ModuleNotFoundError as e:
            if e.name != models_module_str:
                raise e

    @staticmethod
    def idify(path: Path):
        """
        >>> Plugin.idify(Path("plugins/sdvx"))
        'plugins.sdvx'
        """
        return ".".join(path.parts)

    @classmethod
    @property
    def current(cls) -> "Plugin":
        """
        Resolves to the plugin that called this function
        """
        for frame in inspect.stack():
            if frame.filename.startswith("<"):
                continue
            path = Path(frame.filename)
            print(path)
            if not path.is_relative_to(Path.cwd()):
                continue
            path = path.relative_to(Path.cwd())
            id = cls.idify(path)
            for plugin in plugins_table:
                if id.startswith(plugin):
                    return plugins_table[plugin]

    @classmethod
    @property
    def db(cls) -> Database:
        """
        Shortcut for Plugin.current.db
        """
        return cls.current.db


def load_plugins(path: str):
    for plugin in Path(path).glob("*/"):
        plugin = Plugin(plugin)
        plugins_table[plugin.id] = plugin


load_plugins(FAIRYJOKE_PATH / "plugins")
load_plugins("plugins")

for plugin in plugins_table.values():
    if hasattr(plugin, "db"):
        plugin.db.init()
