const {
  getLessonOpeningsUseCase,
  updateLessonOpeningStatusUseCase,
} = require("../../../../infrastructure/dependencies/lesson/lesson_dependency");

const {
  getTeacherActivePlannedClassSectionsUseCase,
} = require("../../../../infrastructure/dependencies/class_section/class_section_dependency");

const {
  getActivePlannedSemestersUseCase,
} = require("../../../../infrastructure/dependencies/semester/semester_dependency");
const {
  getAssignmentUseCase,
  applyAssignmentUseCase,
  getAssignmentApplicationsUseCase,
  updateAssignmentApplicationClassSectionStatusUseCase,
} = require("../../../../infrastructure/dependencies/assignment/assignment_dependency");
function createClassSectionLessonPlanId(classSectionId) {
  if (!classSectionId) {
    return null;
  }

  return `CSLP-${classSectionId}`;
}
function normalizeAssignment(assignment) {
  if (!assignment) {
    return null;
  }

  return {
    assignmentId:
      assignment.assignmentId ??
      assignment.assignment_id ??
      assignment.id ??
      "",

    title: assignment.title ?? assignment.name ?? "",

    subjectId: assignment.subjectId ?? assignment.subject_id ?? "",

    subjectName: assignment.subjectName ?? assignment.subject_name ?? "",
  };
}

class LessonOpeningController {
  async getLessonOpenings(req, res) {
    const { classSectionId } = req.params;

    const classSectionLessonPlanId =
      createClassSectionLessonPlanId(classSectionId);

    try {
      const lessonOpenings = await getLessonOpeningsUseCase.execute(
        req,
        classSectionId,
      );

      return res.render("teacher/assignment/lesson", {
        lessonOpenings,
        classSectionId,
        classSectionLessonPlanId,
        success: true,
      });
    } catch (error) {
      console.error("[NODE] GET LESSON OPENINGS ERROR:", error);

      console.error("[NODE] ERROR MESSAGE:", error.message);

      console.error("[NODE] ERROR RESPONSE:", error.response?.data);

      console.error("[NODE] ERROR STATUS:", error.response?.status);

      return res
        .status(error.response?.status || 400)
        .render("teacher/assignment/lesson", {
          lessonOpenings: [],
          classSectionId,
          classSectionLessonPlanId,
          success: false,
          error:
            error.response?.data?.message ||
            error.message ||
            "Không thể tải danh sách buổi học.",
        });
    }
  }

  async updateLessonOpeningStatus(req, res) {
    try {
      const { classSectionLessonPlanId, lessonId } = req.params;

      const status = String(req.body?.status || "").trim();

      if (!classSectionLessonPlanId) {
        return res.status(400).json({
          success: false,
          message: "Class section lesson plan ID không được để trống.",
        });
      }

      if (!lessonId) {
        return res.status(400).json({
          success: false,
          message: "Lesson ID không được để trống.",
        });
      }

      if (!status) {
        return res.status(400).json({
          success: false,
          message: "Trạng thái buổi học không được để trống.",
        });
      }

      const result = await updateLessonOpeningStatusUseCase.execute(req, {
        classSectionLessonPlanId,
        lessonId,
        status,
      });

      return res.status(200).json({
        success: true,
        message: "Cập nhật trạng thái buổi học thành công.",
        data: result?.data ?? result,
      });
    } catch (error) {
      console.error("[NODE] UPDATE LESSON OPENING STATUS ERROR:", error);

      console.error("[NODE] ERROR RESPONSE:", error.response?.data);

      console.error("[NODE] ERROR STATUS:", error.response?.status);

      return res.status(error.response?.status || 400).json({
        success: false,
        message:
          error.response?.data?.message ||
          error.message ||
          "Không thể cập nhật trạng thái buổi học.",
      });
    }
  }
  async showLessonOpeningApplicationPage(req, res) {
    const assignmentId = String(req.params.assignment_id || "").trim();

    if (!assignmentId) {
      return res
        .status(400)
        .render("teacher/assignment/lesson_opening_application", {
          academicYears: [],
          semesters: [],
          assignmentId: "",
          assignmentTitle: "",
          subjectId: "",
          subjectName: "",
          success: false,
          error: "Thiếu mã bài tập.",
        });
    }

    try {
      const assignmentResult = await getAssignmentUseCase.execute(
        req,
        assignmentId,
      );

      const assignment = normalizeAssignment(
        assignmentResult?.data ?? assignmentResult,
      );

      if (!assignment) {
        return res
          .status(404)
          .render("teacher/assignment/lesson_opening_application", {
            academicYears: [],
            semesters: [],
            assignmentId,
            assignmentTitle: "",
            subjectId: "",
            subjectName: "",
            success: false,
            error: "Không tìm thấy bài tập.",
          });
      }

      if (!assignment.subjectId) {
        return res
          .status(400)
          .render("teacher/assignment/lesson_opening_application", {
            academicYears: [],
            semesters: [],
            assignmentId,
            assignmentTitle: assignment.title,
            subjectId: "",
            subjectName: assignment.subjectName,
            academicYears: [],
            semesters: [],
            success: false,
            error: "Bài tập chưa có môn học.",
          });
      }

      const semesters = await getActivePlannedSemestersUseCase.execute(req);

      const normalizedSemesters = (semesters || []).map((semester) => ({
        semesterId: semester.semesterId ?? semester.semester_id,

        name: semester.name ?? semester.semesterName ?? semester.semester_name,

        semesterNumber: semester.semesterNumber ?? semester.semester_number,

        academicYearId: semester.academicYearId ?? semester.academic_year_id,

        academicYearName:
          semester.academicYearName ?? semester.academic_year_name,

        startDate: semester.startDate ?? semester.start_date,

        endDate: semester.endDate ?? semester.end_date,

        status: semester.status,
      }));

      const academicYears = [
        ...new Map(
          normalizedSemesters
            .filter((semester) => semester.academicYearId)
            .map((semester) => [
              semester.academicYearId,
              {
                academicYearId: semester.academicYearId,

                academicYearName: semester.academicYearName,
              },
            ]),
        ).values(),
      ];

      return res.render("teacher/assignment/lesson_opening_application", {
        assignmentId: assignment.assignmentId || assignmentId,

        assignmentTitle: assignment.title,

        subjectId: assignment.subjectId,

        subjectName: assignment.subjectName,

        academicYears,
        semesters: normalizedSemesters,

        success: true,
      });
    } catch (error) {
      console.error("[NODE] GET LESSON OPENING PAGE ERROR:", error);

      return res
        .status(error.response?.status || 400)
        .render("teacher/assignment/lesson_opening_application", {
          assignmentId,
          assignmentTitle: "",
          subjectId: "",
          subjectName: "",
          academicYears: [],
          semesters: [],
          success: false,
          error:
            error.response?.data?.message ||
            error.message ||
            "Không thể tải trang mở buổi học.",
        });
    }
  }

