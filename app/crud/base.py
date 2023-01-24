from datetime import datetime
from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.db.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    _updated_at_field = "updated_at"

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """

        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        query = db.query(self.model).filter_by(id=id)
        result = query.first()
        return result

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_batch(
        self, db: Session, *, objs_in: list[Union[CreateSchemaType, Dict[str, Any]]]
    ) -> list[ModelType]:
        objs_in_data = []
        for obj_in in objs_in:
            obj_in_data = (
                obj_in if isinstance(obj_in, dict) else jsonable_encoder(obj_in)
            )
            objs_in_data.append(obj_in_data)

        result = None
        if "id" in self.model.__table__.columns.keys():
            expr = insert(self.model).values(objs_in_data).returning(self.model.id)
            result = db.execute(expr).all()
        else:
            expr = insert(self.model).values(objs_in_data)
            db.execute(expr)
        db.commit()

        db_objs = []
        for count, obj_in_data in enumerate(objs_in_data):
            if result:
                obj_in_data["id"] = result[count][0]
            db_obj = self.model(**obj_in_data)
            db_objs.append(db_obj)
        return db_objs

    # TODO fix hardcode for prize_distribution
    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = (
            obj_in
            if isinstance(obj_in, dict)
            else obj_in.dict(exclude_unset=True, exclude_none=True)
        )
        if (
            self._updated_at_field in self.model.__dict__
            and self._updated_at_field not in update_data
        ):
            update_data[self._updated_at_field] = datetime.now()

        for field in obj_data:
            if field in update_data:
                if field == "prize_distribution":
                    for item in update_data[field]:
                        item["prize"] = str(item["prize"])
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_multi(
        self, db: Session, *, ids: list[Union[int, UUID]], obj_in: UpdateSchemaType
    ) -> None:
        query = db.query(self.model).filter(self.model.id.in_(ids))
        query.update(obj_in.dict(exclude_unset=True, exclude_none=True))
        db.commit()

    def remove(self, db: Session, *, id: int) -> Optional[ModelType]:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
