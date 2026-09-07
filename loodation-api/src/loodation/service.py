import logging

from loodation.database import DbSessionDep
from loodation.paginator import PaginatorServiceDep

logger = logging.getLogger(__name__)


class BaseService:
    def __init__(self, session: DbSessionDep, paginator: PaginatorServiceDep) -> None:
        self.session = session
        self.paginator = paginator
