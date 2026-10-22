from enum import StrEnum


class UserSortFields(StrEnum):
    ID = "id"
    USERNAME = "username"
    ACTIVE = "active"
    LAST_LOGIN_AT = "last_login_at"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
