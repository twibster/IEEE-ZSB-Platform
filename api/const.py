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


default_permissions = {
    Positions.CHAIRMAN: {
        'view_task': True,
        'create_task': True,
        'modify_task': True,
        'delete_task': True,
        'view_user': True,
        'confirm_user': True,
        'modify_user': True,
        'delete_user': True
    },
    Positions.LEADER: {
        'view_task': True,
        'create_task': True,
        'modify_task': True,
        'delete_task': True,
        'modify_user': True
    },
    Positions.MEMBER: {
        'view_task': True,
        'submit_task': True,
        'excuse_task': True,
        'modify_user': True
    },
    Positions.ROOKIE: {
        'view_task': True,
        'submit_task': True,
        'excuse_task': True,
        'modify_user': True
    }
}
