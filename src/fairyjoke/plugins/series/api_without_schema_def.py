import sqlalchemy as sa

from fairyjoke import Plugin


class SeriesSchema(Plugin.Schema):
    __url__ = ""
    id: str
    name: str
    translation: str = None


class GameSchema(Plugin.Schema):
    __url__ = "/{series_id}/games"
    id: str
    series_id: str
    name: str
    date: str = None

    @classmethod
    def get_all(cls, series_id):
        with Plugin.Session() as s:
            statement = sa.select(cls._table).where(
                cls._table.series_id == series_id
            )
            return s.execute(statement).scalars().all()

    @classmethod
    def get_one(cls, series_id, id):
        with Plugin.Session() as s:
            return s.get(cls._table, (series_id, id))


class GroupSchema(Plugin.Schema):
    id: str
    name: str
