import pathlib

from sqlalchemy import (
    create_engine,
    Integer, String, DateTime,
    Column, Table,
    ForeignKey,
    select, insert, update, exists, func, PrimaryKeyConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, query
from sqlalchemy.orm.session import Session
from typing import List, Optional, Type, TypeVar, Union

engine = create_engine('sqlite:///database.sqlite', echo=False)
SessionObj = sessionmaker(engine)
Base = declarative_base()

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
    def get(cls: Type[T], *args) -> List[T]:
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
    
    @classmethod
    def exists(cls: Type[T], *args) -> bool:
        with SessionObj() as session:
            session: Session = session
            result: query.Query = session.query(
                    exists().where(*args)
                ) 

        return result.scalar()

class Tag(Base, DefaultFunctions):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
class Image(Base, DefaultFunctions):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    path = Column(String, nullable=False)
    
class Template(Base, DefaultFunctions):
    __tablename__ = 'templates'

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)

class Property(Base, DefaultFunctions):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)

class Group(Base, DefaultFunctions):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
class Activity(Base, DefaultFunctions):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey(Image.id, name='activities_image_id_foreign'), nullable=True)
    description = Column(String, nullable=True)
    preview = Column(String, nullable=True)
    preview_image_id = Column(Integer, ForeignKey(Image.id, name='activities_preview_image_id_foreign'), nullable=True)
    created_at = Column(DateTime, nullable=False)
    unpublished_at = Column(DateTime, nullable=True)
    tags = relationship("Tag", secondary=Table("tags_activities", Base.metadata,
        Column("tag_id", ForeignKey("tags.id", name='tag_activity_tag_id_foreign')),
        Column("activity_id", ForeignKey("activities.id", name='tag_activity_activity_id_foreign'))
    ))
    templates = relationship("Template", secondary=Table("templates_activities", Base.metadata,
        Column("template_id", ForeignKey("templates.id", name='template_activity_template_id_foreign')),
        Column("activity_id", ForeignKey("activities.id", name='template_activity_activity_id_foreign'))
    ))
    groups = relationship("Group", secondary=Table("groups_activities", Base.metadata,
        Column("group_id", ForeignKey("groups.id", name='group_activity_group_id_foreign')),
        Column("activity_id", ForeignKey("activities.id", name='group_activity_activity_id_foreign'))
    ))
    properties = relationship("Property", secondary=Table("properties_activities", Base.metadata,
        Column("property_id", ForeignKey("properties.id", name='property_activity_property_id_foreign')),
        Column("activity_id", ForeignKey("activities.id", name='property_activity_activity_id_foreign'))
    ))
    
class FAQ(Base, DefaultFunctions):
    __tablename__ = 'faq'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey(Image.id, name='faq_image_id_foreign'), nullable=True)
    description = Column(String, nullable=True)
    preview = Column(String, nullable=True)
    preview_image_id = Column(Integer, ForeignKey(Image.id, name='faq_preview_image_id_foreign'), nullable=True)
    created_at = Column(DateTime, nullable=False)
    unpublished_at = Column(DateTime, nullable=True)
    tags = relationship("Tag", secondary=Table("tags_faq", Base.metadata,
        Column("tag_id", ForeignKey("tags.id", name='tag_faq_tag_id_foreign')),
        Column("faq_id", ForeignKey("faq.id", name='tag_faq_faq_id_foreign'))
    ))
    templates = relationship("Template", secondary=Table("templates_faq", Base.metadata,
        Column("template_id", ForeignKey("templates.id", name='template_faq_template_id_foreign')),
        Column("faq_id", ForeignKey("faq.id", name='template_faq_faq_id_foreign'))
    ))
    groups = relationship("Group", secondary=Table("groups_faq", Base.metadata,
        Column("group_id", ForeignKey("groups.id", name='group_faq_group_id_foreign')),
        Column("faq_id", ForeignKey("faq.id", name='group_faq_faq_id_foreign'))
    ))
    properties = relationship("Property", secondary=Table("properties_faq", Base.metadata,
        Column("property_id", ForeignKey("properties.id", name='property_faq_property_id_foreign')),
        Column("faq_id", ForeignKey("faq.id", name='property_faq_faq_id_foreign'))
    ))
    
