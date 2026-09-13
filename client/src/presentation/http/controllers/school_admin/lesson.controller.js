const {
  getLessonsUseCase,
  createLessonUseCase,
  getSemesterLessonPlansUseCase,
  createSemesterLessonPlansUseCase,
  getSubjectLessonPlansUseCase,
  createSubjectLessonPlanUseCase,
  getClassSectionLessonPlansUseCase,
  getCourseLessonPlansUseCase,
  ensureLessonPlansUseCase,
} = require("../../../../infrastructure/dependencies/lesson/lesson_dependency");
const {
  getActivePlannedSemestersUseCase,
} = require("../../../../infrastructure/dependencies/semester/semester_dependency");
class LessonController {
  // =========================================
  // LESSON PLAN PAGE
  // =========================================

  async getLessonPlanPage(req, res) {
    try {
      const [
        lessons,
        semesterLessonPlans,
        subjectLessonPlans,
        courseLessonPlans,
      ] = await Promise.all([
        getLessonsUseCase.execute(req),
        getSemesterLessonPlansUseCase.execute(req),
        getSubjectLessonPlansUseCase.execute(req),
        getCourseLessonPlansUseCase.execute(req),
      ]);
      console.log(subjectLessonPlans);
      return res.render("school_admin/university/lesson/list", {
        title: "Kế hoạch giảng dạy",
        lessons,
        semesterLessonPlans,
        subjectLessonPlans,
        courseLessonPlans,
      });
    } catch (error) {
      console.error("GET LESSON PLAN PAGE ERROR:", error);
      return res.render("school_admin/university/lesson/list", {
        title: "Kế hoạch giảng dạy",
        lessons: [],
        semesterLessonPlans: [],
        subjectLessonPlans: [],
        courseLessonPlans: {},
        error: "Không thể tải dữ liệu kế hoạch giảng dạy.",
      });
    }
  }
  async getClassSectionLessonPlans(req, res) {
    try {
      const { courseLessonPlanId } = req.params;

      const classSectionLessonPlans = await getClassSectionLessonPlansUseCase.execute(
        req,
        courseLessonPlanId,
      );

      return res.render(
        "school_admin/university/lesson/list_class_section_lesson_plans",
        {
          title: "Chi tiết kế hoạch nhóm lớp học phần",
          classSectionLessonPlans,
        },
      );
    } catch (error) {
      console.error("GET CLASS SECTION LESSON PLANS PAGE ERROR:", error);

      return res
        .status(500)
        .render("school_admin/university/lesson/list_class_section_lesson_plans", {
          title: "Chi tiết kế hoạch nhóm lớp học phần",
          classSectionLessonPlans: [],
          error: error.message,
        });
    }
  }
  async ensureLessonPlans(req, res, next) {
    console.log("ensureLessonPlansUseCase:", ensureLessonPlansUseCase);

    try {
      const result = await ensureLessonPlansUseCase.execute(req);

      return res.redirect("/school-admin/university/lessons");
    } catch (error) {
      console.error("ENSURE LESSON PLANS ERROR:", error);

      next(error);
    }
  }
  async createLessonPage(req, res) {
    return res.render("school_admin/university/lesson/create_lesson", {
      title: "Tạo mới buổi chung",
    });
  }
  async createLesson(req, res) {
    try {
      const data = {
        create_mode: req.body.create_mode,

        lesson_number: req.body.lesson_number
          ? Number(req.body.lesson_number)
          : undefined,

        lesson_number_start: req.body.lesson_number_start
          ? Number(req.body.lesson_number_start)
          : undefined,

        lesson_number_end: req.body.lesson_number_end
          ? Number(req.body.lesson_number_end)
          : undefined,
      };

      await createLessonUseCase.execute(req, data);

      return res.redirect("/school-admin/university/lessons");
    } catch (error) {
      console.error("CREATE LESSON ERROR:", error);

      return res.render("school_admin/university/lesson/create_lesson", {
        title: "Tạo buổi học",
        error: error.response?.data?.message || "Không thể tạo buổi học.",
        formData: req.body,
      });
    }
  }
  async createSemesterLessonPlanPage(req, res) {
    try {
      const semesters = await getActivePlannedSemestersUseCase.execute(req);

      // Chỉ lấy mỗi academicYearId một lần
      const academicYears = [
        ...new Map(
          semesters.map((semester) => [
            semester.academicYearId,
            {
              academicYearId: semester.academicYearId,
              academicYearName: semester.academicYearName,
            },
          ]),
        ).values(),
      ];

      return res.render(
        "school_admin/university/lesson/create_semester_lesson_plan",
        {
          title: "Tạo kế hoạch học kỳ",

          // Toàn bộ SemesterContentDTO
          semesters,

          // Academic year duy nhất
          academicYears,

          formData: {},
        },
      );
    } catch (error) {
      console.error("GET CREATE SEMESTER PAGE ERROR:", error);

      return res
        .status(500)
        .render("school_admin/university/lesson/create_semester_lesson_plan", {
          title: "Tạo kế hoạch học kỳ",
          semesters: [],
          academicYears: [],
          formData: {},
          error:
            error.response?.data?.message ||
            error.message ||
            "Không thể tải danh sách học kỳ.",
        });
    }
  }
  async createSemesterLessonPlan(req, res) {
    try {
      console.log(req.body);
      await createSemesterLessonPlansUseCase.execute(req, req.body);

      return res.redirect("/school-admin/university/lessons");
    } catch (error) {
      console.error("CREATE SEMESTER LESSON PLANS ERROR:", error);

      let semesters = [];
      let academicYears = [];

      try {
        semesters = await getActivePlannedSemestersUseCase.execute(req);

        academicYears = [
          ...new Map(
            semesters.map((semester) => [
              semester.academicYearId,
              {
                academicYearId: semester.academicYearId,

                academicYearName: semester.academicYearName,
              },
            ]),
          ).values(),
        ];
      } catch (loadError) {
        console.error("RELOAD SEMESTERS ERROR:", loadError);
      }

      return res
        .status(400)
        .render("school_admin/university/lesson/create_semester_lesson_plan", {
          title: "Tạo kế hoạch học kỳ",

          semesters,

          academicYears,

          error:
            error.response?.data?.message ||
            error.message ||
            "Không thể tạo kế hoạch học kỳ.",

          formData: req.body,
        });
    }
  }
  async createSubjectLessonPlanPage(req, res) {
    return res.render(
      "school_admin/university/lesson/create_subject_lesson_plan",
      {
        title: "Tạo kế hoạch môn học",
      },
    );
  }
  async createSubjectLessonPlan(req, res) {
    try {
      console.log("REQ BODY:", JSON.stringify(req.body, null, 2));

      await createSubjectLessonPlanUseCase.execute(req, req.body);

      return res.redirect("/school-admin/university/lessons");
    } catch (error) {
      console.error("CREATE SUBJECT LESSON PLAN ERROR:", error);

      return res.render(
        "school_admin/university/lesson/create_subject_lesson_plan",
        {
          title: "Tạo quy tắc kế hoạch môn học",
          error: error.message,
          selectedSemesterNumber: req.body.semester_number,
          formData: req.body,
        },
      );
    }
  }
}

module.exports = new LessonController();
