from uuid import UUID

from fastapi import status

from loodation.core.exceptions import BusinessError
from loodation.ledger.enums import TransactionTypeCode
from loodation.money.schemas import Money


class TransactionNotFoundError(BusinessError):
    name: str = "transaction_not_found"
    status_code: int = status.HTTP_404_NOT_FOUND

    def __init__(self, transaction_id: UUID) -> None:
        super().__init__(message="Transaction not found.", extra={"transaction_id": transaction_id})


class IdempotencyKeyAlreadyUsedError(BusinessError):
    name: str = "idempotency_key_already_used"
    status_code: int = status.HTTP_409_CONFLICT

    def __init__(self, idempotency_key: UUID, existing_transaction_id: UUID) -> None:
        super().__init__(
            message="Idempotency key is already used by transaction.",
            extra={
                "idempotency_key": idempotency_key,
                "existing_transaction_id": existing_transaction_id,
            },
        )


class NotEnoughBalanceError(BusinessError):
    name: str = "not_enough_balance"
    status_code: int = status.HTTP_423_LOCKED

    def __init__(
        self,
        user_id: UUID,
        balance: Money,
        bet_amount: Money,
        transaction_type_code: TransactionTypeCode,
    ) -> None:
        super().__init__(
            message="User has not enough balance.",
            extra={
                "user_id": user_id,
                "balance": balance,
                "bet_amount": bet_amount,
                "transaction_type_code": transaction_type_code,
            },
        )
