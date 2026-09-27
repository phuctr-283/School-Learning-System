class AssignmentApiError(Exception):

    status_code = 400

    def __init__(
        self,
        message,
        status_code=None,
    ):
        super().__init__(message)

        if status_code is not None:
            self.status_code = status_code


class AssignmentBadRequestError(AssignmentApiError):
    status_code = 400


class AssignmentForbiddenError(AssignmentApiError):
    status_code = 403


class AssignmentNotFoundError(AssignmentApiError):
    status_code = 404


class AssignmentLockedError(AssignmentApiError):
    status_code = 409
