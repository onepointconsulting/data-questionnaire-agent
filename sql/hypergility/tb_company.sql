--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-04-14 15:25:33

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
-- TOC entry 226 (class 1259 OID 27479)
-- Name: tb_company; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_company (
    id integer NOT NULL,
    company_name character varying(256) NOT NULL
);


ALTER TABLE public.tb_company OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 27478)
-- Name: tb_company_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.tb_company ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.tb_company_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 4975 (class 0 OID 27479)
-- Dependencies: 226
-- Data for Name: tb_company; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (1, 'Hypergility Ltd');
INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (2, 'SITA');
INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (6, 'eigenvectorAI.com');
INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (7, 'APM - Association Progrès du Management');
INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (9, 'Monster  Worldwide');
INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (10, 'Concordia University - John Molson School of Business');
INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (12, 'Govforms Ltd');
INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (13, 'Project Doers Ltd');
INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (14, 'Department for Education');
INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (16, 'AIsidekick.co');
INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (17, 'DataGems');
INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (18, 'Erez Capital');
INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (19, 'BADideas.fund');
INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (20, 'Founders Capital');
INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (21, 'Aqueous Digital');
INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (22, 'Prevent Breast Cancer');
INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (23, 'The Menopausal Godmother');
INSERT INTO public.tb_company OVERRIDING SYSTEM VALUE VALUES (24, 'Halton Haven Hospice');


--
-- TOC entry 4981 (class 0 OID 0)
-- Dependencies: 225
-- Name: tb_company_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_company_id_seq', 25, true);


--
-- TOC entry 4823 (class 2606 OID 27485)
-- Name: tb_company tb_company_company_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_company
    ADD CONSTRAINT tb_company_company_name_key UNIQUE (company_name);


--
-- TOC entry 4825 (class 2606 OID 27483)
-- Name: tb_company tb_company_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_company
    ADD CONSTRAINT tb_company_pkey PRIMARY KEY (id);


-- Completed on 2025-04-14 15:25:33

--
-- PostgreSQL database dump complete
--

