const {
  createAssignmentUseCase,
  getAssignmentsUseCase,
  getAssignmentsBySubjectUseCase,
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
    return res.render("teacher/assignment/index", { title: "Bà tập" });
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
  
}

module.exports = new AssignmentController();
