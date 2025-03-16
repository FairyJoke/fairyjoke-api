import humps
from sqlalchemy.orm import DeclarativeBase, declared_attr


def _pluralize(name: str) -> str:
    if not name.endswith("s"):
        if name.endswith("y"):
            name = name[:-1] + "ie"
        name += "s"
    return name


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = humps.decamelize(cls.__name__)
        name = _pluralize(name)

        return name
