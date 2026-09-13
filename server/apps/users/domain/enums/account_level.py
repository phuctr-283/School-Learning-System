from enum import IntEnum


class AccountLevel(IntEnum):

    SUPER_ADMIN = 1

    SCHOOL_ADMIN = 2

    TEACHER = 3

    STUDENT = 4