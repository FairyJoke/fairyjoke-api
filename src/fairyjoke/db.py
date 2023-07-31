from collections.abc import Iterator
from contextlib import contextmanager
from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, declared_attr


class Base(DeclarativeBase):
    prefix = False
    plugin = None

    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = ""
        for c in cls.__name__:
            if name and name[-1] != "_" and c.isupper():
                name += "_"
            name += c.lower()

        if not name.endswith("s"):
            name += "s"
        if cls.prefix:
            if isinstance(cls.prefix, str):
                prefix = cls.prefix
            else:
                prefix = cls.plugin.name
            name = f"{prefix}_{name}"
        return name


class Database:
    """
    Helper class to manage the database connection and session
    Exposes the SQLAlchemy Base and Session objects
    """

    def __init__(self, uri: str, plugin=None):
        class SelfBase(Base, DeclarativeBase):
            _models = {}

            def __init_subclass__(cls):
                super().__init_subclass__()
                cls._models[cls.__name__] = cls

            @classmethod
            def get_model(cls, name) -> Type[Base]:
                return cls._models[name]

        protocol, path = uri.split(":", 1)
        # We override some protocols as the URI should not show any Python
        # specific stuff
        protocol = {
            "sqlite": "sqlite+pysqlite",
        }.get(protocol, protocol)
        uri = f"{protocol}:{path}"
        self.engine = create_engine(uri)
        self.Base = SelfBase
        self.Base.plugin = plugin

    @contextmanager
    def session(self) -> Iterator[Session]:
        with Session(self.engine, expire_on_commit=False) as s:
            # Disabling expire_on_commit allows us to access the objects after
            # the session is closed or committed, which happens as soon as the
            # context manager exits
            with s.begin():
                yield s

    def init(self):
        """
        Create the tables in the database
        """
        self.Base.metadata.create_all(self.engine)
