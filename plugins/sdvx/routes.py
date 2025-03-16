from fairyjoke import Plugin

from .db import Music


@Plugin.Router().get("/musics/")
def musics():
    with Music.Session() as s:
        return s.query(Music).all()


@Plugin.Router().get("/musics/{id}/")
def music(id: int):
    with Music.Session() as s:
        return s.query(Music).get(id)
