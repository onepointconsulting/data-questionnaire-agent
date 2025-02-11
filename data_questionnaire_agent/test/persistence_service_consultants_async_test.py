import asyncio

from consultant_info_generator.model import Consultant, Skill

from data_questionnaire_agent.service.persistence_service_consultants_async import (
    delete_skill,
    upsert_skill,
    save_consultant,
    delete_consultant,
)

if __name__ == "__main__":

    def test_upsert_skill():
        skill = "testing123"
        count = asyncio.run(upsert_skill(skill))
        assert count == 1, "Count is expected to be 1"
        count = asyncio.run(delete_skill(skill))
        assert count == 1, "Delete count is expected to be 1"

    def test_save_consultant():
        consultant = Consultant(
            given_name="John",
            surname="Doe",
            email="john.doe@gmail.com",
            cv="General blabla",
            industry_name="IT",
            geo_location="London",
            linkedin_profile_url="john-doe",
            experiences=[],
            skills=[Skill(name="Data Science"), Skill(name="Enterprise Architecture")]
        )
        asyncio.run(save_consultant(consultant))
        asyncio.run(delete_consultant(consultant))

    # test_upsert_skill()
    test_save_consultant()
