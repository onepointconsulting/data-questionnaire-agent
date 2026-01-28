
import asyncio
from pathlib import Path

from data_questionnaire_agent.model.global_configuration import GlobalConfiguration, GlobalConfigurationProperty
from data_questionnaire_agent.service.persistence_service_async import update_global_configuration


def load_global_config_from_dot_env():
    env_file = Path(__file__).resolve().parent.parent.parent / ".env"
    assert env_file.exists(), f"Cannot find {env_file}"

    keys: list[GlobalConfigurationProperty] = []

    with open(env_file, "r") as f:
        line = f.readline()
        for line in f:
            if not line.startswith("#") and "=" in line:
                key, value = line.split("=")
                key = key.strip()
                value = value.strip()
                if not key.startswith("DB_"):
                    keys.append(GlobalConfigurationProperty(config_key=key, config_value=value))

    asyncio.run(update_global_configuration(GlobalConfiguration(properties=keys)))
    return keys
            

if __name__ == "__main__":
    global_config = load_global_config_from_dot_env()
    for prop in global_config:
        print(f"{prop.config_key}: {prop.config_value}")