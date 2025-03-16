import datetime

from fairyjoke import Plugin, log

from .db import Difficulty, Music


def process_music_db(path):
    with Plugin.Session() as s:
        for music in Plugin.Data().load(path):
            id = int(music.get("id"))
            log.info(f"Processing music {id} from music_db")

            values = {}
            title = music.parse("info/title_name")
            # SDVX uses some custom characters in song titles that are not
            # in standard encodings
            for old, new in Plugin.Data().special_chars.items():
                title = title.replace(old, new)
            date = str(music.parse("info/distribution_date"))
            date = datetime.date.fromisoformat(
                f"{date[:4]}-{date[4:6]}-{date[6:8]}"
            )
            values = music.parse_all(
                artist="info/artist_name",
                bpm_min="info/bpm_min",
                bpm_max="info/bpm_max",
                version="info/version",
            )
            values["title"] = title
            values["distribution_date"] = date
            values["bpm_min"] /= 100
            values["bpm_max"] /= 100

            s.upsert(Music, values, id=id)

            for difficulty in music.find("difficulty"):
                name = difficulty.tag
                level = difficulty.parse("difnum")
                if level == 0:
                    continue
                values = difficulty.parse_all(
                    illustrator="illustrator",
                    effector="effected_by",
                    max_ex_score="max_exscore",
                    radar_notes="radar/notes",
                    radar_peak="radar/peak",
                    radar_tsumami="radar/tsumami",
                    radar_tricky="radar/tricky",
                    radar_hand_trip="radar/hand-trip",
                    radar_one_hand="radar/one-hand",
                )
                values["level"] = level

                s.upsert(Difficulty, values, music_id=id, name=name)
        s.commit()


def main():
    for path in Plugin.Data().path.glob("music_db*.xml"):
        process_music_db(path)
