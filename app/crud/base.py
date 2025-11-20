from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.database.base_class import Base
from app.schemas.utils import DatabaseAction

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def handle_session(self, db: AsyncSession, action: DatabaseAction):
        """
        Handles database session actions using a dispatch table pattern.

        This method maps `DatabaseAction` enum values to corresponding
        session operations (commit, flush, or none) using a dictionary-based
        dispatch table. This approach is a Pythonic implementation of the
        Command Pattern, simplifying control flow and improving extensibility.

        Parameters:
            db (Session): SQLAlchemy database session instance.
            action (DatabaseAction): Enum representing the desired session action.

        Raises:
            NotImplementedError: If the action is not recognized.
        """
        action_map: Dict[DatabaseAction, Callable[[], Coroutine[Any, Any, None]]] = {
            DatabaseAction.COMMIT: db.commit,
            DatabaseAction.FLUSH: db.flush,
        }
        try:
            await action_map[action]()
        except KeyError:
            raise NotImplementedError(f"Action {action} is not implemented")

    async def get(self, db: AsyncSession, id: UUID) -> Optional[ModelType]:
        query = select(self.model).filter(self.model.id == id)
        result = await db.execute(query)
        result = result.scalars().first()
        return result

    def total(self, db: Session) -> int:
        return db.query(self.model).count()

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: CreateSchemaType,
        action: DatabaseAction = DatabaseAction.COMMIT,
    ) -> ModelType:
        # obj_in_data = jsonable_encoder(obj_in)
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await self.handle_session(db, action=action)
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        action: DatabaseAction = DatabaseAction.COMMIT,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await self.handle_session(db, action=action)
        await db.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db: AsyncSession,
        *,
        id: UUID,
        action: DatabaseAction = DatabaseAction.COMMIT,
    ) -> Optional[ModelType]:
        obj = await db.get(self.model, id)
        if obj is not None:
            await db.delete(obj)
            await self.handle_session(db, action=action)
            return cast(ModelType, obj)
        return None

    async def bulk_fetch_by_ids(
        self,
        db: AsyncSession,
        *,
        ids: List[UUID],
    ) -> List[ModelType]:
        if not ids:
            stmt = select(self.model)
        else:
            stmt = select(self.model).where(self.model.id.in_(ids))
        result = await db.execute(stmt)
        db_objs = list(result.scalars().all())
        return db_objs
    
    async def fetch_all(
        self,
        db: AsyncSession,
    ) -> List[ModelType]:
        stmt = select(self.model)
        result = await db.execute(stmt)
        db_objs = list(result.scalars().all())
        return db_objs

    async def deactivate(
        self, db: AsyncSession, db_obj: ModelType
    ) -> Optional[ModelType]:
        if db_obj:
            if hasattr(db_obj, "is_active"):
                db_obj.is_active = False
                db.add(db_obj)
                await db.commit()
                await db.refresh(db_obj)
            else:
                raise AttributeError(
                    f"{self.model.__name__} has no attribute 'is_active'"
                )
        return db_obj

    async def reactivate(
        self, db: AsyncSession, db_obj: ModelType
    ) -> Optional[ModelType]:
        if db_obj:
            if hasattr(db_obj, "is_active"):
                db_obj.is_active = True
                db.add(db_obj)
                await db.commit()
                await db.refresh(db_obj)
            else:
                raise AttributeError(
                    f"{self.model.__name__} has no attribute 'is_active'"
                )
        return db_obj
