from sqlalchemy.ext.declarative import DeclarativeMeta

from movies_auth.app import db


def delete_objects_by_id(objects: list[DeclarativeMeta]) -> None:
    if not objects:
        return

    model_class = type(objects[0])
    item_ids = [item.id for item in objects]
    db.session.query(model_class).filter(model_class.id.in_(item_ids)).delete()
    db.session.commit()


def delete_object_by_attribute(item: DeclarativeMeta, attribute: str) -> None:
    model_class = type(item)
    db.session.query(model_class).filter_by(**{attribute: getattr(item, attribute)}).delete()
    db.session.commit()
