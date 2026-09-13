from mongoengine import (
    Document,
    StringField,
    IntField,
    DateField,
    ReferenceField,
)
from apps.academic_years.infrastructure.persistence.models.academic_year_model import AcademicYearModel
from apps.semesters.infrastructure.persistence.models.semester_model import SemesterModel
from apps.teachers.infrastructure.persistence.models.teacher_model import TeacherModel
from apps.subjects.infrastructure.persistence.models.subject_model import SubjectModel

class ClassSectionModel(Document):

    meta = {
        "collection": "class_sections",
        "indexes": [
            {
                "fields": [
                    "subject",
                    "group_number",
                    "semester",
                    "academic_year",
                ],
                "unique": True,
            },
            "teacher",
            "semester",
            "academic_year",
            "start_date",
            "end_date",
            "status",
        ],
    }

    class_section_id = StringField(
        required=True,
        max_length=30,
    )

    subject = ReferenceField(
        SubjectModel,
        required=True,
    )

    group_number = IntField(
        required=True,
        min_value=1,
    )

    teacher = ReferenceField(
        TeacherModel,
        required=True,
    )

    semester = ReferenceField(
        SemesterModel,
        required=True,
    )

    academic_year = ReferenceField(
        AcademicYearModel,
        required=True,
    )

    start_date = DateField(
        required=True,
    )

    end_date = DateField(
        required=True,
    )

    status = StringField(
        required=True,
        choices=[
            "planned",
            "active",
            "locked",
        ],
        default="planned",
    )