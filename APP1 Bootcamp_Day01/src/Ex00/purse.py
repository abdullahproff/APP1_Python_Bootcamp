from enum import Enum

PurseType = dict[str, int]

class PurseFields(str, Enum):
    GI = "gold_ingots"

def empty() -> PurseType:
    return {}


def add_ingot(purse: PurseType) -> PurseType:
    ingots = purse.get(PurseFields.GI, 0)
    return {PurseFields.GI.value: ingots + 1}


def get_ingot(purse: PurseType) -> PurseType:
    ingots = purse.get(PurseFields.GI, 0)
    if not ingots:
        raise ValueError("the purse is already empty")
    return {PurseFields.GI.value: ingots - 1}