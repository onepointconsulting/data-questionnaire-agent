#####################################################
#### WARNING: this part of the code is not used #####
#####################################################
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
    return LLMChain(llm=cfg.image_llm, prompt=prompt, verbose=cfg.verbose_llm)


def generate_image(chain: LLMChain, description: str) -> str:
    return DallEAPIWrapper().run(chain.run(description))


def generate_advice_image(chain: LLMChain, advice: ConditionalAdvice) -> str:
    image_description = f"Please generate an image with speech ballons with the text of these advices: {advice}"
    return generate_image(chain, image_description)


if __name__ == "__main__":
    from data_questionnaire_agent.test.provider.advice_provider import create_advice_2
    chain = image_chain_factory()

    def create_image_from_advice():
        image_url = generate_advice_image(chain, create_advice_2())
        return image_url
    
    def create_image_bot():
        image_prompt_res = chain.run({"image_desc": 
                                      """A chatbot next to a data gouvernance expert in a smart suit in a futuristic landscape like the ones you have in the movie TRON. 
The chatbot should be to the left and the expert on the right side of the image. Please include no text in the image."""})
        print(image_prompt_res)
        image_url = DallEAPIWrapper().run(image_prompt_res)
        return image_url
    
    print(create_image_bot())