  async getClassSections(req, res) {
    try {
      const { academic_year_id, semester_id, subject_id } = req.query;

      if (!academic_year_id || !semester_id || !subject_id) {
        return res.status(400).json({
          success: false,
          message: "Thiếu năm học, học kỳ hoặc môn học.",
        });
      }

      const classSections =
        await getTeacherActivePlannedClassSectionsUseCase.execute(req, {
          academicYearId: academic_year_id,

          semesterId: semester_id,

          subjectId: subject_id,
        });

      return res.status(200).json({
        success: true,
        data: classSections,
      });
    } catch (error) {
      console.error("[NODE] GET LESSON OPENING CLASS SECTIONS ERROR:", error);

      return res.status(error.response?.status || 500).json({
        success: false,
        message:
          error.response?.data?.message ||
          error.message ||
          "Không thể tải danh sách nhóm lớp học phần.",
      });
    }
  }

  async getLessonOpeningsBySelection(req, res) {
    try {
      const { academic_year_id, semester_id, subject_id } = req.query;

      if (!academic_year_id || !semester_id || !subject_id) {
        return res.status(400).json({
          success: false,
          message: "Thiếu năm học, học kỳ hoặc môn học.",
        });
      }

      const classSections =
        await getTeacherActivePlannedClassSectionsUseCase.execute(req, {
          academicYearId: academic_year_id,

          semesterId: semester_id,

          subjectId: subject_id,
        });

      if (!Array.isArray(classSections) || classSections.length === 0) {
        return res.status(200).json({
          success: true,
          data: [],
        });
      }

      const firstClassSection = classSections[0];

      const classSectionId =
        firstClassSection.class_section_id ?? firstClassSection.classSectionId;

      if (!classSectionId) {
        return res.status(500).json({
          success: false,
          message: "Dữ liệu lớp học phần không chứa class_section_id.",
        });
      }

      const lessonOpenings = await getLessonOpeningsUseCase.execute(
        req,
        classSectionId,
      );

      return res.status(200).json({
        success: true,
        data: lessonOpenings,
      });
    } catch (error) {
      console.error("[NODE] GET LESSON OPENINGS BY SELECTION ERROR:", error);

      return res.status(error.response?.status || 500).json({
        success: false,
        message:
          error.response?.data?.message ||
          error.message ||
          "Không thể tải danh sách buổi học.",
      });
    }
  }
  async applyAssignment(req, res) {
    try {
      const result = await applyAssignmentUseCase.execute(req, {
        assignmentId: req.body.assignment_id,
        lessonId: req.body.lesson_id,
        classSectionIds: req.body.class_section_ids,
        maxAttempts: req.body.max_attempts ?? 1,
      });

      return res.status(200).json({
        success: true,
        message: "Áp dụng bài tập cho buổi học thành công.",
        data: result,
      });
    } catch (error) {
      console.error("APPLY ASSIGNMENT ERROR:", error);

      return res.status(400).json({
        success: false,
        message: error.message || "Không thể áp dụng bài tập.",
      });
    }
  }
  async getAssignmentApplications(req, res) {
    try {
      const { class_section_id, lesson_id } = req.query;

      const applications = await getAssignmentApplicationsUseCase.execute(req, {
        classSectionId: class_section_id,
        lessonId: lesson_id,
      });

      return res.status(200).json({
        success: true,

        data: applications,
      });
    } catch (error) {
      console.error("GET ASSIGNMENT APPLICATIONS ERROR:", error);

      return res.status(400).json({
        success: false,

        message: error.message || "Không thể tải bài tập của buổi học.",
      });
    }
  }
  async updateAssignmentApplicationClassSectionStatus(req, res) {
    try {
      const { applicationId, classSectionId } = req.params;

      const { status } = req.body;

      const data =
        await updateAssignmentApplicationClassSectionStatusUseCase.execute(
          req,
          {
            assignmentApplicationId: applicationId,

            classSectionId,

            status,
          },
        );

      return res.status(200).json({
        success: true,
        data,
      });
    } catch (error) {
      console.error(
        "UPDATE ASSIGNMENT APPLICATION CLASS SECTION STATUS ERROR:",
        error,
      );

      return res.status(400).json({
        success: false,
        message: error.message || "Không thể cập nhật trạng thái bài tập.",
      });
    }
  }
}

module.exports = new LessonOpeningController();
