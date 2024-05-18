from data_questionnaire_agent.model.openai_schema import ResponseQuestions
from data_questionnaire_agent.service.similarity_search import (
    init_vector_search,
    similarity_search,
)
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.service.initial_question_service import (
    chain_factory_initial_question,
    prepare_initial_question,
    prompts,
)


def test_initial_question():
    initial_question = prompts["questionnaire"]["initial"]["question"]
    assert initial_question is not None

    docsearch = init_vector_search()
    
    assert docsearch is not None
    answer = "Data Quality"
    search_res = similarity_search(docsearch, answer)
    input = prepare_initial_question(
        question=initial_question,
        answer=answer,
        questions_per_batch=1,
        knowledge_base=search_res,
    )
    chain = chain_factory_initial_question()
    res: ResponseQuestions = chain.run(input)
    # res: ResponseQuestions = chain.invoke(input)
    assert len(res.questions) > 0

    logger.info("Results: ")
    logger.info(res)

test_initial_question()