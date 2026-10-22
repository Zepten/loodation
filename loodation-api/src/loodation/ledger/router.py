from uuid import UUID

from fastapi import APIRouter, status

from loodation.auth.deps import UserServiceDep
from loodation.ledger.deps import LedgerServiceDep, TransactionPaginatorParamsDep
from loodation.ledger.schemas import (
    TransactionCreate,
    TransactionResponse,
    TransactionResponsePaginated,
    TransactionsByUserResponsePaginated,
    UserBalanceResponse,
)

router = APIRouter()


@router.post(
    "/transactions",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
    transaction_create: TransactionCreate,
    ledger_service: LedgerServiceDep,
    user_service: UserServiceDep,
) -> TransactionResponse:
    await user_service.ensure_user_exists(transaction_create.user_id)
    await ledger_service.ensure_user_has_enough_balance(
        user_id=transaction_create.user_id,
        bet_amount=transaction_create.amount,
        type_code=transaction_create.type_code,
    )
    transaction = await ledger_service.create_transaction(**transaction_create.model_dump())
    return TransactionResponse.model_validate(transaction)


@router.get("/transactions/{user_id}", response_model=TransactionsByUserResponsePaginated)
async def get_transactions_by_user_id(
    user_id: UUID,
    ledger_service: LedgerServiceDep,
    paginator: TransactionPaginatorParamsDep,
) -> TransactionsByUserResponsePaginated:
    result = await ledger_service.get_transactions_by_user_id(user_id, paginator)
    return TransactionsByUserResponsePaginated(
        user_id=user_id,
        transactions=TransactionResponsePaginated(
            total_count=result.total_count,
            items=tuple(TransactionResponse.model_validate(item) for item in result.items),
        ),
    )


@router.get("/balance", response_model=UserBalanceResponse)
async def get_user_balance(
    user_id: UUID,
    ledger_service: LedgerServiceDep,
    user_service: UserServiceDep,
) -> UserBalanceResponse:
    await user_service.ensure_user_exists(user_id)
    user_balance = await ledger_service.get_user_balance(user_id)
    return UserBalanceResponse(user_id=user_id, balance=user_balance)
