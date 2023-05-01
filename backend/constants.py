from enum import Enum


class Positions(str, Enum):
    CHAIRMAN = "chairman"
    LEADER = "leader"
    MEMBER = "member"
    ROOKIE = "rookie"


class Chapters(str, Enum):
    RAS, PES, CS = "ras", "pes", "cs"


class Departments(str, Enum):
    ES = "embedded systems"
    AI = "ai"
    ROS = "ros"
    MECHANICAL = "mechanical"
    MOBILE = "mobile"
    WEB = "web"
    POWER = "power"
    DISTRIBUTION = "distribution"