from enum import Enum, EnumMeta
from typing import Any


class StreetNinjaEnumMeta(EnumMeta):

    @property
    def choices(cls) -> list[tuple[str, str]]:
        """Returns a list of tuplesav that can be used in models.CharField's choices property.
        Example:
            [
                ("red", "Red"),
                ("blue", "Blue"),
            ]
        """
        return [(enum.value, enum.name.replace("_", " ").title()) for enum in cls]  # type: ignore

    @property
    def values(cls) -> list[Any]:
        return [enum.value for _, enum in cls.__members__.items()]  # type: ignore


class StreetNinjaEnum(Enum, metaclass=StreetNinjaEnumMeta):
    pass
