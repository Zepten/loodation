from uuid import UUID

from loguru import logger
from sqlalchemy import case, func, select

from loodation.core.paginator.schemas import PaginatedResult, PaginatorParams
from loodation.core.service import BaseService
from loodation.ledger.enums import TransactionSortFields, TransactionStatusCode, TransactionTypeCode
from loodation.ledger.exceptions import IdempotencyKeyAlreadyUsedError, NotEnoughBalanceError
from loodation.ledger.models import Transaction
from loodation.money.schemas import Money


class LedgerService(BaseService):
    async def create_transaction(
        self,
        user_id: UUID,
        amount_cents: int,
        type_code: TransactionTypeCode,
        idempotency_key: UUID,
        reference_id: UUID,
    ) -> Transaction:
        existing_transaction_id = await self.session.scalar(
            select(Transaction.id).where(Transaction.idempotency_key == idempotency_key)
        )
        if existing_transaction_id:
            raise IdempotencyKeyAlreadyUsedError(idempotency_key, existing_transaction_id)

        transaction = Transaction(
            user_id=user_id,
            reference_id=reference_id,
            idempotency_key=idempotency_key,
            amount_cents=amount_cents,
            type_code=type_code,
            status_code=TransactionStatusCode.COMPLETED,
        )

        self.session.add(transaction)
        await self.session.flush()
        await self.session.refresh(transaction)

        logger.info(f"Created transaction {transaction}.")
        return transaction

    async def get_transactions_by_user_id(
        self, user_id: UUID, paginator: PaginatorParams[TransactionSortFields]
    ) -> PaginatedResult[Transaction]:
        transactions_by_user_id_stmt = select(Transaction).where(Transaction.user_id == user_id)
        return await self.paginator.paginate(Transaction, transactions_by_user_id_stmt, paginator)

    async def get_user_balance(self, user_id: UUID) -> Money:
        user_balance_cents = await self.session.scalar(
            select(
                func.sum(
                    case(
                        (
                            Transaction.type_code == TransactionTypeCode.WIN,
                            Transaction.amount_cents,
                        ),
                        else_=-Transaction.amount_cents,
                    )
                )
            ).where(
                Transaction.user_id == user_id,
                Transaction.status_code == TransactionStatusCode.COMPLETED,
            )
        )
        return Money(cents=user_balance_cents) if user_balance_cents else Money(cents=0)

    async def ensure_user_has_enough_balance(
        self, user_id: UUID, bet_amount: Money, type_code: TransactionTypeCode
    ) -> None:
        if type_code == TransactionTypeCode.BET:
            user_balance = await self.get_user_balance(user_id)
            if user_balance.cents < bet_amount.cents:
                raise NotEnoughBalanceError(
                    user_id=user_id,
                    balance=user_balance,
                    bet_amount=bet_amount,
                    transaction_type_code=type_code,
                )