class Catalog(Base, DefaultFunctions):
    __tablename__ = 'catalog'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey(Image.id, name='catalog_image_id_foreign'), nullable=True)
    description = Column(String, nullable=True)
    preview = Column(String, nullable=True)
    preview_image_id = Column(Integer, ForeignKey(Image.id, name='catalog_preview_image_id_foreign'), nullable=True)
    created_at = Column(DateTime, nullable=False)
    unpublished_at = Column(DateTime, nullable=True)
    tags = relationship("Tag", secondary=Table("tags_catalog", Base.metadata,
        Column("tag_id", ForeignKey("tags.id", name='tag_catalog_tag_id_foreign')),
        Column("catalog_id", ForeignKey("catalog.id", name='tag_catalog_catalog_id_foreign'))
    ))
    templates = relationship("Template", secondary=Table("templates_catalog", Base.metadata,
        Column("template_id", ForeignKey("templates.id", name='template_catalog_template_id_foreign')),
        Column("catalog_id", ForeignKey("catalog.id", name='template_catalog_catalog_id_foreign'))
    ))
    groups = relationship("Group", secondary=Table("groups_catalog", Base.metadata,
        Column("group_id", ForeignKey("groups.id", name='group_catalog_group_id_foreign')),
        Column("catalog_id", ForeignKey("catalog.id", name='group_catalog_catalog_id_foreign'))
    ))
    properties = relationship("Property", secondary=Table("properties_catalog", Base.metadata,
        Column("property_id", ForeignKey("properties.id", name='property_catalog_property_id_foreign')),
        Column("catalog_id", ForeignKey("catalog.id", name='property_catalog_catalog_id_foreign'))
    ))
    
class Laboratory(Base, DefaultFunctions):
    __tablename__ = 'laboratories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey(Image.id, name='laboratories_image_id_foreign'), nullable=True)
    description = Column(String, nullable=True)
    preview = Column(String, nullable=True)
    preview_image_id = Column(Integer, ForeignKey(Image.id, name='laboratories_preview_image_id_foreign'), nullable=True)
    created_at = Column(DateTime, nullable=False)
    unpublished_at = Column(DateTime, nullable=True)
    tags = relationship("Tag", secondary=Table("tags_laboratories", Base.metadata,
        Column("tag_id", ForeignKey("tags.id", name='tag_laboratory_tag_id_foreign')),
        Column("laboratory_id", ForeignKey("laboratories.id", name='tag_laboratory_laboratory_id_foreign'))
    ))
    templates = relationship("Template", secondary=Table("templates_laboratories", Base.metadata,
        Column("template_id", ForeignKey("templates.id", name='template_laboratory_template_id_foreign')),
        Column("laboratory_id", ForeignKey("laboratories.id", name='template_laboratory_laboratory_id_foreign'))
    ))
    groups = relationship("Group", secondary=Table("groups_laboratories", Base.metadata,
        Column("group_id", ForeignKey("groups.id", name='group_laboratory_group_id_foreign')),
        Column("laboratory_id", ForeignKey("laboratories.id", name='group_laboratory_laboratory_id_foreign'))
    ))
    properties = relationship("Property", secondary=Table("properties_laboratories", Base.metadata,
        Column("property_id", ForeignKey("properties.id", name='property_laboratory_property_id_foreign')),
        Column("laboratory_id", ForeignKey("laboratories.id", name='property_laboratory_laboratory_id_foreign'))
    ))
    
class LibraryNew(Base, DefaultFunctions):
    __tablename__ = 'library_news'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey(Image.id, name='library_news_image_id_foreign'), nullable=True)
    description = Column(String, nullable=True)
    preview = Column(String, nullable=True)
    preview_image_id = Column(Integer, ForeignKey(Image.id, name='library_news_preview_image_id_foreign'), nullable=True)
    created_at = Column(DateTime, nullable=False)
    unpublished_at = Column(DateTime, nullable=True)
    tags = relationship("Tag", secondary=Table("tags_library_news", Base.metadata,
        Column("tag_id", ForeignKey("tags.id", name='tag_library_new_tag_id_foreign')),
        Column("library_new_id", ForeignKey("library_news.id", name='tag_library_new_library_new_id_foreign'))
    ))
    templates = relationship("Template", secondary=Table("templates_library_news", Base.metadata,
        Column("template_id", ForeignKey("templates.id", name='template_library_new_template_id_foreign')),
        Column("library_new_id", ForeignKey("library_news.id", name='template_library_new_library_new_id_foreign'))
    ))
    groups = relationship("Group", secondary=Table("groups_library_news", Base.metadata,
        Column("group_id", ForeignKey("groups.id", name='group_library_new_group_id_foreign')),
        Column("library_new_id", ForeignKey("library_news.id", name='group_library_new_library_new_id_foreign'))
    ))
    properties = relationship("Property", secondary=Table("properties_library_news", Base.metadata,
        Column("property_id", ForeignKey("properties.id", name='property_library_new_property_id_foreign')),
        Column("library_new_id", ForeignKey("library_news.id", name='property_library_new_library_new_id_foreign'))
    ))
    
