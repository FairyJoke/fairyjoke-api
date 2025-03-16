import datetime

from pydantic import BaseModel

from fairyjoke import Plugin

from .db import Music


class MusicModel(BaseModel):
    id: int
    title: str
    artist: str
    bpm: str
    version: int
    distribution_date: datetime.date
    difficulties: list["DifficultyModel"]

    class Config:
        from_attributes = True


class DifficultyModel(BaseModel):
    class Radar(BaseModel):
        notes: int
        peak: int
        tsumami: int
        tricky: int
        hand_trip: int
        one_hand: int

    name: str
    level: int
    illustrator: str
    effector: str
    max_ex_score: int
    radar: Radar

    class Config:
        from_attributes = True


@Plugin.Router().get("/musics/")
def musics():
    with Plugin.Session() as s:
        return [MusicModel.model_validate(x) for x in s.query(Music)]


@Plugin.Router().get("/musics/{id}/")
def music(id: int) -> MusicModel:
    with Plugin.Session() as s:
        return MusicModel.model_validate(s.query(Music).get(id))
