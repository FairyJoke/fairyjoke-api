from fairyjoke import log
from fairyjoke.plugin import Plugin

from .db import Music


def main():
    for music in Plugin.Data().music_db:
        id = int(music.get("id"))
        log.info(f"Processing music {id} from music_db")
        with Plugin.Table().Session() as s:
            row = s.query(Music).get(id)
            if not row:
                log.info(f"Creating music {id}")
                row = Music(id=id)
                s.add(row)
                s.commit()
            title = music.find("info/title_name").text
            # SDVX uses some custom characters in song titles that are not
            # in standard encodings
            for k, v in Plugin.Data().special_chars.items():
                title = title.replace(k, v)
            if title != row.title:
                row.title = title
                log.info(f"Updated {row}")
                s.commit()
