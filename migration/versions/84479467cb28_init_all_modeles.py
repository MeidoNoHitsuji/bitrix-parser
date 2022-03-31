"""init all modeles

Revision ID: 84479467cb28
Revises: 93d92f6cc092
Create Date: 2022-03-17 15:31:32.460236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84479467cb28'
down_revision = '93d92f6cc092'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('preview', sa.String(), nullable=True),
    sa.Column('preview_image_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], name='activities_image_id_foreign'),
    sa.ForeignKeyConstraint(['preview_image_id'], ['images.id'], name='activities_preview_image_id_foreign'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('catalog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('preview', sa.String(), nullable=True),
    sa.Column('preview_image_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], name='catalog_image_id_foreign'),
    sa.ForeignKeyConstraint(['preview_image_id'], ['images.id'], name='catalog_preview_image_id_foreign'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('certificates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('preview', sa.String(), nullable=True),
    sa.Column('preview_image_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], name='certificates_image_id_foreign'),
    sa.ForeignKeyConstraint(['preview_image_id'], ['images.id'], name='certificates_preview_image_id_foreign'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('computer_programs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('preview', sa.String(), nullable=True),
    sa.Column('preview_image_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], name='computer_programs_image_id_foreign'),
    sa.ForeignKeyConstraint(['preview_image_id'], ['images.id'], name='computer_programs_preview_image_id_foreign'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('equipments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('preview', sa.String(), nullable=True),
    sa.Column('preview_image_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], name='equipments_image_id_foreign'),
    sa.ForeignKeyConstraint(['preview_image_id'], ['images.id'], name='equipments_preview_image_id_foreign'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('faq',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('preview', sa.String(), nullable=True),
    sa.Column('preview_image_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], name='faq_image_id_foreign'),
    sa.ForeignKeyConstraint(['preview_image_id'], ['images.id'], name='faq_preview_image_id_foreign'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('laboratories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('preview', sa.String(), nullable=True),
    sa.Column('preview_image_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], name='laboratories_image_id_foreign'),
    sa.ForeignKeyConstraint(['preview_image_id'], ['images.id'], name='laboratories_preview_image_id_foreign'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('library_news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('preview', sa.String(), nullable=True),
    sa.Column('preview_image_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], name='library_news_image_id_foreign'),
    sa.ForeignKeyConstraint(['preview_image_id'], ['images.id'], name='library_news_preview_image_id_foreign'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('preview', sa.String(), nullable=True),
    sa.Column('preview_image_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], name='patents_image_id_foreign'),
    sa.ForeignKeyConstraint(['preview_image_id'], ['images.id'], name='patents_preview_image_id_foreign'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('phonebook',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('preview', sa.String(), nullable=True),
    sa.Column('preview_image_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], name='phonebook_image_id_foreign'),
    sa.ForeignKeyConstraint(['preview_image_id'], ['images.id'], name='phonebook_preview_image_id_foreign'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profkom_news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('preview', sa.String(), nullable=True),
    sa.Column('preview_image_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], name='profkom_news_image_id_foreign'),
    sa.ForeignKeyConstraint(['preview_image_id'], ['images.id'], name='profkom_news_preview_image_id_foreign'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('preview', sa.String(), nullable=True),
    sa.Column('preview_image_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], name='services_image_id_foreign'),
    sa.ForeignKeyConstraint(['preview_image_id'], ['images.id'], name='services_preview_image_id_foreign'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teachers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('preview', sa.String(), nullable=True),
    sa.Column('preview_image_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], name='teachers_image_id_foreign'),
    sa.ForeignKeyConstraint(['preview_image_id'], ['images.id'], name='teachers_preview_image_id_foreign'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trademarks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('preview', sa.String(), nullable=True),
    sa.Column('preview_image_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], name='trademarks_image_id_foreign'),
    sa.ForeignKeyConstraint(['preview_image_id'], ['images.id'], name='trademarks_preview_image_id_foreign'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('groups_activities',
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('activity_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], name='group_activity_activity_id_foreign'),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='group_activity_group_id_foreign')
    )
    op.create_table('groups_catalog',
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('catalog_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['catalog_id'], ['catalog.id'], name='group_catalog_catalog_id_foreign'),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='group_catalog_group_id_foreign')
    )
    op.create_table('groups_certificates',
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('certificate_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['certificate_id'], ['certificates.id'], name='group_certificate_certificate_id_foreign'),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='group_certificate_group_id_foreign')
    )
    op.create_table('groups_computer_programs',
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('computer_program_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['computer_program_id'], ['computer_programs.id'], name='group_computer_program_computer_program_id_foreign'),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='group_computer_program_group_id_foreign')
    )
    op.create_table('groups_equipments',
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('equipment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['equipment_id'], ['equipments.id'], name='group_equipment_equipment_id_foreign'),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='group_equipment_group_id_foreign')
    )
    op.create_table('groups_faq',
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('faq_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['faq_id'], ['faq.id'], name='group_faq_faq_id_foreign'),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='group_faq_group_id_foreign')
    )
    op.create_table('groups_laboratories',
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('laboratory_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='group_laboratory_group_id_foreign'),
    sa.ForeignKeyConstraint(['laboratory_id'], ['laboratories.id'], name='group_laboratory_laboratory_id_foreign')
    )
    op.create_table('groups_library_news',
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('library_new_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='group_library_new_group_id_foreign'),
    sa.ForeignKeyConstraint(['library_new_id'], ['library_news.id'], name='group_library_new_library_new_id_foreign')
    )
    op.create_table('groups_patents',
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('patent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='group_patent_group_id_foreign'),
    sa.ForeignKeyConstraint(['patent_id'], ['patents.id'], name='group_patent_patent_id_foreign')
    )
    op.create_table('groups_phonebook',
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('phonebook_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='group_phonebook_group_id_foreign'),
    sa.ForeignKeyConstraint(['phonebook_id'], ['phonebook.id'], name='group_phonebook_phonebook_id_foreign')
    )
    op.create_table('groups_profkom_news',
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('profkom_new_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='group_profkom_new_group_id_foreign'),
    sa.ForeignKeyConstraint(['profkom_new_id'], ['profkom_news.id'], name='group_profkom_new_profkom_new_id_foreign')
    )
    op.create_table('groups_services',
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('service_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='group_service_group_id_foreign'),
    sa.ForeignKeyConstraint(['service_id'], ['services.id'], name='group_service_service_id_foreign')
    )
    op.create_table('groups_teachers',
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='group_teacher_group_id_foreign'),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], name='group_teacher_teacher_id_foreign')
    )
    op.create_table('groups_trademarks',
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('trademark_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], name='group_trademark_group_id_foreign'),
    sa.ForeignKeyConstraint(['trademark_id'], ['trademarks.id'], name='group_trademark_trademark_id_foreign')
    )
    op.create_table('properties_activities',
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('activity_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], name='property_activity_activity_id_foreign'),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='property_activity_property_id_foreign')
    )
    op.create_table('properties_catalog',
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('catalog_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['catalog_id'], ['catalog.id'], name='property_catalog_catalog_id_foreign'),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='property_catalog_property_id_foreign')
    )
    op.create_table('properties_certificates',
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('certificate_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['certificate_id'], ['certificates.id'], name='property_certificate_certificate_id_foreign'),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='property_certificate_property_id_foreign')
    )
    op.create_table('properties_computer_programs',
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('computer_program_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['computer_program_id'], ['computer_programs.id'], name='property_computer_program_computer_program_id_foreign'),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='property_computer_program_property_id_foreign')
    )
    op.create_table('properties_equipments',
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('equipment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['equipment_id'], ['equipments.id'], name='property_equipment_equipment_id_foreign'),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='property_equipment_property_id_foreign')
    )
    op.create_table('properties_faq',
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('faq_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['faq_id'], ['faq.id'], name='property_faq_faq_id_foreign'),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='property_faq_property_id_foreign')
    )
    op.create_table('properties_laboratories',
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('laboratory_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['laboratory_id'], ['laboratories.id'], name='property_laboratory_laboratory_id_foreign'),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='property_laboratory_property_id_foreign')
    )
    op.create_table('properties_library_news',
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('library_new_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['library_new_id'], ['library_news.id'], name='property_library_new_library_new_id_foreign'),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='property_library_new_property_id_foreign')
    )
    op.create_table('properties_patents',
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('patent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['patent_id'], ['patents.id'], name='property_patent_patent_id_foreign'),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='property_patent_property_id_foreign')
    )
    op.create_table('properties_phonebook',
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('phonebook_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['phonebook_id'], ['phonebook.id'], name='property_phonebook_phonebook_id_foreign'),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='property_phonebook_property_id_foreign')
    )
    op.create_table('properties_profkom_news',
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('profkom_new_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['profkom_new_id'], ['profkom_news.id'], name='property_profkom_new_profkom_new_id_foreign'),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='property_profkom_new_property_id_foreign')
    )
    op.create_table('properties_services',
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('service_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='property_service_property_id_foreign'),
    sa.ForeignKeyConstraint(['service_id'], ['services.id'], name='property_service_service_id_foreign')
    )
    op.create_table('properties_teachers',
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='property_teacher_property_id_foreign'),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], name='property_teacher_teacher_id_foreign')
    )
    op.create_table('properties_trademarks',
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('trademark_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='property_trademark_property_id_foreign'),
    sa.ForeignKeyConstraint(['trademark_id'], ['trademarks.id'], name='property_trademark_trademark_id_foreign')
    )
    op.create_table('tags_activities',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('activity_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], name='tag_activity_activity_id_foreign'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='tag_activity_tag_id_foreign')
    )
    op.create_table('tags_catalog',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('catalog_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['catalog_id'], ['catalog.id'], name='tag_catalog_catalog_id_foreign'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='tag_catalog_tag_id_foreign')
    )
    op.create_table('tags_certificates',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('certificate_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['certificate_id'], ['certificates.id'], name='tag_certificate_certificate_id_foreign'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='tag_certificate_tag_id_foreign')
    )
    op.create_table('tags_computer_programs',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('computer_program_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['computer_program_id'], ['computer_programs.id'], name='tag_computer_program_computer_program_id_foreign'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='tag_computer_program_tag_id_foreign')
    )
    op.create_table('tags_equipments',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('equipment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['equipment_id'], ['equipments.id'], name='tag_equipment_equipment_id_foreign'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='tag_equipment_tag_id_foreign')
    )
    op.create_table('tags_faq',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('faq_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['faq_id'], ['faq.id'], name='tag_faq_faq_id_foreign'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='tag_faq_tag_id_foreign')
    )
    op.create_table('tags_laboratories',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('laboratory_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['laboratory_id'], ['laboratories.id'], name='tag_laboratory_laboratory_id_foreign'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='tag_laboratory_tag_id_foreign')
    )
    op.create_table('tags_library_news',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('library_new_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['library_new_id'], ['library_news.id'], name='tag_library_new_library_new_id_foreign'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='tag_library_new_tag_id_foreign')
    )
    op.create_table('tags_patents',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('patent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['patent_id'], ['patents.id'], name='tag_patent_patent_id_foreign'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='tag_patent_tag_id_foreign')
    )
    op.create_table('tags_phonebook',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('phonebook_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['phonebook_id'], ['phonebook.id'], name='tag_phonebook_phonebook_id_foreign'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='tag_phonebook_tag_id_foreign')
    )
    op.create_table('tags_profkom_news',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('profkom_new_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['profkom_new_id'], ['profkom_news.id'], name='tag_profkom_new_profkom_new_id_foreign'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='tag_profkom_new_tag_id_foreign')
    )
    op.create_table('tags_services',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('service_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['service_id'], ['services.id'], name='tag_service_service_id_foreign'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='tag_service_tag_id_foreign')
    )
    op.create_table('tags_teachers',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='tag_teacher_tag_id_foreign'),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], name='tag_teacher_teacher_id_foreign')
    )
    op.create_table('tags_trademarks',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('trademark_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='tag_trademark_tag_id_foreign'),
    sa.ForeignKeyConstraint(['trademark_id'], ['trademarks.id'], name='tag_trademark_trademark_id_foreign')
    )
    op.create_table('templates_activities',
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('activity_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], name='template_activity_activity_id_foreign'),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], name='template_activity_template_id_foreign')
    )
    op.create_table('templates_catalog',
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('catalog_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['catalog_id'], ['catalog.id'], name='template_catalog_catalog_id_foreign'),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], name='template_catalog_template_id_foreign')
    )
    op.create_table('templates_certificates',
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('certificate_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['certificate_id'], ['certificates.id'], name='template_certificate_certificate_id_foreign'),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], name='template_certificate_template_id_foreign')
    )
    op.create_table('templates_computer_programs',
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('computer_program_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['computer_program_id'], ['computer_programs.id'], name='template_computer_program_computer_program_id_foreign'),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], name='template_computer_program_template_id_foreign')
    )
    op.create_table('templates_equipments',
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('equipment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['equipment_id'], ['equipments.id'], name='template_equipment_equipment_id_foreign'),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], name='template_equipment_template_id_foreign')
    )
    op.create_table('templates_faq',
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('faq_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['faq_id'], ['faq.id'], name='template_faq_faq_id_foreign'),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], name='template_faq_template_id_foreign')
    )
    op.create_table('templates_laboratories',
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('laboratory_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['laboratory_id'], ['laboratories.id'], name='template_laboratory_laboratory_id_foreign'),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], name='template_laboratory_template_id_foreign')
    )
    op.create_table('templates_library_news',
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('library_new_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['library_new_id'], ['library_news.id'], name='template_library_new_library_new_id_foreign'),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], name='template_library_new_template_id_foreign')
    )
    op.create_table('templates_patents',
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('patent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['patent_id'], ['patents.id'], name='template_patent_patent_id_foreign'),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], name='template_patent_template_id_foreign')
    )
    op.create_table('templates_phonebook',
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('phonebook_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['phonebook_id'], ['phonebook.id'], name='template_phonebook_phonebook_id_foreign'),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], name='template_phonebook_template_id_foreign')
    )
    op.create_table('templates_profkom_news',
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('profkom_new_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['profkom_new_id'], ['profkom_news.id'], name='template_profkom_new_profkom_new_id_foreign'),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], name='template_profkom_new_template_id_foreign')
    )
    op.create_table('templates_services',
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('service_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['service_id'], ['services.id'], name='template_service_service_id_foreign'),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], name='template_service_template_id_foreign')
    )
    op.create_table('templates_teachers',
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], name='template_teacher_teacher_id_foreign'),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], name='template_teacher_template_id_foreign')
    )
    op.create_table('templates_trademarks',
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('trademark_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], name='template_trademark_template_id_foreign'),
    sa.ForeignKeyConstraint(['trademark_id'], ['trademarks.id'], name='template_trademark_trademark_id_foreign')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('templates_trademarks')
    op.drop_table('templates_teachers')
    op.drop_table('templates_services')
    op.drop_table('templates_profkom_news')
    op.drop_table('templates_phonebook')
    op.drop_table('templates_patents')
    op.drop_table('templates_library_news')
    op.drop_table('templates_laboratories')
    op.drop_table('templates_faq')
    op.drop_table('templates_equipments')
    op.drop_table('templates_computer_programs')
    op.drop_table('templates_certificates')
    op.drop_table('templates_catalog')
    op.drop_table('templates_activities')
    op.drop_table('tags_trademarks')
    op.drop_table('tags_teachers')
    op.drop_table('tags_services')
    op.drop_table('tags_profkom_news')
    op.drop_table('tags_phonebook')
    op.drop_table('tags_patents')
    op.drop_table('tags_library_news')
    op.drop_table('tags_laboratories')
    op.drop_table('tags_faq')
    op.drop_table('tags_equipments')
    op.drop_table('tags_computer_programs')
    op.drop_table('tags_certificates')
    op.drop_table('tags_catalog')
    op.drop_table('tags_activities')
    op.drop_table('properties_trademarks')
    op.drop_table('properties_teachers')
    op.drop_table('properties_services')
    op.drop_table('properties_profkom_news')
    op.drop_table('properties_phonebook')
    op.drop_table('properties_patents')
    op.drop_table('properties_library_news')
    op.drop_table('properties_laboratories')
    op.drop_table('properties_faq')
    op.drop_table('properties_equipments')
    op.drop_table('properties_computer_programs')
    op.drop_table('properties_certificates')
    op.drop_table('properties_catalog')
    op.drop_table('properties_activities')
    op.drop_table('groups_trademarks')
    op.drop_table('groups_teachers')
    op.drop_table('groups_services')
    op.drop_table('groups_profkom_news')
    op.drop_table('groups_phonebook')
    op.drop_table('groups_patents')
    op.drop_table('groups_library_news')
    op.drop_table('groups_laboratories')
    op.drop_table('groups_faq')
    op.drop_table('groups_equipments')
    op.drop_table('groups_computer_programs')
    op.drop_table('groups_certificates')
    op.drop_table('groups_catalog')
    op.drop_table('groups_activities')
    op.drop_table('trademarks')
    op.drop_table('teachers')
    op.drop_table('services')
    op.drop_table('profkom_news')
    op.drop_table('phonebook')
    op.drop_table('patents')
    op.drop_table('library_news')
    op.drop_table('laboratories')
    op.drop_table('faq')
    op.drop_table('equipments')
    op.drop_table('computer_programs')
    op.drop_table('certificates')
    op.drop_table('catalog')
    op.drop_table('activities')
    # ### end Alembic commands ###