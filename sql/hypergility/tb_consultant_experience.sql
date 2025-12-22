--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-04-14 15:27:06

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
-- TOC entry 230 (class 1259 OID 27504)
-- Name: tb_consultant_experience; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_consultant_experience (
    id integer NOT NULL,
    consultant_id integer NOT NULL,
    title character varying(256),
    location character varying(256),
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone,
    company_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone
);


ALTER TABLE public.tb_consultant_experience OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 27503)
-- Name: tb_consultant_experience_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.tb_consultant_experience ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.tb_consultant_experience_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 4976 (class 0 OID 27504)
-- Dependencies: 230
-- Data for Name: tb_consultant_experience; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (1, 1, 'Co-Founder', 'Brighton, England, United Kingdom', '2024-07-01 00:00:00', NULL, 1, '2025-04-14 15:09:32.782745', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (2, 1, 'Group Head Of IP', 'Aldershot Hampshire', '2000-02-01 00:00:00', '2024-07-01 00:00:00', 2, '2025-04-14 15:09:32.782745', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (3, 1, 'Director Legal', 'Guildford, England, United Kingdom', '2008-01-01 00:00:00', '2015-12-01 00:00:00', 2, '2025-04-14 15:09:32.782745', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (4, 1, 'Director Business Legal Affairs', 'London Area, United Kingdom', '2005-01-01 00:00:00', '2008-12-01 00:00:00', 2, '2025-04-14 15:09:32.782745', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (5, 1, 'Director Legal GEO', 'London Area, United Kingdom', '2002-01-01 00:00:00', '2005-12-01 00:00:00', 2, '2025-04-14 15:09:32.782745', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (6, 2, 'Founder and CEO', '', '2024-01-01 00:00:00', NULL, 6, '2025-04-14 15:09:42.008202', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (7, 2, 'Expert -Big Data ,Advanced Business Analytics and AI ', '', '2017-01-01 00:00:00', NULL, 7, '2025-04-14 15:09:42.008202', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (8, 2, 'Vice President-Chief Data Science & Artificial Intelligence Officer', 'Montreal- Canada ,    Geneva-Switzerland ', '2019-01-01 00:00:00', '2024-01-01 00:00:00', 2, '2025-04-14 15:09:42.008202', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (9, 2, 'Global Vice President Predictive Analytics & BI', 'Greater Boston Area', '2005-01-01 00:00:00', '2018-12-01 00:00:00', 9, '2025-04-14 15:09:42.008202', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (10, 2, 'Principal Teacher (Executive Certificate in  Advanced Business Analytics )', 'Montreal, Canada Area', '2013-01-01 00:00:00', '2016-12-01 00:00:00', 10, '2025-04-14 15:09:42.008202', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (11, 3, 'Chief Executive Officer | Co-Founder ', 'Brighton, England, United Kingdom', '2023-11-01 00:00:00', NULL, 1, '2025-04-14 15:09:49.784281', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (12, 3, 'Client Director | Co-Founder | SaaS | Cloud | Digital | B2B2C | GovTech ', 'Brighton | Farnborough | London', '2018-05-01 00:00:00', NULL, 12, '2025-04-14 15:09:49.784281', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (13, 3, 'Product Lead | Business Development | Digital | SaaS | GovTech | HealthTech | FinTech TravelTech', 'London | Farnham | Ljubljana Slovenia | Orem Utah | Washington DC | Boston | Sydney | EMEA', '2014-04-01 00:00:00', '2023-12-01 00:00:00', 13, '2025-04-14 15:09:49.784281', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (14, 3, 'Product Lead | Product Owner | GovTech | EdTech | SaaS', 'Sheffield, England, United Kingdom', '2023-01-01 00:00:00', '2023-02-01 00:00:00', 14, '2025-04-14 15:09:49.784281', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (15, 3, 'Innovation Lead | Programme Lead | TravelTech | HealthTech | GovTech | SaaS | Azure', 'London | EMEA | USA | Geneva | Australia', '2022-07-01 00:00:00', '2022-11-01 00:00:00', 2, '2025-04-14 15:09:49.784281', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (16, 4, 'Fractional COO / Chief of Staff', '', '2024-10-01 00:00:00', NULL, 16, '2025-04-14 15:10:02.225866', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (17, 4, 'Co-Founder', 'London, England, United Kingdom', '2023-04-01 00:00:00', NULL, 17, '2025-04-14 15:10:02.225866', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (18, 4, 'Venture Partner', 'Remote', '2024-06-01 00:00:00', NULL, 18, '2025-04-14 15:10:02.225866', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (19, 4, 'Angel Investor', '', '2023-09-01 00:00:00', NULL, 19, '2025-04-14 15:10:02.225866', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (20, 4, 'Angel Investor', 'Poland', '2023-07-01 00:00:00', NULL, 20, '2025-04-14 15:10:02.225866', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (21, 5, 'Chief Commercial Officer (CCO)', 'Runcorn', '2023-04-01 00:00:00', NULL, 21, '2025-04-14 15:10:12.857842', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (22, 5, 'Ambassador', 'Manchester, England, United Kingdom', '2021-04-01 00:00:00', NULL, 22, '2025-04-14 15:10:12.857842', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (23, 5, 'Author', '', '2020-05-01 00:00:00', NULL, 23, '2025-04-14 15:10:12.857842', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (24, 5, 'Chair of the Board of Trustees', 'Runcorn, England, United Kingdom', '2022-04-01 00:00:00', '2025-03-01 00:00:00', 24, '2025-04-14 15:10:12.857842', NULL);
INSERT INTO public.tb_consultant_experience OVERRIDING SYSTEM VALUE VALUES (25, 5, 'Board Advisor', '', '2023-12-01 00:00:00', '2025-02-01 00:00:00', 1, '2025-04-14 15:10:12.857842', NULL);


--
-- TOC entry 4982 (class 0 OID 0)
-- Dependencies: 229
-- Name: tb_consultant_experience_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_consultant_experience_id_seq', 25, true);


--
-- TOC entry 4824 (class 2606 OID 27511)
-- Name: tb_consultant_experience tb_consultant_experience_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_consultant_experience
    ADD CONSTRAINT tb_consultant_experience_pkey PRIMARY KEY (id);


--
-- TOC entry 4825 (class 2606 OID 27517)
-- Name: tb_consultant_experience company_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_consultant_experience
    ADD CONSTRAINT company_id FOREIGN KEY (company_id) REFERENCES public.tb_company(id) ON DELETE CASCADE;


--
-- TOC entry 4826 (class 2606 OID 27512)
-- Name: tb_consultant_experience consultant_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_consultant_experience
    ADD CONSTRAINT consultant_id FOREIGN KEY (consultant_id) REFERENCES public.tb_consultant(id) ON DELETE CASCADE;


-- Completed on 2025-04-14 15:27:06

--
-- PostgreSQL database dump complete
--

