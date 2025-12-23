import requests
import asyncio

from data_questionnaire_agent.service.persistence_service_consultants_async import read_consultant_image, save_consultant_image


async def import_images(email: str, image_url: str) -> int | None:
    # Download the image from the url
    response = requests.get(image_url)
    if response.status_code != 200:
        return None
    image = response.content
    # Save the image to the database
    return await save_consultant_image(email, image)


if __name__ == "__main__":

    async def bootstrap():
        consultants = [
            {
                "email": "chrisjwray@linkedin.com",
                "image_url": "https://media.licdn.com/dms/image/v2/C5603AQEJI3rMmTyUnA/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1517403914519?e=1767830400&v=beta&t=VR21mTCCx2m35ETVcsDCulwB4cYDxKnJv1oM34c-z6k"
            },
            {
                "email": "tuli-faas-37b8674@linkedin.com",
                "image_url": "https://media.licdn.com/dms/image/v2/D4E03AQF-LGWIoTvW0g/profile-displayphoto-scale_400_400/B4EZkuuBRlIkAg-/0/1757425441876?e=1767830400&v=beta&t=mEUHWGbOuR-LBNoxKfbRtaFmIUD45d1y2i-CR_HpDhs"
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
        

    asyncio.run(bootstrap())