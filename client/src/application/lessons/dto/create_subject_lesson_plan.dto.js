class CreateSubjectLessonPlanRuleDTO {
  constructor(data = {}) {
    this.lessonType = data.lessonType;

    this.minCredits = data.minCredits ?? null;

    this.maxCredits = data.maxCredits ?? null;

    this.totalLessons = data.totalLessons;
  }

  toJSON() {
    return {
      lesson_type: this.lessonType,

      min_credits: this.minCredits,

      max_credits: this.maxCredits,

      total_lessons: this.totalLessons,
    };
  }
}

class CreateSubjectLessonPlanDTO {
  constructor(data = {}) {
    this.semesterNumber = data.semesterNumber;

    this.rules = (data.rules || []).map((rule) =>
      rule instanceof CreateSubjectLessonPlanRuleDTO
        ? rule
        : new CreateSubjectLessonPlanRuleDTO(rule),
    );
  }

  static fromRequestBody(body = {}) {
    const rules = [];

    const source = body.rules || {};

    for (const lessonType of ["theory", "practice"]) {
      const typeRules = source[lessonType] || {};

      const items = Array.isArray(typeRules)
        ? typeRules
        : Object.values(typeRules);

      for (const rule of items) {
        rules.push(
          new CreateSubjectLessonPlanRuleDTO({
            lessonType,

            minCredits:
              rule.min_credits !== undefined && rule.min_credits !== ""
                ? Number(rule.min_credits)
                : null,

            maxCredits:
              rule.max_credits !== undefined && rule.max_credits !== ""
                ? Number(rule.max_credits)
                : null,

            totalLessons:
              rule.total_lessons !== undefined && rule.total_lessons !== ""
                ? Number(rule.total_lessons)
                : null,
          }),
        );
      }
    }

    return new CreateSubjectLessonPlanDTO({
      semesterNumber: body.semester_number,

      rules,
    });
  }

  toJSON() {
    return {
      semester_number: this.semesterNumber,

      rules: this.rules.map((rule) => rule.toJSON()),
    };
  }
}

module.exports = CreateSubjectLessonPlanDTO;
