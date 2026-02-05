INSERT INTO tb_global_configuration(config_key, config_value) values('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1');
INSERT INTO tb_global_configuration(config_key, config_value) values('OPENROUTER_API_KEY', '<key>');
INSERT INTO tb_global_configuration(config_key, config_value) values('OPENROUTER_PROVIDER', 'google-ai-studio');
update tb_global_configuration set config_value = 'google/gemini-3-flash-preview' where config_key = 'OPENAI_MODEL';