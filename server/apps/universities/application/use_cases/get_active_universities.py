class GetActiveUniversitiesUseCase:

    def __init__(self, university_repository):
        self.university_repository = university_repository

    def execute(self):
        return self.university_repository.get_active()