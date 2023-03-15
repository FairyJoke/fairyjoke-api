import importlib
import inspect
from pathlib import Path

from sqlalchemy_setup import Database

from fairyjoke import VAR_PATH


class Plugin:
    all = {}

    def __init__(self, path: Path | str):
        self.id = self.idify(path)
        self.name = self.id.split(".")[-1]
        self.module = importlib.import_module(self.id)
        self._db = None
        print("Found module", self.module.__name__)
        self.all[self.id] = self

    def init(self):
        # We access the "models" submodule to trigger the creation of the
        # tables
        models_module_str = f"{self.id}.models"
        try:
            importlib.import_module(models_module_str)
        except ModuleNotFoundError as e:
            if e.name != models_module_str:
                raise e
        # If "Plugin.db" was accessed at least once, it should mean that tables
        # are defined, we then actually create them in the database
        if self._db:
            self.db.init()

    @property
    def db(self):
        if self._db:
            return self._db
        filename = f"plugin_{self.name}"
        db = Database(f"sqlite:///{VAR_PATH / filename}.sqlite")
        self._db = db
        return db

    @classmethod
    def get(cls, path: Path):
        id = cls.idify(path)
        return cls.all.get(id) or cls(path)

    @staticmethod
    def idify(path: Path):
        """
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
        Resolves to the plugin that called this function
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
    def Database(cls):
        return cls.current.db

    @classmethod
    @property
    def Table(cls):
        return cls.Database.Base
