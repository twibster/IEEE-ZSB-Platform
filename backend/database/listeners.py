from fastapi import Depends
from sqlalchemy import event
from sqlalchemy.orm import LoaderCallableStatus, Session
from backend.database.models import Permission, User
from backend.constants import Positions
from backend.dependencies import get_db

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


@event.listens_for(User, "after_insert")
def add_default_permissions(
            mapper, connection, user: User, db: Session = Depends(get_db)
        ) -> None:
    permissions = Permission(**default_permissions[user.position])

    @event.listens_for(Session, "after_flush")  # do the relatedObject creation after flushing to avoid warnings
    def create_relationship(session, context) -> None:
        permissions.user = user
        db.add(permissions)


@event.listens_for(User.position, "set", propagate=True)
def restore_default_permissions(user: User, value, old_value, _) -> None:
    if value != old_value and old_value != LoaderCallableStatus.NO_VALUE:
        for permission in Permission.__table__.columns:
            if permission.default:  # check if this columns has a default value to avoid columns like id
                default_permission = default_permissions[value].get(permission.name)
                if default_permission:
                    setattr(user.permissions, permission.name, default_permission)
                else:
                    setattr(user.permissions, permission.name, permission.default.arg)
                
