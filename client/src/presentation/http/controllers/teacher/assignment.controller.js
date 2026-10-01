const {
  createAssignmentUseCase,
  getAssignmentsUseCase,
  getAssignmentsBySubjectUseCase,
  getAssignmentByIdUseCase,
  getStudentAssignmentAttemptsUseCase,
  updateAssignmentUseCase,
} = require("../../../../infrastructure/dependencies/assignment/assignment_dependency");

const {
  getTeacherSubjectsUseCase,
} = require("../../../../infrastructure/dependencies/class_section/class_section_dependency");
const clean = (value) => String(value ?? "").trim();

const getRequestSubjectId = (req) => {
  const bodySubjectId = clean(req.body?.subject_id);

  const querySubjectId = clean(req.query?.subject_id);

  return bodySubjectId || querySubjectId;
};

const normalizeSubjects = (subjects) => {
  return (subjects || [])
    .map((subject) => ({
      subject_id: clean(subject.subjectId ?? subject.subject_id),

      subject_name: clean(subject.subjectName ?? subject.subject_name),
    }))
    .filter((subject) => subject.subject_id !== "");
};

class AssignmentController {
  async getIndex(req, res) {
    return res.render("teacher/assignment/index", { title: "Bài tập" });
  }

  async showAssignmentList(req, res) {
    try {
      const assignments = await getAssignmentsUseCase.execute(req);

      const subjects = await getTeacherSubjectsUseCase.execute(req);
      console.log(assignments);
      return res.render("teacher/assignment/list", {
        title: "Danh sách bài tập",
        assignments,
        subjects: normalizeSubjects(subjects),
        selectedSubjectId: null,
        selectedSubjectName: "Bài tập chung",
        error: null,
      });
    } catch (error) {
      console.error("GET ASSIGNMENTS ERROR:", error);

      return res.status(500).render("teacher/assignment/list", {
        title: "Danh sách bài tập",
        assignments: [],
        subjects: [],
        selectedSubjectId: null,
        selectedSubjectName: "Bài tập chung",
        error: "Không thể tải danh sách bài tập.",
      });
    }
  }
  async showAssignmentsBySubject(req, res) {
    const subjectId = String(req.params.subjectId || "").trim();

    try {
      const assignments = await getAssignmentsBySubjectUseCase.execute(
        req,
        subjectId,
      );

      const subjects = await getTeacherSubjectsUseCase.execute(req);

      const normalizedSubjects = normalizeSubjects(subjects);

      const selectedSubject = normalizedSubjects.find((subject) => {
        return subject.subject_id === subjectId;
      });

      return res.render("teacher/assignment/list", {
        title: "Danh sách bài tập",

        assignments,

        subjects: normalizedSubjects,

        selectedSubjectId: subjectId,

        selectedSubjectName:
          selectedSubject?.subject_name || "Bài tập theo môn học",

        error: null,
      });
    } catch (error) {
      console.error("GET ASSIGNMENTS BY SUBJECT PAGE ERROR:", error);

      return res.status(500).render("teacher/assignment/list", {
        title: "Danh sách bài tập",

        assignments: [],

        subjects: [],

        selectedSubjectId: subjectId,

        selectedSubjectName: "Bài tập theo môn học",

        error: "Không thể tải bài tập của môn học.",
      });
    }
  }

  async renderCreateAssignmentPage(req, res, options = {}) {
    const formData = options.formData || {};

    const subjectId = clean(formData.subject_id ?? getRequestSubjectId(req));

    const normalizedFormData = {
      title: clean(formData.title),
      description:
        typeof formData.description === "string" ? formData.description : "",
      subject_id: subjectId,
      assignment_type: clean(formData.assignment_type) || "practice",
      duration_minutes: formData.duration_minutes || 30,
      questions: Array.isArray(formData.questions) ? formData.questions : [],
    };

    let subjects = [];

    try {
      subjects = await getTeacherSubjectsUseCase.execute(req);
    } catch (error) {
      console.error("GET SUBJECTS FOR ASSIGNMENT ERROR:", error);
    }
    const normalizedSubjects = normalizeSubjects(subjects);
    return res
      .status(options.statusCode || 200)
      .render("teacher/assignment/create", {
        title: "Tạo bài tập",
        subjects: normalizedSubjects,
        formData: normalizedFormData,
        hasSelectedSubject: Boolean(normalizedFormData.subject_id),
        error: options.error || null,
      });
  }

  async createAssignmentPage(req, res) {
    return this.renderCreateAssignmentPage(req, res);
  }