class ProfkomNew(Base, DefaultFunctions):
    __tablename__ = 'profkom_news'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey(Image.id, name='profkom_news_image_id_foreign'), nullable=True)
    description = Column(String, nullable=True)
    preview = Column(String, nullable=True)
    preview_image_id = Column(Integer, ForeignKey(Image.id, name='profkom_news_preview_image_id_foreign'), nullable=True)
    created_at = Column(DateTime, nullable=False)
    unpublished_at = Column(DateTime, nullable=True)
    tags = relationship("Tag", secondary=Table("tags_profkom_news", Base.metadata,
        Column("tag_id", ForeignKey("tags.id", name='tag_profkom_new_tag_id_foreign')),
        Column("profkom_new_id", ForeignKey("profkom_news.id", name='tag_profkom_new_profkom_new_id_foreign'))
    ))
    templates = relationship("Template", secondary=Table("templates_profkom_news", Base.metadata,
        Column("template_id", ForeignKey("templates.id", name='template_profkom_new_template_id_foreign')),
        Column("profkom_new_id", ForeignKey("profkom_news.id", name='template_profkom_new_profkom_new_id_foreign'))
    ))
    groups = relationship("Group", secondary=Table("groups_profkom_news", Base.metadata,
        Column("group_id", ForeignKey("groups.id", name='group_profkom_new_group_id_foreign')),
        Column("profkom_new_id", ForeignKey("profkom_news.id", name='group_profkom_new_profkom_new_id_foreign'))
    ))
    properties = relationship("Property", secondary=Table("properties_profkom_news", Base.metadata,
        Column("property_id", ForeignKey("properties.id", name='property_profkom_new_property_id_foreign')),
        Column("profkom_new_id", ForeignKey("profkom_news.id", name='property_profkom_new_profkom_new_id_foreign'))
    ))
    
class New(Base, DefaultFunctions):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey(Image.id, name='news_image_id_foreign'), nullable=True)
    description = Column(String, nullable=True)
    preview = Column(String, nullable=True)
    preview_image_id = Column(Integer, ForeignKey(Image.id, name='news_preview_image_id_foreign'), nullable=True)
    created_at = Column(DateTime, nullable=False)
    unpublished_at = Column(DateTime, nullable=True)
    tags = relationship("Tag", secondary=Table("tags_news", Base.metadata,
        Column("tag_id", ForeignKey("tags.id", name='tag_new_tag_id_foreign')),
        Column("new_id", ForeignKey("news.id", name='tag_new_new_id_foreign'))
    ))
    templates = relationship("Template", secondary=Table("templates_news", Base.metadata,
        Column("template_id", ForeignKey("templates.id", name='template_new_template_id_foreign')),
        Column("new_id", ForeignKey("news.id", name='template_new_new_id_foreign'))
    ))
    groups = relationship("Group", secondary=Table("groups_news", Base.metadata,
        Column("group_id", ForeignKey("groups.id", name='group_new_group_id_foreign')),
        Column("new_id", ForeignKey("news.id", name='group_new_new_id_foreign'))
    ))
    properties = relationship("Property", secondary=Table("properties_news", Base.metadata,
        Column("property_id", ForeignKey("properties.id", name='property_new_property_id_foreign')),
        Column("new_id", ForeignKey("news.id", name='property_new_new_id_foreign'))
    ))

