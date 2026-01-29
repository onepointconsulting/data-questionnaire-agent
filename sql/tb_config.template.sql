--
-- PostgreSQL database dump template
-- This is a template file with obfuscated values for configuration
-- Copy this file to tb_config.sql and replace placeholder values with actual secrets
--

\restrict xw5S69TQ9fr5WxmOwO6Z6352nKKLx6jty6dF6ZBRMLKI3VJqxW3VTjrqwhf0R6K

-- Dumped from database version 17.4
-- Dumped by pg_dump version 18.0

-- Started on 2026-01-29 10:46:32

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4983 (class 0 OID 49172)
-- Dependencies: 236
-- Data for Name: tb_global_configuration; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (169, 'AGGREGATOR_REPORT_FOLDER', '/tmp/data_wellness', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (158, 'DWELL_URL', 'http://localhost:5173', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (159, 'DWISE_URL', 'http://localhost:5174?index.html', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (161, 'GRAPHRAG_BASE_URL', 'https://engine.example.com/protected/project', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (163, 'GRAPHRAG_CONTEXT_SIZE', '3000', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (167, 'GRAPHRAG_ENGINE', 'lightrag', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (164, 'GRAPHRAG_JWT', 'YOUR_GRAPHRAG_JWT_TOKEN_HERE', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (162, 'GRAPHRAG_MODE', 'local', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (165, 'GRAPHRAG_PROJECT', 'your_project_name', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (166, 'GRAPHRAG_READ_TIMEOUT', '20', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (155, 'JWT_ALGORITHM', 'HS256', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (157, 'JWT_GEN_FOLDER', '/tmp/data-wellness-companion-hypergility/jwt_gen', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (156, 'JWT_TIME_DELTA_MINUTES', '120', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (1, 'MESSAGE_UPPER_LIMIT', '13', 'Maximum number of messages after which the report is generated.', '2025-10-15 13:25:01.003267');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (168, 'REPORT_TOKEN_LIMIT', '30000', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (160, 'USE_GRAPHRAG', 'true', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (120, 'CHATGPT_STREAMING', 'false', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (115, 'DEEP_RESEARCH_MODEL', 'o4-mini-deep-research', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (119, 'LANGCHAIN_CACHE', 'false', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (125, 'MAIL_FROM', 'noreply@example.com', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (122, 'MAIL_FROM_PERSON', 'Your Application Name', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (124, 'MAIL_PASSWORD', 'YOUR_SMTP_PASSWORD_HERE', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (126, 'MAIL_SERVER', 'email-smtp.region.amazonaws.com:25', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (127, 'MAIL_SUBJECT', 'Your recommendations from the Application Name', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (123, 'MAIL_USER', 'YOUR_SMTP_USERNAME_HERE', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (2, 'MESSAGE_LOWER_LIMIT', '8', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2025-10-15 13:25:01.003267');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (113, 'OPENAI_API_KEY', 'sk-YOUR_OPENAI_API_KEY_HERE', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (116, 'OPENAI_API_TEMPERATURE', '1', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (114, 'OPENAI_MODEL', 'gpt-4.1-mini', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (117, 'REQUEST_TIMEOUT', '300', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (121, 'UI_TIMEOUT', '60', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (118, 'VERBOSE_LLM', 'true', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (137, 'EMBEDDINGS_CHUNK_SIZE', '2500', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (136, 'EMBEDDINGS_PERSISTENCE_DIR', '${PROJECT_ROOT}/embeddings', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (128, 'FEEDBACK_EMAIL', 'feedback@example.com', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (140, 'MINIMUM_QUESTIONNAIRE_SIZE', '4', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (134, 'PDF_FOLDER', '/tmp/data_questionnaire_agent/pdfs', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (129, 'PROJECT_ROOT', '/path/to/your/project', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (130, 'QUESTION_CACHE_FOLDER', '/tmp/data_questionnaire_agent/cache', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (139, 'QUESTIONS_PER_BATCH', '1', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (135, 'RAW_TEXT_FOLDER', '${PROJECT_ROOT}/docs/raw_text', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (138, 'SEARCH_RESULTS_HOW_MANY', '2', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (131, 'TRANSLATION_PATH', '${PROJECT_ROOT}/i18n', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (132, 'WKHTMLTOPDF_BINARY', '/path/to/wkhtmltopdf/bin/wkhtmltopdf.exe', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (149, 'IMAGES_FOLDER', '${PROJECT_ROOT}/public/images', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (154, 'JWT_SECRET', 'YOUR_JWT_SECRET_HERE', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (153, 'LANGCHAIN_API_KEY', 'YOUR_LANGCHAIN_API_KEY_HERE', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (152, 'LANGCHAIN_ENDPOINT', 'https://api.smith.langchain.com', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (151, 'LANGCHAIN_PROJECT', 'Your Project Name', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (150, 'LANGCHAIN_TRACING_V2', 'true', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (143, 'OPENAI_RETRY_ATTEMPTS', '3', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (144, 'OPENAI_WAIT_FIXED', '30', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (142, 'SHOW_SESSION_COST', 'false', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (141, 'TOKEN_LIMIT', '6000', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (147, 'WEBSOCKET_CORS_ALLOWED_ORIGINS', '*', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (146, 'WEBSOCKET_PORT', '8085', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');
INSERT INTO public.tb_global_configuration (id, config_key, config_value, description, created_at) VALUES (145, 'WEBSOCKET_SERVER', '0.0.0.0', 'Number of messages after which the user is given the option of stopping the questionnaire before time', '2026-01-28 13:54:41.344594');


--
-- TOC entry 4990 (class 0 OID 0)
-- Dependencies: 235
-- Name: tb_global_configuration_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_global_configuration_id_seq', 464, true);


-- Completed on 2026-01-29 10:46:32

--
-- PostgreSQL database dump complete
--

\unrestrict xw5S69TQ9fr5WxmOwO6Z6352nKKLx6jty6dF6ZBRMLKI3VJqxW3VTjrqwhf0R6K
