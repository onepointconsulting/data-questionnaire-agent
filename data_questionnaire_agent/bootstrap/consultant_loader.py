import asyncio

import click
from consultant_info_generator.consultant_info_tools import extract_consultant

from data_questionnaire_agent.bootstrap import db_cfg
from data_questionnaire_agent.service.persistence_service_consultants_async import (
    save_consultant,
)


@click.command()
@click.option(
    "--linkedin_id", "-lid", help="The linked in ID", multiple=True, required=True
)
def save_consultants(linkedin_id: list[str]):
    for id in linkedin_id:
        try:
            consultant = extract_consultant(id)
            asyncio.run(save_consultant(consultant))
        except Exception as e:
            click.echo(f"Failed to retrieve {id}", err=True)
            click.echo(f"Error message {e}", err=True)


if __name__ == "__main__":
    print(db_cfg.db_conn_str)
    save_consultants()