class Equipment(Base, DefaultFunctions):
    __tablename__ = 'equipments'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey(Image.id, name='equipments_image_id_foreign'), nullable=True)
    description = Column(String, nullable=True)
    preview = Column(String, nullable=True)
    preview_image_id = Column(Integer, ForeignKey(Image.id, name='equipments_preview_image_id_foreign'), nullable=True)
    created_at = Column(DateTime, nullable=False)
    unpublished_at = Column(DateTime, nullable=True)
    tags = relationship("Tag", secondary=Table("tags_equipments", Base.metadata,
        Column("tag_id", ForeignKey("tags.id", name='tag_equipment_tag_id_foreign')),
        Column("equipment_id", ForeignKey("equipments.id", name='tag_equipment_equipment_id_foreign'))
    ))
    templates = relationship("Template", secondary=Table("templates_equipments", Base.metadata,
        Column("template_id", ForeignKey("templates.id", name='template_equipment_template_id_foreign')),
        Column("equipment_id", ForeignKey("equipments.id", name='template_equipment_equipment_id_foreign'))
    ))
    groups = relationship("Group", secondary=Table("groups_equipments", Base.metadata,
        Column("group_id", ForeignKey("groups.id", name='group_equipment_group_id_foreign')),
        Column("equipment_id", ForeignKey("equipments.id", name='group_equipment_equipment_id_foreign'))
    ))
    properties = relationship("Property", secondary=Table("properties_equipments", Base.metadata,
        Column("property_id", ForeignKey("properties.id", name='property_equipment_property_id_foreign')),
        Column("equipment_id", ForeignKey("equipments.id", name='property_equipment_equipment_id_foreign'))
    ))

class Patent(Base, DefaultFunctions):
    __tablename__ = 'patents'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey(Image.id, name='patents_image_id_foreign'), nullable=True)
    description = Column(String, nullable=True)
    preview = Column(String, nullable=True)
    preview_image_id = Column(Integer, ForeignKey(Image.id, name='patents_preview_image_id_foreign'), nullable=True)
    created_at = Column(DateTime, nullable=False)
    unpublished_at = Column(DateTime, nullable=True)
    tags = relationship("Tag", secondary=Table("tags_patents", Base.metadata,
        Column("tag_id", ForeignKey("tags.id", name='tag_patent_tag_id_foreign')),
        Column("patent_id", ForeignKey("patents.id", name='tag_patent_patent_id_foreign'))
    ))
    templates = relationship("Template", secondary=Table("templates_patents", Base.metadata,
        Column("template_id", ForeignKey("templates.id", name='template_patent_template_id_foreign')),
        Column("patent_id", ForeignKey("patents.id", name='template_patent_patent_id_foreign'))
    ))
    groups = relationship("Group", secondary=Table("groups_patents", Base.metadata,
        Column("group_id", ForeignKey("groups.id", name='group_patent_group_id_foreign')),
        Column("patent_id", ForeignKey("patents.id", name='group_patent_patent_id_foreign'))
    ))
    properties = relationship("Property", secondary=Table("properties_patents", Base.metadata,
        Column("property_id", ForeignKey("properties.id", name='property_patent_property_id_foreign')),
        Column("patent_id", ForeignKey("patents.id", name='property_patent_patent_id_foreign'))
    ))

class Teacher(Base, DefaultFunctions):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey(Image.id, name='teachers_image_id_foreign'), nullable=True)
    description = Column(String, nullable=True)
    preview = Column(String, nullable=True)
    preview_image_id = Column(Integer, ForeignKey(Image.id, name='teachers_preview_image_id_foreign'), nullable=True)
    created_at = Column(DateTime, nullable=False)
    unpublished_at = Column(DateTime, nullable=True)
    tags = relationship("Tag", secondary=Table("tags_teachers", Base.metadata,
        Column("tag_id", ForeignKey("tags.id", name='tag_teacher_tag_id_foreign')),
        Column("teacher_id", ForeignKey("teachers.id", name='tag_teacher_teacher_id_foreign'))
    ))
    templates = relationship("Template", secondary=Table("templates_teachers", Base.metadata,
        Column("template_id", ForeignKey("templates.id", name='template_teacher_template_id_foreign')),
        Column("teacher_id", ForeignKey("teachers.id", name='template_teacher_teacher_id_foreign'))
    ))
    groups = relationship("Group", secondary=Table("groups_teachers", Base.metadata,
        Column("group_id", ForeignKey("groups.id", name='group_teacher_group_id_foreign')),
        Column("teacher_id", ForeignKey("teachers.id", name='group_teacher_teacher_id_foreign'))
    ))
    properties = relationship("Property", secondary=Table("properties_teachers", Base.metadata,
        Column("property_id", ForeignKey("properties.id", name='property_teacher_property_id_foreign')),
        Column("teacher_id", ForeignKey("teachers.id", name='property_teacher_teacher_id_foreign'))
    ))

