import pathlib

from sqlalchemy import (
    create_engine,
    Integer, String, DateTime,
    Column, Table,
    ForeignKey,
    select, insert, update, func, PrimaryKeyConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.orm import relationship, sessionmaker, query
from sqlalchemy.orm.session import Session
from typing import List, Optional, Type, TypeVar, Union

engine = create_engine('sqlite:///database.db', echo=True)
SessionObj = sessionmaker(engine)
Base = declarative_base()

tag_new = Table("tags_news", Base.metadata,
                Column("tag_id", ForeignKey("tags.id", name='tag_new_tag_id_foreign')),
                Column("new_id", ForeignKey("news.id", name='tag_new_new_id_foreign'))
                )

T = TypeVar('T', bound='DefaultFunctions')


class DefaultFunctions:

    @classmethod
    def create(cls: Type[T], **kwargs) -> T:
        obj = cls(**kwargs)
        with SessionObj() as session:
            session.add(obj)
            session.commit()
        return obj

    def update(self, **kwargs) -> Optional[Type[T]]:
        table: Table = self.__table__
        key: PrimaryKeyConstraint = table.primary_key

        if len(key.columns) == 0:
            raise Exception('У объекта отсутствует primary_key')

        key_first = key.columns[0]

        with SessionObj() as session:
            session: Session = session
            session.query(table)\
                .where(key_first == self.id)\
                .update(kwargs, synchronize_session=False)
            session.commit()

        return self.first(key_first == self.id)

    def delete(self):
        table: Table = self.__table__
        key: PrimaryKeyConstraint = table.primary_key

        if len(key.columns) == 0:
            raise Exception('У объекта отсутствует primary_key')

        key_first = key.columns[0]

        with SessionObj() as session:
            session: Session = session
            session.query(table) \
                .where(key_first == self.id) \
                .delete(synchronize_session=False)
            session.commit()

    @classmethod
    def get(cls: Type[T], *args) -> Union[List[T]]:
        with SessionObj() as session:
            session: Session = session
            result: query.Query = session.query(cls) \
                .where(*args)

        return result.all()

    @classmethod
    def count(cls: Type[T], *args) -> int:
        with SessionObj() as session:
            session: Session = session
            result = session.query(cls) \
                .where(*args) \
                .count()

        return result

    @classmethod
    def first(cls: Type[T], *args) -> Optional[Type[T]]:
        with SessionObj() as session:
            session: Session = session
            result: query.Query = session.query(cls) \
                .where(*args)

        return result.first()


class Tag(Base, DefaultFunctions):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class New(Base, DefaultFunctions):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # created_at = Column(DateTime)
    tags = relationship("Tag", secondary=tag_new)

    # def update(self, *args, **kwargs):
    #     self.
