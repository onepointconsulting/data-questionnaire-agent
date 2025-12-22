--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-04-14 15:20:03

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
-- TOC entry 4975 (class 0 OID 27435)
-- Dependencies: 218
-- Data for Name: tb_skill; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (1, 'Fundraising');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (2, 'Data Ethics');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (3, 'AI governance');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (4, 'Senior Stakeholder Management');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (5, 'Database Marketing');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (6, 'Business Analytics');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (7, 'Business Intelligence');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (8, 'Communications Audits');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (9, 'Team Management');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (10, 'Business-to-Business (B2B)');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (11, 'Business Development');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (12, 'Strategic Planning');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (13, 'Generalist Profile');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (14, 'Artificial Intelligence (AI)');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (15, 'Recruiting');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (16, 'Scrum');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (17, 'Executive Advisory');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (18, 'Board Advisory Services');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (19, 'Business Advising');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (20, 'Reputation Management');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (21, 'Client Services');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (22, 'Event Planning');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (23, 'Customer Support');
INSERT INTO public.tb_skill OVERRIDING SYSTEM VALUE VALUES (24, 'Sales');


--
-- TOC entry 4981 (class 0 OID 0)
-- Dependencies: 217
-- Name: tb_skill_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_skill_id_seq', 24, true);


-- Completed on 2025-04-14 15:20:03

--
-- PostgreSQL database dump complete
--