class ComputerProgram(Base, DefaultFunctions):
    __tablename__ = 'computer_programs'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey(Image.id, name='computer_programs_image_id_foreign'), nullable=True)
    description = Column(String, nullable=True)
    preview = Column(String, nullable=True)
    preview_image_id = Column(Integer, ForeignKey(Image.id, name='computer_programs_preview_image_id_foreign'), nullable=True)
    created_at = Column(DateTime, nullable=False)
    unpublished_at = Column(DateTime, nullable=True)
    tags = relationship("Tag", secondary=Table("tags_computer_programs", Base.metadata,
        Column("tag_id", ForeignKey("tags.id", name='tag_computer_program_tag_id_foreign')),
        Column("computer_program_id", ForeignKey("computer_programs.id", name='tag_computer_program_computer_program_id_foreign'))
    ))
    templates = relationship("Template", secondary=Table("templates_computer_programs", Base.metadata,
        Column("template_id", ForeignKey("templates.id", name='template_computer_program_template_id_foreign')),
        Column("computer_program_id", ForeignKey("computer_programs.id", name='template_computer_program_computer_program_id_foreign'))
    ))
    groups = relationship("Group", secondary=Table("groups_computer_programs", Base.metadata,
        Column("group_id", ForeignKey("groups.id", name='group_computer_program_group_id_foreign')),
        Column("computer_program_id", ForeignKey("computer_programs.id", name='group_computer_program_computer_program_id_foreign'))
    ))
    properties = relationship("Property", secondary=Table("properties_computer_programs", Base.metadata,
        Column("property_id", ForeignKey("properties.id", name='property_computer_program_property_id_foreign')),
        Column("computer_program_id", ForeignKey("computer_programs.id", name='property_computer_program_computer_program_id_foreign'))
    ))

class Certificates(Base, DefaultFunctions):
    __tablename__ = 'certificates'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey(Image.id, name='certificates_image_id_foreign'), nullable=True)
    description = Column(String, nullable=True)
    preview = Column(String, nullable=True)
    preview_image_id = Column(Integer, ForeignKey(Image.id, name='certificates_preview_image_id_foreign'), nullable=True)
    created_at = Column(DateTime, nullable=False)
    unpublished_at = Column(DateTime, nullable=True)
    tags = relationship("Tag", secondary=Table("tags_certificates", Base.metadata,
        Column("tag_id", ForeignKey("tags.id", name='tag_certificate_tag_id_foreign')),
        Column("certificate_id", ForeignKey("certificates.id", name='tag_certificate_certificate_id_foreign'))
    ))
    templates = relationship("Template", secondary=Table("templates_certificates", Base.metadata,
        Column("template_id", ForeignKey("templates.id", name='template_certificate_template_id_foreign')),
        Column("certificate_id", ForeignKey("certificates.id", name='template_certificate_certificate_id_foreign'))
    ))
    groups = relationship("Group", secondary=Table("groups_certificates", Base.metadata,
        Column("group_id", ForeignKey("groups.id", name='group_certificate_group_id_foreign')),
        Column("certificate_id", ForeignKey("certificates.id", name='group_certificate_certificate_id_foreign'))
    ))
    properties = relationship("Property", secondary=Table("properties_certificates", Base.metadata,
        Column("property_id", ForeignKey("properties.id", name='property_certificate_property_id_foreign')),
        Column("certificate_id", ForeignKey("certificates.id", name='property_certificate_certificate_id_foreign'))
    ))

