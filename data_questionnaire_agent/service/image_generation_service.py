
from langchain.utilities.dalle_image_generator import DallEAPIWrapper

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from data_questionnaire_agent.config import cfg

from data_questionnaire_agent.model.openai_schema import ConditionalAdvice


def image_chain_factory() -> LLMChain:
    prompt = PromptTemplate(
        input_variables=["image_desc"],
        template="Generate a detailed prompt to generate an image based on the following description: {image_desc}",
    )
    return LLMChain(llm=cfg.image_llm, prompt=prompt)


def generate_image(chain: LLMChain, description: str) -> str:
    return DallEAPIWrapper().run(chain.run(description))


def generate_advice_image(chain: LLMChain, advice: ConditionalAdvice) -> str:
    image_description = f"Please generate an image with speech ballons with the text of these advices: {advice}"
    return generate_image(chain, image_description)


if __name__ == "__main__":
    from data_questionnaire_agent.test.provider.advice_provider import create_advice_2
    chain = image_chain_factory()
    image_url = generate_advice_image(chain, create_advice_2())
    print(image_url)
