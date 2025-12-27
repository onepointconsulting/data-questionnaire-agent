import asyncio

import click
# from consultant_info_generator.consultant_info_tools import extract_consultant

# from data_questionnaire_agent.bootstrap import db_cfg
from data_questionnaire_agent.service.image_import_service import import_images
from data_questionnaire_agent.service.persistence_service_consultants_async import (
    read_consultant_image
)

@click.group()
def cli():
    pass


# @cli.command()
# @click.option(
#     "--linkedin_id", "-lid", help="The linked in ID", multiple=True, required=True
# )
# def save_consultants(linkedin_id: list[str]):
#     for id in linkedin_id:
#         try:
#             consultant = extract_consultant(id)
#             click.echo(f"Processed {id}")
#             asyncio.run(save_consultant(consultant))
#         except Exception as e:
#             click.echo(f"Failed to retrieve {id}", err=True)
#             click.echo(f"Error message {e}", err=True)


@cli.command()
def bootstrap_photos():
    asyncio.run(abootstrap_photos())


async def abootstrap_photos():

    consultants = [
        {
            "email": "chrisjwray@linkedin.com",
            "image_url": "https://media.licdn.com/dms/image/v2/C5603AQEJI3rMmTyUnA/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1517403914519?e=1767830400&v=beta&t=VR21mTCCx2m35ETVcsDCulwB4cYDxKnJv1oM34c-z6k"
        },
        {
            "email": "tuli-faas-37b8674@linkedin.com",
            "image_url": "https://media.licdn.com/dms/image/v2/D4E03AQF-LGWIoTvW0g/profile-displayphoto-scale_400_400/B4EZkuuBRlIkAg-/0/1757425441876?e=1767830400&v=beta&t=mEUHWGbOuR-LBNoxKfbRtaFmIUD45d1y2i-CR_HpDhs"
        },
        {
            "email": "allanschweitz@linkedin.com",
            "image_url": "https://media.licdn.com/dms/image/v2/D4E03AQEOQ-JSZRUdaQ/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1724161708940?e=1768435200&v=beta&t=FXy3o9w7SwKJV6SVTN1gvSnrUeFg7TFWSDL-F0mZE64"
        },
        {
            "email": "shashinbshah@linkedin.com",
            "image_url": "https://media.licdn.com/dms/image/v2/D4E03AQEEBDoAz1mbaA/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1725447261446?e=1768435200&v=beta&t=nbbWKipwsxsKsM1uBhrO3ivhIXy4-YSiGInxt3Gltg0"
        },
        {
            "email": "alexander-polev-cto@linkedin.com",
            "image_url": "https://media.licdn.com/dms/image/v2/D4E03AQEY0W3f_Xug1g/profile-displayphoto-shrink_800_800/B4EZaqQl8bHIAc-/0/1746613199118?e=1768435200&v=beta&t=PWtis1MlE81hommj_4z4tic2S-JPpzU32CoBATRthEU"
        },
        {
            "email": "miguelvale@linkedin.com",
            "image_url": "https://media.licdn.com/dms/image/v2/C5603AQHIAHpZhpMq9Q/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1516274191466?e=1768435200&v=beta&t=VXODY66geR7Fmb0ctxKcgMMpvKt4SyHtZr55EdM-140"
        },
        {
            "email": "gil-palma-fernandes@linkedin.com",
            "image_url": "https://media.licdn.com/dms/image/v2/C4D03AQEDBl5Kh0CY8Q/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1602326759733?e=1768435200&v=beta&t=5W3P0bUkyL127Uzj5R_XgM6sS6HEPjQzhdW00sVAZAc"
        },
        {
            "email": "sangeethaviswanathan@linkedin.com",
            "image_url": "https://media.licdn.com/dms/image/v2/D4E03AQG8rp_wuVzmLA/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1726141935535?e=1768435200&v=beta&t=24NZmeFjQaIGaNlq4QaN71gWxMiN1BCn_JkBff70uqg"
        }
    ]
    for consultant in consultants:
        image = await read_consultant_image(consultant["email"])
        if image is not None:
            print(f"Image for {consultant['email']} already exists")
        else:
            print(f"Image for {consultant['email']} does not exist")
            inserted = await import_images(consultant["email"], consultant["image_url"])
            print(f"Inserted {inserted} rows")


if __name__ == "__main__":
    cli()
