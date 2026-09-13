from apps.subjects.domain.repositories.subject_repository import (
    SubjectRepository,
)

from apps.subjects.domain.entities.subject_entity import (
    Subject,
)

from apps.subjects.infrastructure.persistence.models.subject_model import (
    SubjectModel,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)


class MongoSubjectRepository(SubjectRepository):

    def get_by_university(
        self,
        university_id: str,
    ):
        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return []

        subjects = SubjectModel.objects(
            university=university,
        ).order_by("name")

        result = []

        for subject in subjects:

            department = subject.department

            result.append(
                Subject(
                    subject_id=subject.subject_id,
                    name=subject.name,
                    university_id=university.university_id,
                    university_name=university.name,
                    department_id=department.department_id,
                    department_name=department.name,
                    subject_types=subject.subject_types,
                    credits=subject.credits,
                    process_percent=subject.process_percent,
                    midterm_percent=subject.midterm_percent,
                    final_percent=subject.final_percent,
                    status=subject.status,
                )
            )

        return result

    def exists_by_id(
        self,
        subject_id: str,
    ):

        return (
            SubjectModel.objects(
                subject_id=subject_id,
            ).first()
            is not None
        )

    def create(
        self,
        subject,
        university,
        department,
    ):

        subject_model = SubjectModel(
            subject_id=subject.subject_id,
            name=subject.name,
            university=university,
            department=department,
            subject_types=subject.subject_types,
            credits=subject.credits,
            process_percent=subject.process_percent,
            midterm_percent=subject.midterm_percent,
            final_percent=subject.final_percent,
            status=subject.status,
        )

        subject_model.save()

        return Subject(
            subject_id=subject_model.subject_id,
            name=subject_model.name,
            university_id=university.university_id,
            university_name=university.name,
            department_id=department.department_id,
            department_name=department.name,
            subject_types=subject_model.subject_types,
            credits=subject_model.credits,
            process_percent=subject_model.process_percent,
            midterm_percent=subject_model.midterm_percent,
            final_percent=subject_model.final_percent,
            status=subject_model.status,
        )

    def get_by_name(
        self,
        name: str,
        university_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return None

        return SubjectModel.objects(
            name=name,
            university=university,
        ).first()

    def get_by_id(
        self,
        university_id: str,
        subject_id: str,
    ):
        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return None

        model = SubjectModel.objects(
            subject_id=subject_id,
            university=university,
        ).first()

        if not model:
            return None

        department = model.department

        return Subject(
            subject_id=model.subject_id,
            name=model.name,
            university_id=university.university_id,
            university_name=university.name,
            department_id=department.department_id,
            department_name=department.name,
            subject_types=model.subject_types,
            credits=model.credits,
            process_percent=model.process_percent,
            midterm_percent=model.midterm_percent,
            final_percent=model.final_percent,
            status=model.status,
        )
