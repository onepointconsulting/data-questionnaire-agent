--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-04-14 15:24:23

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 222 (class 1259 OID 27455)
-- Name: tb_consultant_skill; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_consultant_skill (
    id integer NOT NULL,
    consultant_id integer NOT NULL,
    skill_id integer NOT NULL
);


ALTER TABLE public.tb_consultant_skill OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 27454)
-- Name: tb_consultant_skill_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.tb_consultant_skill ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.tb_consultant_skill_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 4977 (class 0 OID 27455)
-- Dependencies: 222
-- Data for Name: tb_consultant_skill; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (1, 1, 1);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (2, 1, 2);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (3, 1, 3);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (4, 1, 4);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (5, 2, 5);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (6, 2, 6);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (7, 2, 7);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (8, 2, 8);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (9, 3, 9);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (10, 3, 10);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (11, 3, 11);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (12, 3, 12);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (13, 4, 13);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (14, 4, 14);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (15, 4, 15);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (16, 4, 16);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (17, 5, 17);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (18, 5, 18);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (19, 5, 19);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (20, 5, 20);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (21, 6, 21);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (22, 6, 22);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (23, 6, 23);
INSERT INTO public.tb_consultant_skill OVERRIDING SYSTEM VALUE VALUES (24, 6, 24);


--
-- TOC entry 4983 (class 0 OID 0)
-- Dependencies: 221
-- Name: tb_consultant_skill_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_consultant_skill_id_seq', 24, true);


--
-- TOC entry 4823 (class 2606 OID 27459)
-- Name: tb_consultant_skill tb_consultant_skill_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_consultant_skill
    ADD CONSTRAINT tb_consultant_skill_pkey PRIMARY KEY (id);


--
-- TOC entry 4825 (class 2606 OID 27461)
-- Name: tb_consultant_skill unique_consultant_skill; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_consultant_skill
    ADD CONSTRAINT unique_consultant_skill UNIQUE (consultant_id, skill_id);


--
-- TOC entry 4826 (class 2606 OID 27462)
-- Name: tb_consultant_skill consultant_skill_consultant_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_consultant_skill
    ADD CONSTRAINT consultant_skill_consultant_id FOREIGN KEY (consultant_id) REFERENCES public.tb_consultant(id) ON DELETE CASCADE;


--
-- TOC entry 4827 (class 2606 OID 27467)
-- Name: tb_consultant_skill consultant_skill_skill_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_consultant_skill
    ADD CONSTRAINT consultant_skill_skill_id FOREIGN KEY (skill_id) REFERENCES public.tb_skill(id) ON DELETE CASCADE;


-- Completed on 2025-04-14 15:24:23

--
-- PostgreSQL database dump complete
--

