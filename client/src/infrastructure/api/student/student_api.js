const authenticatedApi = require("../authenticated_api");
const FormData = require("form-data");
const fs = require("fs");

const studentApi = {
  async getUniversityStudents(req, config = {}) {
    const response = await authenticatedApi.get(req, "/students/list/", config);

    return response.data;
  },
  async importStudents(req, file) {
    const formData = new FormData();

    formData.append("file", fs.createReadStream(file.path), {
      filename: file.originalname,
      contentType: file.mimetype,
    });

    const response = await authenticatedApi.post(
      req,
      "/students/import/",
      formData,
      {
        headers: formData.getHeaders(),
        maxBodyLength: Infinity,
        maxContentLength: Infinity,
      },
    );

    return response.data;
  },
};

module.exports = studentApi;
