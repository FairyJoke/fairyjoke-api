import sqlalchemy as sa

from fairyjoke import Plugin

db = Plugin.db


class Song(db.Base):
    title = sa.Column(sa.String)
