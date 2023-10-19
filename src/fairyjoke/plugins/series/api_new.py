import typing as t

from fairyjoke import Plugin

# Dummy implementation of the new API:


def route():
    pass


SeriesSchema = GameSchema = GroupSchema = type

# New target usage:


class GroupSchema(Plugin.Schema):
    id: str
    name: str


class SeriesSchema(Plugin.Schema):
    id: str
    name: str
    translation: t.Optional[str]
    active: bool
    group: t.Optional[GroupSchema]


class GameSchema(Plugin.Schema):
    id: str
    name: str
    date: str


# These two could be implicit
@Plugin.route("/series/")
def search_series():
    return SeriesSchema.search()


@Router.route("/series/{id}")
def get_series(id):
    return SeriesSchema.get(id)


# These two would be harder to get an implicit implementation
@Plugin.route("/series/{series_id}/games")
def search_games_in_series(series_id):
    return GameSchema.search(series_id=series_id)


@Plugin.route("/games/")
def search_games():
    return GameSchema.search()


@Plugin.route("/{series_id}/games/{id}")
def get_game(series_id, id):
    return GameSchema.get(series_id, id)


@Plugin.route("/groups/")
def search_groups():
    return GroupSchema.search()
