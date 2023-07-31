import importlib
import inspect
from pathlib import Path

from fastapi import APIRouter

from fairyjoke import VAR_PATH
from fairyjoke.db import Database


class Plugin:
    all = {}

    def __init__(self, path: Path | str):
        self.id = self.idify(path)
        self.name = self.id.split(".")[-1]
        self.module = importlib.import_module(self.id)
        self._db = None
        print("Found plugin module", self)
        self.all[self.id] = self
        self.api_router = None
        self.frontend_router = None

    def __str__(self):
        return self.id

    def init(self):
        def load(module, attribute=None):
            module_str = f"{self.id}.{module}"
            try:
                imported = importlib.import_module(module_str)
                if attribute and hasattr(imported, attribute):
                    return getattr(imported, attribute)
                return imported
            except ModuleNotFoundError as e:
                if e.name != module_str:
                    raise e
                return None

        # We access the "models" submodule to trigger the creation of the
        # tables
        load("models")
        # If "Plugin.db" was accessed at least once, it should mean that tables
        # are defined, we then actually create them in the database
        if self._db:
            self.db.init()

        self.api_router = load("api", "router")
        self.frontend_router = load("frontend", "router")

    @property
    def db(self):
        if self._db:
            return self._db
        filename = f"plugin_{self.name}"
        db = Database(f"sqlite:///{VAR_PATH / filename}.sqlite", plugin=self)
        self._db = db
        return db

    @classmethod
    def get(cls, path: Path):
        id = cls.idify(path)
        return cls.all.get(id) or cls(path)

    @staticmethod
    def idify(path: Path):
        """Converts / to . relative to current directory
        >>> Plugin.idify(Path("plugins/sdvx"))
        'plugins.sdvx'
        """
        if isinstance(path, str):
            path = Path(path)
        if path.is_absolute():
            path = path.relative_to(Path.cwd())
        if path.name == "__init__.py":
            path = path.parent
        return ".".join(path.parts)

    @classmethod
    @property
    def current(cls) -> "Plugin":
        """
        Resolves to the plugin that called this function, by looking at last
        occurence of a plugin in the stack trace
        """
        for frame in inspect.stack():
            if frame.filename.startswith("<"):
                continue
            path = Path(frame.filename)
            if not path.is_relative_to(Path.cwd()):
                continue
            path = path.relative_to(Path.cwd())
            id = cls.idify(path)
            for plugin in cls.all:
                if id.startswith(plugin):
                    return cls.all[plugin]

    @classmethod
    @property
    def Database(cls) -> Database:
        """
        Returns the Database object of the current plugin, see
        Plugin.current for how the current plugin is resolved
        """
        return cls.current.db

    @classmethod
    @property
    def Table(cls):
        """
        Returns the Base object of the current plugin database, see
        Plugin.current for how the current plugin is resolved
        """
        return cls.Database.Base

    @classmethod
    def Router(cls):
        return APIRouter(prefix=f"/{cls.current.name}")

    @classmethod
    @property
    def Session(cls):
        """
        Returns the Session object of the current plugin database, see
        Plugin.current for how the current plugin is resolved
        """
        return cls.Database.session
