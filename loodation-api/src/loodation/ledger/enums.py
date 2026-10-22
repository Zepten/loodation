from enum import StrEnum


class TransactionTypeCode(StrEnum):
    BET = "bet"
    WIN = "win"
    BONUS = "bonus"
    ADMIN = "admin"


class TransactionStatusCode(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class TransactionSortFields(StrEnum):
    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    TYPE_CODE = "type_code"
    STATUS_CODE = "status_code"
    USER_ID = "user_id"
    AMOUNT_CENTS = "amount_cents"
