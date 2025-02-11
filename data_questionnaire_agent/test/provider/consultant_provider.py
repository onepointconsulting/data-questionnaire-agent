import datetime

from consultant_info_generator.model import Company, Consultant, Experience, Skill


def create_simple_consultant() -> Consultant:
    company = Company(name="Onepoint Consulting Ltd")
    experience1 = Experience(
        location="London, UK",
        title="Enterprise Architect",
        company=company,
        start=datetime.datetime(2023, 1, 1),
        end=None,
    )
    consultant = Consultant(
        given_name="John",
        surname="Doe",
        email="john.doe@gmail.com",
        cv="General blabla",
        industry_name="IT",
        geo_location="London",
        linkedin_profile_url="john-doe",
        experiences=[experience1],
        skills=[Skill(name="Data Science"), Skill(name="Enterprise Architecture")],
    )
    return consultant