  async createAssignment(req, res) {
    const subjectId = getRequestSubjectId(req);

    let questions = [];

    try {
      const rawQuestions = req.body?.questions;

      if (typeof rawQuestions === "string") {
        const value = rawQuestions.trim();

        questions = value ? JSON.parse(value) : [];
      } else if (Array.isArray(rawQuestions)) {
        questions = rawQuestions;
      }

      if (!Array.isArray(questions)) {
        throw new Error("Danh sách câu hỏi không hợp lệ.");
      }
    } catch (error) {
      console.error("PARSE ASSIGNMENT QUESTIONS ERROR:", error);
      return this.renderCreateAssignmentPage(req, res, {
        statusCode: 400,

        formData: {
          ...req.body,
          subject_id: subjectId,
          questions: [],
        },
        error: "Dữ liệu câu hỏi không hợp lệ.",
      });
    }

    const formData = {
      ...req.body,
      subject_id: subjectId,
      questions,
    };

    try {
      await createAssignmentUseCase.execute(req, formData);
      return res.redirect("/teacher/assignment/list");
    } catch (error) {
      console.error("CREATE ASSIGNMENT ERROR:", error);
      return this.renderCreateAssignmentPage(req, res, {
        statusCode: 400,
        formData,
        error: error.message || "Không thể tạo bài tập.",
      });
    }
  }
  async showUpdatePage(req, res) {
    const assignmentId = String(req.params.assignmentId ?? "").trim();

    if (!assignmentId) {
      return res.redirect("/teacher/assignment/list");
    }

    try {
      const assignment = await getAssignmentByIdUseCase.execute(
        req,
        assignmentId,
      );

      const subjects = await getTeacherSubjectsUseCase.execute(req);

      console.log("GET ASSIGNMENT BY ID:", JSON.stringify(assignment, null, 2));

      // =========================================================
      // NORMALIZE QUESTIONS
      // =========================================================

      let questions = assignment?.questions;

      // Trường hợp backend trả JSON string
      if (typeof questions === "string") {
        try {
          questions = JSON.parse(questions);
        } catch (error) {
          console.error("PARSE ASSIGNMENT QUESTIONS ERROR:", error);

          questions = [];
        }
      }

      // Nếu backend không trả array
      if (!Array.isArray(questions)) {
        questions = [];
      }

      // =========================================================
      // NORMALIZE QUESTION DATA
      // =========================================================

      questions = questions.map((question) => ({
        question_type: question?.question_type ?? question?.questionType ?? "",

        question: question?.question ?? "",

        content: question?.content ?? "",

        answer: question?.answer ?? "",

        score: question?.score ?? "",
      }));

      console.log("UPDATE FORM QUESTIONS:", JSON.stringify(questions, null, 2));

      const formData = {
        assignment_id: assignment?.assignment_id ?? assignmentId,
        title: assignment?.title ?? "",
        description: assignment?.description ?? "",
        subject_id: assignment?.subject_id ?? "",
        assignment_type: assignment?.assignment_type ?? "practice",
        duration_minutes: assignment?.duration_minutes ?? 30,
        questions,
      };
      console.log("UPDATE FORM DATA:", JSON.stringify(formData, null, 2));
      return res.status(200).render("teacher/assignment/update", {
        pageTitle: "Chỉnh sửa bài tập",
        isEdit: true,
        assignment,
        formData,
        subjects,
        hasSelectedSubject: Boolean(formData.subject_id),
        error: null,
      });
    } catch (error) {
      console.error("SHOW UPDATE ASSIGNMENT PAGE ERROR:", error);

      return res
        .status(error.response?.status ?? 400)
        .render("teacher/assignment/update", {
          pageTitle: "Chỉnh sửa bài tập",
          isEdit: true,
          assignment: null,
          formData: {
            assignment_id: assignmentId,
            title: "",
            description: "",
            subject_id: "",
            assignment_type: "practice",
            duration_minutes: 30,
            questions: [],
          },
          subjects: [],
          hasSelectedSubject: false,
          error: error.message || "Không thể tải bài tập.",
        });
    }
  }
  async updateAssignment(req, res) {
    const assignmentId = String(req.params.assignmentId ?? "").trim();
    let questions = [];
    try {
      if (!assignmentId) {
        throw new Error("Thiếu mã bài tập.");
      }
      questions = req.body.questions;
      if (typeof questions === "string") {
        try {
          questions = JSON.parse(questions);
        } catch (parseError) {
          console.error("PARSE QUESTIONS ERROR:", parseError);
          throw new Error("Dữ liệu câu hỏi không hợp lệ.");
        }
      }

      if (!Array.isArray(questions)) {
        questions = [];
      }
      console.log("========== UPDATE ASSIGNMENT ==========");
      console.log("ASSIGNMENT ID:", assignmentId);
      console.log("REQUEST BODY:", req.body);
      console.log("QUESTIONS:", JSON.stringify(questions, null, 2));

      const input = {
        assignment_id: assignmentId,

        title: req.body.title,

        description: req.body.description,

        subject_id: req.body.subject_id,

        assignment_type: req.body.assignment_type,

        duration_minutes: req.body.duration_minutes,

        questions,
      };
      const result = await updateAssignmentUseCase.execute(req, input);

      console.log("UPDATE ASSIGNMENT SUCCESS:", result);

      return res.redirect("/teacher/assignment/list");
    } catch (error) {
      console.error("UPDATE ASSIGNMENT PAGE ERROR:", error);
      try {
        const assignment = await getAssignmentByIdUseCase.execute(
          req,
          assignmentId,
        );
        const subjects = await getTeacherSubjectsUseCase.execute(req);
        return res
          .status(error.response?.status ?? 400)
          .render("teacher/assignment/update", {
            pageTitle: "Chỉnh sửa bài tập",
            isEdit: true,
            assignment,
            formData: {
              assignment_id: assignmentId,
              title: req.body.title ?? assignment.title ?? "",
              description: req.body.description ?? assignment.description ?? "",
              subject_id: req.body.subject_id ?? assignment.subject_id ?? "",
              assignment_type:
                req.body.assignment_type ??
                assignment.assignment_type ??
                "practice",
              duration_minutes:
                req.body.duration_minutes ?? assignment.duration_minutes ?? 30,
              questions,
            },
            subjects,
            hasSelectedSubject: Boolean(
              req.body.subject_id ?? assignment.subject_id,
            ),
            error: error.message || "Không thể cập nhật bài tập.",
          });
      } catch (renderError) {
        console.error("RENDER UPDATE ERROR:", renderError);
        return res.status(400).render("teacher/assignment/update", {
          pageTitle: "Chỉnh sửa bài tập",
          isEdit: true,
          assignment: null,
          formData: {
            assignment_id: assignmentId,
            title: req.body.title ?? "",
            description: req.body.description ?? "",
            subject_id: req.body.subject_id ?? "",
            assignment_type: req.body.assignment_type ?? "practice",
            duration_minutes: req.body.duration_minutes ?? 30,
            questions,
          },
          subjects: [],
          hasSelectedSubject: Boolean(req.body.subject_id),
          error: error.message || "Không thể cập nhật bài tập.",
        });
      }
    }
  }
  async showStudentAttemptsPage(req, res) {
    const assignmentApplicationId = String(
      req.params.assignmentApplicationId ?? "",
    ).trim();

    const classSectionId = String(req.query.class_section_id ?? "").trim();

    const lessonId = String(req.query.lesson_id ?? "").trim();
    if (!assignmentApplicationId || !classSectionId || !lessonId) {
      return res.redirect(
        `/teacher/history/class-sections/${encodeURIComponent(classSectionId)}`,
      );
    }
    try {
      const data = await getStudentAssignmentAttemptsUseCase.execute(req, {
        assignmentApplicationId,
        classSectionId,
        lessonId,
      });

      return res.status(200).render("teacher/history/list_student", {
        pageTitle: "Sinh viên làm bài",

        assignmentApplicationId,

        classSectionId,

        lessonId,

        students: data.students || [],

        totalStudents: data.students?.length || 0,

        completedStudents:
          data.students?.filter(
            (item) => item.status === "submitted" || item.status === "graded",
          ).length || 0,

        inProgressStudents:
          data.students?.filter((item) => item.status === "in_progress")
            .length || 0,

        notStartedStudents:
          data.students?.filter((item) => item.status === "not_started")
            .length || 0,

        error: null,
      });
    } catch (error) {
      console.error("SHOW STUDENT ATTEMPTS PAGE ERROR:", error);

      return res
        .status(error.response?.status || 400)
        .render("teacher/history/list_student", {
          pageTitle: "Sinh viên làm bài",

          assignmentApplicationId,

          classSectionId,

          lessonId,

          students: [],

          totalStudents: 0,

          completedStudents: 0,

          inProgressStudents: 0,

          notStartedStudents: 0,

          error: error.message || "Không thể tải danh sách sinh viên.",
        });
    }
  }
}

module.exports = new AssignmentController();
