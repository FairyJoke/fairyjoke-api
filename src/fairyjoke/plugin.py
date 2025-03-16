import dataclasses
import importlib
import inspect
from dataclasses import dataclass
from pathlib import Path

from fastapi import APIRouter
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker

from fairyjoke import FAIRYJOKE_PATH, VAR_PATH, app, log
from fairyjoke.data import Data


@dataclass
class Plugin:

    path: Path
    id: str = None
    router: APIRouter = dataclasses.field(default_factory=APIRouter)

    def __str__(self):
        return f"<{self.__class__.__name__} {self.id}>"

    def __post_init__(self):
        if not self.id:
            self.id = self.path.name
        if not getattr(app, "plugins", None):
            app.plugins = {}
        if self.id in app.plugins:
            raise ValueError(f"Plugin with id {self.id} already exists")
        self.data = Data(self.path / "data")
        app.plugins[self.id] = self
        self.tables = {}

    def load(self, module):
        for subpath in (f"{module}.py", module):
            if (self.path / subpath).exists():
                module_str = ".".join(self.path.parts) + f".{module}"
                return importlib.import_module(module_str)

    def init(self):
        module = self.load("init")
        if module:
            log.info(f"Running init for {self}")
            module.main()
        else:
            log.debug(f"No init for {self}")

    @classmethod
    def from_path(cls, path: Path) -> "Plugin":
        result = cls(path=path)
        return result

    @classmethod
    def Router(cls) -> APIRouter:
        return cls.get_caller_plugin().router

    @classmethod
    def Data(cls) -> Data:
        return cls.get_caller_plugin().data

    @classmethod
    def Table(cls):
        plugin = cls.get_caller_plugin()
        db_path = VAR_PATH / plugin.id / "db.sqlite"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        engine = create_engine(f"sqlite:///{db_path}")

        class Base(DeclarativeBase):
            __allow_unmapped__ = True

            @declared_attr.directive
            def __tablename__(cls):
                return cls.__name__.lower()

            def __init_subclass__(cls, **kwargs):
                super().__init_subclass__(**kwargs)
                cls.metadata.create_all(engine)
                plugin.tables[cls.__name__] = cls

            @classmethod
            def Session(cls):
                return sessionmaker(bind=engine)()

        return Base

    @classmethod
    def get_caller_plugin(cls):
        # check for plugins/<plugin_id> in stack and return the corresponding
        # Plugin instance
        for frame in inspect.stack():
            parts = frame.filename.split("/")
            if "plugins" in parts:
                plugin_path = Path(
                    "/".join(parts[: parts.index("plugins") + 2])
                )
                plugin_id = plugin_path.name
                return app.plugins.get(plugin_id)
        raise ValueError("No plugin found in stack")


def load_plugins() -> list[Plugin]:
    result = []
    for plugin_base_dir in ((FAIRYJOKE_PATH / "plugins"), Path("plugins")):
        for plugin_path in plugin_base_dir.glob("*/"):
            plugin = Plugin.from_path(plugin_path)
            result.append(plugin)
    for plugin in result:
        plugin.load("routes")
        plugin.load("db")
    return result