class Phonebook(Base, DefaultFunctions):
    __tablename__ = 'phonebook'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey(Image.id, name='phonebook_image_id_foreign'), nullable=True)
    description = Column(String, nullable=True)
    preview = Column(String, nullable=True)
    preview_image_id = Column(Integer, ForeignKey(Image.id, name='phonebook_preview_image_id_foreign'), nullable=True)
    created_at = Column(DateTime, nullable=False)
    unpublished_at = Column(DateTime, nullable=True)
    tags = relationship("Tag", secondary=Table("tags_phonebook", Base.metadata,
        Column("tag_id", ForeignKey("tags.id", name='tag_phonebook_tag_id_foreign')),
        Column("phonebook_id", ForeignKey("phonebook.id", name='tag_phonebook_phonebook_id_foreign'))
    ))
    templates = relationship("Template", secondary=Table("templates_phonebook", Base.metadata,
        Column("template_id", ForeignKey("templates.id", name='template_phonebook_template_id_foreign')),
        Column("phonebook_id", ForeignKey("phonebook.id", name='template_phonebook_phonebook_id_foreign'))
    ))
    groups = relationship("Group", secondary=Table("groups_phonebook", Base.metadata,
        Column("group_id", ForeignKey("groups.id", name='group_phonebook_group_id_foreign')),
        Column("phonebook_id", ForeignKey("phonebook.id", name='group_phonebook_phonebook_id_foreign'))
    ))
    properties = relationship("Property", secondary=Table("properties_phonebook", Base.metadata,
        Column("property_id", ForeignKey("properties.id", name='property_phonebook_property_id_foreign')),
        Column("phonebook_id", ForeignKey("phonebook.id", name='property_phonebook_phonebook_id_foreign'))
    ))

class Trademarks(Base, DefaultFunctions):
    __tablename__ = 'trademarks'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey(Image.id, name='trademarks_image_id_foreign'), nullable=True)
    description = Column(String, nullable=True)
    preview = Column(String, nullable=True)
    preview_image_id = Column(Integer, ForeignKey(Image.id, name='trademarks_preview_image_id_foreign'), nullable=True)
    created_at = Column(DateTime, nullable=False)
    unpublished_at = Column(DateTime, nullable=True)
    tags = relationship("Tag", secondary=Table("tags_trademarks", Base.metadata,
        Column("tag_id", ForeignKey("tags.id", name='tag_trademark_tag_id_foreign')),
        Column("trademark_id", ForeignKey("trademarks.id", name='tag_trademark_trademark_id_foreign'))
    ))
    templates = relationship("Template", secondary=Table("templates_trademarks", Base.metadata,
        Column("template_id", ForeignKey("templates.id", name='template_trademark_template_id_foreign')),
        Column("trademark_id", ForeignKey("trademarks.id", name='template_trademark_trademark_id_foreign'))
    ))
    groups = relationship("Group", secondary=Table("groups_trademarks", Base.metadata,
        Column("group_id", ForeignKey("groups.id", name='group_trademark_group_id_foreign')),
        Column("trademark_id", ForeignKey("trademarks.id", name='group_trademark_trademark_id_foreign'))
    ))
    properties = relationship("Property", secondary=Table("properties_trademarks", Base.metadata,
        Column("property_id", ForeignKey("properties.id", name='property_trademark_property_id_foreign')),
        Column("trademark_id", ForeignKey("trademarks.id", name='property_trademark_trademark_id_foreign'))
    ))

class Services(Base, DefaultFunctions):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey(Image.id, name='services_image_id_foreign'), nullable=True)
    description = Column(String, nullable=True)
    preview = Column(String, nullable=True)
    preview_image_id = Column(Integer, ForeignKey(Image.id, name='services_preview_image_id_foreign'), nullable=True)
    created_at = Column(DateTime, nullable=False)
    unpublished_at = Column(DateTime, nullable=True)
    tags = relationship("Tag", secondary=Table("tags_services", Base.metadata,
        Column("tag_id", ForeignKey("tags.id", name='tag_service_tag_id_foreign')),
        Column("service_id", ForeignKey("services.id", name='tag_service_service_id_foreign'))
    ))
    templates = relationship("Template", secondary=Table("templates_services", Base.metadata,
        Column("template_id", ForeignKey("templates.id", name='template_service_template_id_foreign')),
        Column("service_id", ForeignKey("services.id", name='template_service_service_id_foreign'))
    ))
    groups = relationship("Group", secondary=Table("groups_services", Base.metadata,
        Column("group_id", ForeignKey("groups.id", name='group_service_group_id_foreign')),
        Column("service_id", ForeignKey("services.id", name='group_service_service_id_foreign'))
    ))
    properties = relationship("Property", secondary=Table("properties_services", Base.metadata,
        Column("property_id", ForeignKey("properties.id", name='property_service_property_id_foreign')),
        Column("service_id", ForeignKey("services.id", name='property_service_service_id_foreign'))
    ))
