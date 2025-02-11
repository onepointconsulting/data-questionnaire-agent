import asyncio

from data_questionnaire_agent.service.persistence_service_consultants_async import (
    delete_consultant,
    delete_skill,
    read_consultants,
    save_consultant,
    upsert_skill,
)
from data_questionnaire_agent.test.provider.consultant_provider import (
    create_simple_consultant,
)

if __name__ == "__main__":

    def test_upsert_skill():
        skill = "testing123"
        count = asyncio.run(upsert_skill(skill))
        assert count == 1, "Count is expected to be 1"
        count = asyncio.run(delete_skill(skill))
        assert count == 1, "Delete count is expected to be 1"

    async def test_save_consultant():
        consultant = create_simple_consultant()
        await save_consultant(consultant)
        consultants = await read_consultants()
        assert len(consultants) > 0, "There should be at least one consultant"
        await delete_consultant(consultant)

    # test_upsert_skill()
    asyncio.run(test_save_consultant())
