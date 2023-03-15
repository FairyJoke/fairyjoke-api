import sqlalchemy as sa

from fairyjoke import Plugin


class Song(Plugin.Table):
    title = sa.Column(sa.String)
