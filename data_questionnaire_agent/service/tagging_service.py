from typing import List


#from langchain.chains.llm import LLMChain
from langchain.chains import LLMChain
#from langchain.chains import LLMChain
from langchain.chains import create_tagging_chain_pydantic
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.openai_schema import ResponseTags
from data_questionnaire_agent.toml_support import read_prompts_toml

prompts = read_prompts_toml()


def prompt_factory_sentiment() -> ChatPromptTemplate:
    section = prompts["tagging"]
    human_message = section["human_message"]
    human_message_extraction = section["human_message_extraction"]
    prompt_msgs = [
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=section["system_message"], input_variables=[]
            )
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=human_message,
                input_variables=["answer"],
            )
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=human_message_extraction,
                input_variables=["answer"],
            )
        ),
    ]
    return ChatPromptTemplate(messages=prompt_msgs)


def sentiment_chain_factory() -> LLMChain:
    return create_tagging_chain_pydantic(
        ResponseTags, cfg.llm, prompt_factory_sentiment(), verbose=cfg.verbose_llm
    )


chain = create_tagging_chain_pydantic(ResponseTags, cfg.llm, prompt_factory_sentiment())


def prepare_sentiment_input(question: str) -> dict:
    return {"answer": question}


def tag_response(response: str) -> dict:
    res = chain(prepare_sentiment_input(response))
    return res


if __name__ == "__main__":

    def process_answer(answer: str):
        logger.info(type(answer))
        logger.info(answer)

    # Does your organization support an event driven architecture for data integration?
    process_answer(tag_response("Yes, it does"))
    process_answer(
        tag_response(
            "Yes, I know that CDC is good to prevent data from being outdated."
        )
    )
    process_answer(
        tag_response("Well, since you are asking, I am not quite sure about it.")
    )
    # Does your organization take more than 3 weeks for data integration between 2 systems?
    process_answer(
        tag_response(
            "Well, that depends on the size of the project. But in most cases yes."
        )
    )
    process_answer(tag_response("Almost we never finish integrations before that."))
    process_answer(
        tag_response(
            "Which is the meaning of dark data? What is CDC (Change Data Capture)?"
        )
    )
