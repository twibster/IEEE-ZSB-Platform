from fastapi import status
from sqlalchemy.orm import Mapper, Session
from api.depend import get_db
from api.db.models import User


def get_all(mapper: Mapper, db: Session = next(get_db())) -> Mapper:
    return db.query(mapper).all()


def get_by_id(mapper: Mapper, id: int, db: Session = next(get_db())) -> Mapper:
    return db.query(mapper).filter_by(id=id).first()


def get_by_email(email: str, db: Session = next(get_db())) -> Mapper:
    return db.query(User).filter_by(email=email).first()


def get_by_username(username: str, db: Session = next(get_db())) -> Mapper:
    return db.query(User).filter_by(username=username).first()


def update_by_id(mapper: Mapper, id: int,
                 modified: dict, db: Session = next(get_db())) -> Mapper:
    instance = get_by_id(mapper, id)
    if instance:
        instance.update(**modified)
        db.commit()
        return status.HTTP_204_NO_CONTENT, "updated"
    return status.HTTP_404_NOT_FOUND, "not found"


def delete_by_id(mapper: Mapper,
                 id: int, db: Session = next(get_db())) -> Mapper:
    instance = get_by_id(mapper, id)
    if instance:
        db.delete(instance)
        db.commit()
        return status.HTTP_204_NO_CONTENT, "deleted"
    return status.HTTP_404_NOT_FOUND, "not found"
