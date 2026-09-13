const authenticatedApi = require("../authenticated_api");

const lessonApi = {
  // =========================================
  // GET LESSONS
  // =========================================

  async getLessons(req, config = {}) {
    const response = await authenticatedApi.get(req, "/lessons/list/", config);

    return response.data;
  },

  // =========================================
  // CREATE LESSON
  // =========================================

  async createLesson(req, data, config = {}) {
    const response = await authenticatedApi.post(
      req,
      "/lessons/create/",
      data,
      config,
    );

    return response.data;
  },

  // =========================================
  // GET SEMESTER LESSON PLANS
  // =========================================

  async getSemesterLessonPlans(req, config = {}) {
    const response = await authenticatedApi.get(
      req,
      "/lessons/semester-plans/",
      config,
    );

    return response.data;
  },
  async createSemesterLessonPlans(req, data, config = {}) {
    const response = await authenticatedApi.post(
      req,
      "/lessons/semester-plans/create/",
      data,
      config,
    );

    return response.data;
  },
  // =========================================
  // GET SUBJECT LESSON PLANS
  // =========================================

  async getSubjectLessonPlans(req, config = {}) {
    const response = await authenticatedApi.get(
      req,
      "/lessons/subject-plans/",
      config,
    );

    return response.data;
  },
  async createSubjectLessonPlan(req, data, config = {}) {
    const response = await authenticatedApi.post(
      req,
      "/lessons/subject-plans/create/",
      data,
      config,
    );

    return response.data;
  },
  async getCourseLessonPlans(req, config = {}) {
    const response = await authenticatedApi.get(
      req,
      "/lessons/course-lesson-plans/",
      config,
    );

    return response.data;
  },
  async getClassSectionLessonPlans(req, courseLessonPlanId, config = {}) {
    const response = await authenticatedApi.get(
      req,
      `/lessons/course-lesson-plans/${courseLessonPlanId}/class-sections/`,
      config,
    );

    return response.data;
  },
  async ensureLessonPlans(req, config = {}) {
    const response = await authenticatedApi.post(
      req,
      "/lessons/lesson-plans/ensure/",
      {},
      config,
    );

    return response.data;
  },
  async ensureLessonOpenings(req, config = {}) {
    const response = await authenticatedApi.post(
      req,
      "/lesson-openings/ensure/",
      {},
      config,
    );

    return response.data;
  },

  async getLessonOpenings(req, classSectionLessonPlanId, config = {}) {
    const response = await authenticatedApi.get(
      req,
      `/lesson-openings/class-sections/${classSectionLessonPlanId}/`,
      config,
    );

    return response.data;
  },
};

module.exports = lessonApi;
