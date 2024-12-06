from typing import Callable, List, Union

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

from data_questionnaire_agent.toml_support import get_prompts


def factory_prompt(
    find_prompt: Callable, params: list[str], language: str = "en"
) -> ChatPromptTemplate:
    prompts = get_prompts(language)
    section = find_prompt(prompts)
    return prompt_factory_generic(section, params, prompts)


def prompt_factory_generic(
    section: dict,
    input_variables: List[str],
    prompts: object,
    prompt_transform: Union[Callable, None] = None,
) -> ChatPromptTemplate:
    human_message = section["human_message"]
    human_message = (
        prompt_transform(human_message)
        if prompt_transform is not None
        else human_message
    )
    prompt_msgs = [
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=section["system_message"], input_variables=[]
            )
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=human_message,
                input_variables=input_variables,
            )
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=prompts["general_messages"]["tip_correct_format"],
                input_variables=[],
            )
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=prompts["general_messages"]["tip_language"],
                input_variables=[],
            )
        ),
    ]
    return ChatPromptTemplate(messages=prompt_msgs)
