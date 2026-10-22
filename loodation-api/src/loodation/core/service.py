from loodation.core.database import DbSessionDep
from loodation.core.paginator.deps import PaginatorServiceDep


class BaseService:
    def __init__(self, session: DbSessionDep, paginator: PaginatorServiceDep) -> None:
        self.session = session
        self.paginator = paginator
