import jinja2

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.service.persistence_service_consultants_async import read_consultants
from consultant_info_generator.model import Consultant


def convert_to_markdown(
    consultants: list[Consultant], language: str = "en"
) -> str:
    context = {
        "consultants": consultants,
    }
    template_loader = jinja2.FileSystemLoader(cfg.template_location)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("consultants-template.md")
    return template.render(context)


async def convert_all_consultants() -> str:
    consultants = await read_consultants()
    return convert_to_markdown(consultants)