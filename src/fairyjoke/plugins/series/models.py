from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped as Column
from sqlalchemy.orm import mapped_column as column
from sqlalchemy.orm import relationship

from fairyjoke import Plugin


class Group(Plugin.Table):
    id: Column[str] = column(primary_key=True)
    name: Column[str]


class Series(Plugin.Table):
    id: Column[str] = column(primary_key=True)
    name: Column[str]
    translation: Column[str] = column(nullable=True)
    active: Column[bool] = True
    group_id: Column[int] = column(ForeignKey("groups.id"), nullable=True)

    group: Column[Group] = relationship("Group", backref="series")


class Game(Plugin.Table):
    id: Column[str] = column(primary_key=True)
    series_id: Column[str] = column(ForeignKey("series.id"))
    name: Column[str]
    date: Column[str]

    series: Column[Series] = relationship("Series", backref="series")
