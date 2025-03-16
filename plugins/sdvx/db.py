import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from fairyjoke import Plugin


class Music(Plugin.Table()):
    id: int = mapped_column(primary_key=True)
    title: str = mapped_column()
    artist: str = mapped_column()
    bpm_min: float = mapped_column()
    bpm_max: float = mapped_column()
    version: int = mapped_column()
    distribution_date: datetime.date = mapped_column()

    difficulties = relationship("Difficulty", back_populates="music")

    @property
    def bpm(self):
        if self.bpm_min == self.bpm_max:
            return f"{self.bpm_min:g}"
        return f"{self.bpm_min:g} - {self.bpm_max:g}"

    def __str__(self):
        return f"Music {self.id} {self.title}"


class Difficulty(Plugin.Table()):
    music_id: int = mapped_column(ForeignKey(Music.id), primary_key=True)
    name: str = mapped_column(primary_key=True)

    level: int = mapped_column()
    illustrator: str = mapped_column()
    effector: str = mapped_column()
    max_ex_score: int = mapped_column()
    radar_notes: int = mapped_column()
    radar_peak: int = mapped_column()
    radar_tsumami: int = mapped_column()
    radar_tricky: int = mapped_column()
    radar_hand_trip: int = mapped_column()
    radar_one_hand: int = mapped_column()

    @property
    def radar(self):
        columns = [
            "notes",
            "peak",
            "tsumami",
            "tricky",
            "hand_trip",
            "one_hand",
        ]
        return {k: getattr(self, f"radar_{k}") for k in columns}

    music = relationship("Music", back_populates="difficulties", uselist=False)

    def __str__(self):
        return f"{self.name.upper()} {self.level} of {self.music_id}"
