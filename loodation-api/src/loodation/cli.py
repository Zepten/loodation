import asyncio
import json as _json

import rich_click as click
from alembic.config import Config
from rich.pretty import pprint
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from alembic import command as alembic_command
from loodation.auth.models import User  # noqa
from loodation.auth.service import UserService
from loodation.core.config import Environment, settings
from loodation.core.database import db_session_factory
from loodation.core.paginator.service import PaginatorService
from loodation.ledger.models import Transaction  # noqa

alembic_config = Config("alembic.ini")


@click.group()
def cli() -> None:
    """
    Command line interface for Loodation API.
    """


@cli.group()
def api() -> None:
    """
    🛠️ Loodation API management commands.
    """


@api.command()
@click.option("--json", is_flag=True, help="Get Loodation API config in JSON.")
def config(json: bool) -> None:
    """
    🛠️ View Loodation API configuration in JSON.
    """
    if json:
        click.echo(
            _json.dumps(
                settings.model_dump(mode="json"),
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        pprint(settings.model_dump())


@api.command()
def shell() -> None:
    """
    🐚 Interactive IPython shell for Loodation API.
    """


def get_paginator_service(session: AsyncSession) -> PaginatorService:
    return PaginatorService(session)


def get_user_service(session: AsyncSession) -> UserService:
    return UserService(session, get_paginator_service(session))


@api.command()
@click.option("--username", "-u", required=True, help="User's username")
def create_admin(username: str) -> None:
    """
    👤  Create an administrator user.
    """

    async def create_admin_async(username: str) -> None:
        async with db_session_factory() as session:
            user_service = get_user_service(session)

            await user_service.create_user(username)
            await session.commit()

    asyncio.run(create_admin_async(username))


@cli.group()
def db() -> None:
    """
    🏗️  Database management commands.
    """


@db.command()
@click.option("--message", "-m", required=True, help="String message to apply to the revision.")
def generate(message: str) -> None:
    """
    🏗️  Generate new database migration.
    """

    alembic_command.revision(alembic_config, message=message, autogenerate=True)


@db.command()
def upgrade() -> None:
    """
    🚀  Apply all pending database migrations via Alembic.
    """

    alembic_command.upgrade(alembic_config, "head")


@db.command()
def downgrade() -> None:
    """
    ❌  Revert the last database migration via Alembic.
    """

    click.confirm("⚠️  Are you sure you want to downgrade database?", abort=True)

    alembic_command.downgrade(alembic_config, "-1")


if settings.environment == Environment.DEV:

    @db.command()
    def reset() -> None:
        """
        💥  [DEV] Drop and recreate tables by reverting and reapplying all migrations via Alembic.
        """

        click.confirm(
            "⚠️  This action will wipe all data and create empty tables. Continue?", abort=True
        )

        alembic_command.downgrade(alembic_config, "base")
        alembic_command.upgrade(alembic_config, "head")

    @db.command()
    def nuke() -> None:
        """
        💥  [DEV] Drop database schema and recreates schema.
        """

        click.confirm("⚠️  This action will DROP SCHEMA and wipe all data. Continue?", abort=True)

        async def drop_schema() -> None:
            async with db_session_factory() as session:
                await session.execute(text("DROP SCHEMA public CASCADE"))
                await session.execute(text("CREATE SCHEMA public"))
                await session.commit()

        asyncio.run(drop_schema())


if __name__ == "__main__":
    cli()
