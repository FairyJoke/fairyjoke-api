from pydantic import BaseModel

from fairyjoke import Plugin


class Schema(BaseModel):
    __url__ = None
    __table__ = None

    class Config:
        from_attributes = True

    @classmethod
    @property
    def _route_name(cls):
        if cls.__url__ is not None:
            return cls.__url__
        name = cls.__name__.lower()
        name = name.removesuffix("schema")
        if not name.endswith("s"):
            name += "s"
        if name:
            name = "/" + name
        return name

    @classmethod
    @property
    def _table(cls):
        if cls.__table__ is not None:
            return cls.__table__
        table_name = cls.__name__.removesuffix("Schema")
        return Plugin.Table.get_model(table_name)

    @classmethod
    def get_all(cls):
        with Plugin.Session() as s:
            statement = sa.select(cls._table)
            return s.execute(statement).scalars().all()

    @classmethod
    def get_one(cls, id):
        with Plugin.Session() as s:
            return s.get(cls._table, id)

    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.router = Plugin.Router()

        cls.router.add_api_route(
            f"{cls._route_name}/",
            cls.get_all,
            name=f"Get all {cls._table.__name__}",
        )
        cls.router.add_api_route(
            f"{cls._route_name}/{{id}}",
            cls.get_one,
            name=f"Get one {cls._table.__name__} by ID",
        )
