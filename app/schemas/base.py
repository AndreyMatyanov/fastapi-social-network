from enum import Enum


class EnumBaseLower(str, Enum):
    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value == value.lower():
                return member


class EnumBaseUpper(str, Enum):
    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value == value.upper():
                return member


class OrderingType(EnumBaseLower):
    ASC = "asc"
    DESC = "desc"
