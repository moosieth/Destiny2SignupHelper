from enum import Enum


class ActivityType(Enum):
    RAI = "Raid"
    DUN = "Dungeon"
    RIT = "Ritual"
    STO = "Story"
    MISC = "Other"


class Raids(Enum):
    LW = "Last Wish"
    GOS = "Garden of Salvation"
    DSC = "Deep Stone Crypt"
    VOG = "Vault of Glass"
    VOTD = "Vow of the Disciple"
    KF = "King's Fall"
    RON = "Root of Nightmares"
    CE = "Crota's End"
    SE = "Salvation's Edge"


class Dungeons(Enum):
    ST = "The Shattered Throne"
    POH = "Pit of Heresy"
    PRO = "Prophecy"
    GOA = "Grasp of Avarice"
    DUA = "Duality"
    SOTW = "Spire of the Watcher"
    GOTD = "Ghosts of the Deep"
    WR = "Warlord's Ruin"
    VH = "Vesper's Host"


class Rituals(Enum):
    CRU = "Crucible"
    VAN = "Vanguard Ops"
    GAM = "Gambit"
    ONS = "Onslaught"
    TOS = "Trials of Osiris"
    IB = "Iron Banner"
