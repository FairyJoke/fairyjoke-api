from sqlalchemy.orm import mapped_column

from fairyjoke import Plugin


class Music(Plugin.Table()):
    id: int = mapped_column(primary_key=True)
    title: str = mapped_column()

    def __str__(self):
        return f"Music #{self.id} {self.title}"
