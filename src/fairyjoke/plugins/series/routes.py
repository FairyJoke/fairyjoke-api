from pydantic import BaseModel

from fairyjoke import Plugin


class Series(BaseModel):
    name: str
    active: bool = True
    group: str = None


@Plugin.Router().get("/")
async def index() -> list[Series]:
    """Lists rhythm games series"""

    result = [Series(**x) for x in Plugin.Data().all]
    result.sort(key=lambda x: x.name.lower())
    return result
