import requests

from data_questionnaire_agent.service.persistence_service_consultants_async import read_consultant_image, save_consultant_image


async def import_images(email: str, image_url: str) -> int | None:
    # Download the image from the url
    response = requests.get(image_url)
    if response.status_code != 200:
        return None
    content_type = response.headers["Content-Type"]
    image = response.content
    # Save the image to the database
    image_name = f"{email}.{content_type.split('/')[1]}"
    return await save_consultant_image(email, image_name,image)