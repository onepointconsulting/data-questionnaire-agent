import asyncio
from data_questionnaire_agent.service.persistence_service_async import (
    delete_questionnaire_status,
    insert_questionnaire_status,
    select_questionnaire,
    select_initial_question,
    select_suggestions,
    update_answer,
    save_session_configuration,
    select_session_configuration,
    update_session_steps,
    delete_session_configuration,
    select_current_session_steps_and_language,
    save_report,
    insert_questionnaire_status_suggestions,
    select_questionnaire_status_suggestions,
    save_ontology,
    fetch_ontology,
    delete_ontology,
    save_confidence,
    select_confidence,
    has_final_report,
    delete_last_question,
    insert_jwt_token,
    delete_jwt_token,
    check_question_exists,
    select_questionnaires_by_tokens,
    select_global_configuration,
    update_regenerated_question
)
from data_questionnaire_agent.model.session_configuration import (
    DEFAULT_SESSION_STEPS,
    SessionConfigurationEntry,
    SessionProperties,
)
from data_questionnaire_agent.model.jwt_token import JWTToken

if __name__ == "__main__":
    from data_questionnaire_agent.test.provider.question_answer_provider import (
        create_question_answer_with_possible_answers,
    )
    from data_questionnaire_agent.test.provider.questionnaire_status_provider import (
        create_simple,
    )
    from data_questionnaire_agent.test.provider.session_configuration_provider import (
        create_session_configuration,
    )

    async def test_insert_questionnaire_status():
        qs = create_simple()
        new_qs = await insert_questionnaire_status(qs)
        assert new_qs is not None
        assert new_qs.id is not None
        check_qs = await select_questionnaire(new_qs.session_id)
        assert check_qs is not None
        assert len(check_qs) == 1
        deleted = await delete_questionnaire_status(new_qs.id)
        assert deleted == 1

    async def test_select_initial_fa():
        question = await select_initial_question("fa")
        assert question is not None
        print(question)

    async def test_select_initial_en():
        question = await select_initial_question("en")
        assert question is not None
        suggestions = await select_suggestions(question)
        assert len(suggestions) > 0
        for s in suggestions:
            print(s)

    async def test_insert_answer():
        qs = create_simple()
        new_qs = await insert_questionnaire_status(qs)
        assert new_qs is not None
        assert new_qs.id is not None
        session_id = qs.session_id
        test_answer = "Some answer whatsoever"
        id = await update_answer(session_id, test_answer)
        assert id is not None
        check_qs = await select_questionnaire(session_id)
        assert check_qs[0].answer == test_answer
        deleted = await delete_questionnaire_status(new_qs.id)
        assert deleted == 1

    async def test_select_answers():
        qs = create_simple()
        new_qs = await insert_questionnaire_status(qs)
        assert new_qs is not None
        assert new_qs.id is not None
        session_id = qs.session_id
        test_answer = "Some answer whatsoever"
        id = await update_answer(session_id, test_answer)
        assert id is not None
        check_answers = await select_questionnaire(session_id)
        assert len(check_answers.questions) > 0
        deleted = await delete_questionnaire_status(new_qs.id)
        assert deleted == 1

    async def test_session_configuration_save():
        session_configuration = create_session_configuration()
        saved = await save_session_configuration(session_configuration)
        assert isinstance(saved, SessionConfigurationEntry)
        assert saved.id is not None
        session_configuration = await select_session_configuration(saved.session_id)
        assert len(session_configuration.configuration_entries) > 0
        updated_id = await update_session_steps(saved.session_id, 10)
        assert updated_id == saved.id
        deleted = await delete_session_configuration(saved.id)
        assert deleted == 1

    async def test_select_current_session_steps():
        session_configuration = create_session_configuration()
        saved = await save_session_configuration(session_configuration)
        assert isinstance(saved, SessionConfigurationEntry)
        session_properties: SessionProperties = (
            await select_current_session_steps_and_language(saved.session_id)
        )
        assert session_properties.session_steps == DEFAULT_SESSION_STEPS
        deleted = await delete_session_configuration(saved.id)
        assert deleted == 1

    async def test_save_report():
        from data_questionnaire_agent.test.provider.advice_provider import (
            create_simple_advice,
        )

        advice = create_simple_advice()
        dummy_session = "12321231231231"
        id = await save_report(dummy_session, advice, 0)
        assert id is not None
        deleted = await delete_questionnaire_status(id)
        assert deleted == 1

    async def test_insert_questionnaire_status_suggestions():
        qs = create_simple()
        new_qs = await insert_questionnaire_status(qs)
        assert new_qs is not None
        assert new_qs.id is not None
        question_answer = create_question_answer_with_possible_answers()
        changed = await insert_questionnaire_status_suggestions(
            new_qs.id, question_answer
        )
        assert changed > 1
        possible_question_answers = await select_questionnaire_status_suggestions(
            new_qs.id
        )
        assert len(possible_question_answers) > 0
        deleted = await delete_questionnaire_status(new_qs.id)
        assert deleted == 1

    async def test_save_ontology():
        from data_questionnaire_agent.test.provider.ontology_provider import (
            create_ontology,
        )

        ontology = create_ontology()
        session_id = "fake_id"
        created = await save_ontology(session_id, ontology)
        assert created > 0
        relationships = await fetch_ontology(session_id)
        assert relationships is not None
        deleted = await delete_ontology(session_id)
        assert deleted > 0

    async def test_insert_confidence_rating():
        from data_questionnaire_agent.test.provider.confidence_provider import (
            create_confidence_rating,
        )

        qs = create_simple()
        new_qs = await insert_questionnaire_status(qs)
        session_id = new_qs.session_id
        confidence = create_confidence_rating()
        step = 0
        saved_confidence = await save_confidence(session_id, step, confidence)
        assert saved_confidence is not None
        assert saved_confidence.id is not None
        selected_confidence = await select_confidence(session_id, step)
        assert selected_confidence is not None
        deleted = await delete_questionnaire_status(new_qs.id)
        assert deleted == 1

    async def test_delete_last_question():
        qs = create_simple()
        new_qs = await insert_questionnaire_status(qs)
        assert new_qs is not None
        assert new_qs.id is not None
        has_report = await has_final_report(qs.session_id)
        assert not has_report
        deleted_id = await delete_last_question(qs.session_id)
        assert deleted_id is not None, "Delete last question failed."

    async def test_create_jwt():
        jwt_token = JWTToken(email="john.doe@test.com", token="test")
        id = await insert_jwt_token(jwt_token)
        assert id is not None, "JWT token id is not available"
        count = await delete_jwt_token(id)
        assert count == 1, "Number of deleted tokens not 1"

    async def test_check_question_exists():
        # setup
        qs = create_simple()
        new_qs = await insert_questionnaire_status(qs)
        new_qs2 = await insert_questionnaire_status(qs)

        exists = await check_question_exists(qs.question, qs.session_id)
        assert exists, f"The question {qs.question} should exist."

        # delete
        deleted = await delete_questionnaire_status(new_qs.id)
        assert deleted == 1
        deleted2 = await delete_questionnaire_status(new_qs2.id)
        assert deleted2 == 1

    async def test_select_questionnaires_by_tokens():
        import pickle

        from data_questionnaire_agent.config import cfg

        res = await select_questionnaires_by_tokens(
            [
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpEMkpXTkhBNTZGN1lHRENDU1czRjJaQiIsIm5hbWUiOiJHaWwiLCJpYXQiOjE3MzIwMzI0ODR9.r8LTAiuORLPk2QnrS8YMcX7dHdlYKndHuXc3PEY6Msw",
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpEVDY0S1gxR0hTSktTQVcwSE1aSEhERyIsIm5hbWUiOiJUZXN0XzQiLCJpYXQiOjE3MzI4MjQ0MjB9.PUMd-BBH3SjuXdlG8SWQXsvCJApRW7xy_giEVx84yA4",
            ]
        )
        assert res is not None
        assert len(res) > 0, "No results available"
        with open(cfg.project_root / "data/questionnaire.pkl", "wb") as f:
            pickle.dump(res, f)

    async def test_select_questionnaires_by_tokens_all():
        import pickle

        from data_questionnaire_agent.config import cfg

        res = await select_questionnaires_by_tokens([])
        assert res is not None
        assert len(res) > 0, "No results available"
        with open(cfg.project_root / "data/questionnaire_all.pkl", "wb") as f:
            pickle.dump(res, f)

    async def test_select_global_configuration():
        global_configuration = await select_global_configuration()
        assert global_configuration is not None
        assert global_configuration.properties is not None

    async def test_update_regenerated_question():
        qs = create_simple()
        new_qs = await insert_questionnaire_status(qs)
        assert new_qs is not None
        assert new_qs.id is not None
        updated = await update_regenerated_question(qs.session_id, qs.question, 
                                                    "What if?", ["Could be this", "Could be that"])
        assert updated, "Not a single row was updated."
        deleted_id = await delete_last_question(qs.session_id)
        assert deleted_id is not None, "Delete last question failed."

    # asyncio.run(test_insert_questionnaire_status())
    # asyncio.run(test_select_initial_fa())
    # asyncio.run(test_select_initial_en())
    # asyncio.run(test_insert_answer())
    # asyncio.run(test_select_answers())
    # asyncio.run(test_session_configuration_save())
    # asyncio.run(test_select_current_session_steps())
    # asyncio.run(test_save_report())
    # asyncio.run(test_insert_questionnaire_status_suggestions())
    # asyncio.run(test_save_ontology())
    # asyncio.run(test_insert_confidence_rating())
    # asyncio.run(test_delete_last_question())
    # asyncio.run(test_create_jwt())
    # asyncio.run(test_check_question_exists())
    # asyncio.run(test_select_questionnaires_by_tokens())
    # asyncio.run(test_select_questionnaires_by_tokens_all())
    # asyncio.run(test_select_global_configuration())
    asyncio.run(test_update_regenerated_question())
    
