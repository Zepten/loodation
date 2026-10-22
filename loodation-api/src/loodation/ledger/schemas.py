from datetime import datetime
from typing import TypeAlias
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from loodation.core.paginator.schemas import PaginatedResponse
from loodation.ledger.enums import TransactionStatusCode, TransactionTypeCode
from loodation.money.schemas import Money


class TransactionCreate(BaseModel):
    user_id: UUID
    reference_id: UUID
    amount: Money
    idempotency_key: UUID
    type_code: TransactionTypeCode


class TransactionResponse(TransactionCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    created_at: datetime
    status_code: TransactionStatusCode


TransactionResponsePaginated: TypeAlias = PaginatedResponse[TransactionResponse]


class TransactionsByUserResponsePaginated(BaseModel):
    user_id: UUID
    transactions: TransactionResponsePaginated


class UserBalanceResponse(BaseModel):
    user_id: UUID
    balance: Money
