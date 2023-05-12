from sqlalchemy import event
from sqlalchemy.orm import LoaderCallableStatus, Session
from backend.database.models import Permission, User
from backend.constants import default_permissions


@event.listens_for(Session, "after_flush")  
def create_relationship(session, context) -> None:
    for obj in session.new:
        if isinstance(obj, User):
            permissions = Permission(**default_permissions[obj.position])
            permissions.user = obj
            session.add(permissions)        


@event.listens_for(User.position, "set", propagate=True)
def restore_default_permissions(
        user: User, position, old_position, initiator
        ) -> None:
    if (position != old_position and
        old_position != LoaderCallableStatus.NO_VALUE):
        for permission in Permission.__table__.columns:
            # check if this columns has a default position to avoid columns like id
            if permission.default:  
                default_permission = default_permissions[position].get(permission.name)
                default_permission = default_permission if default_permission else permission.default.arg
                setattr(user.permissions, permission.name, default_permission)
