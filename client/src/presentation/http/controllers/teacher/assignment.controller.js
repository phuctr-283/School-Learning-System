const {
  createAssignmentUseCase,
  getAssignmentsUseCase,
} = require(
  "../../../../infrastructure/dependencies/assignment/assignment_dependency",
);


class AssignmentController {
  async create(req, res) {
    try {
      const result =
        await createAssignmentUseCase.execute(
          req,
          req.body,
        );

      return res.status(201).json({
        success: true,
        data: result,
      });
    } catch (error) {
      console.error(
        "CREATE ASSIGNMENT ERROR:",
        error.response?.data || error.message,
      );

      return res.status(
        error.response?.status || 500,
      ).json({
        success: false,
        message:
          error.response?.data?.detail ||
          error.response?.data?.message ||
          "Không thể tạo bài tập",
      });
    }
  }

  async getList(req, res) {
    try {
      const assignments =
        await getAssignmentsUseCase.execute(
          req,
          req.query,
        );

      return res.status(200).json({
        success: true,
        data: assignments,
      });
    } catch (error) {
      console.error(
        "GET ASSIGNMENTS ERROR:",
        error.response?.data || error.message,
      );

      return res.status(
        error.response?.status || 500,
      ).json({
        success: false,
        message:
          error.response?.data?.detail ||
          error.response?.data?.message ||
          "Không thể tải danh sách bài tập",
      });
    }
  }
}


module.exports = new AssignmentController();