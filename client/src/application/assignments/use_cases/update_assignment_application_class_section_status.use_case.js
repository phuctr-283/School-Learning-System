class UpdateAssignmentApplicationClassSectionStatusUseCase {
  constructor(assignmentApplicationRepository) {
    this.assignmentApplicationRepository = assignmentApplicationRepository;
  }

  async execute(req, { assignmentApplicationId, classSectionId, status }) {
    if (!assignmentApplicationId) {
      throw new Error("Thiếu mã application.");
    }

    if (!classSectionId) {
      throw new Error("Thiếu mã lớp học phần.");
    }

    if (!["active", "closed"].includes(status)) {
      throw new Error("Trạng thái phải là active hoặc closed.");
    }

    return this.assignmentApplicationRepository.updateClassSectionStatus(
      req,
      assignmentApplicationId,
      classSectionId,
      status,
    );
  }
}

module.exports = UpdateAssignmentApplicationClassSectionStatusUseCase;
