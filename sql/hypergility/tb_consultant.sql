--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-04-14 15:23:22

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
-- TOC entry 220 (class 1259 OID 27443)
-- Name: tb_consultant; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tb_consultant (
    id integer NOT NULL,
    given_name character varying(256) NOT NULL,
    surname character varying(256) NOT NULL,
    email character varying(256) NOT NULL,
    cv text NOT NULL,
    cv_summary text,
    industry_name character varying(256),
    geo_location character varying(256),
    linkedin_profile_url character varying(1024),
    linkedin_photo_200 character varying(1024),
    linkedin_photo_400 character varying(1024),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp without time zone,
    CONSTRAINT email_format CHECK (((email)::text ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'::text))
);


ALTER TABLE public.tb_consultant OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 27442)
-- Name: tb_consultant_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.tb_consultant ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.tb_consultant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 4978 (class 0 OID 27443)
-- Dependencies: 220
-- Data for Name: tb_consultant; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.tb_consultant OVERRIDING SYSTEM VALUE VALUES (1, 'Tuli', 'Faas', 'tuli-faas-37b8674@linkedin.com', 'Imagine a world where every new tech idea is like a superhero, making life better and safer for everyone. That''s what I do! I make sure these tech superheroes are balanced with smart strategies to keep any risks in check, so everyone can enjoy the benefits without any worries.

As a co-founder, my focus is on progressing responsible AI that further drives innovation and AI adoption. My strategic vision for the future is underpinned by a deep commitment to advancing digital transformation responsibly, ensuring its benefits are realized across our lives while maintaining the appropriate levels of transparency, explainability, data ethics and mitigating risk.

With a career spanning over two decades, the journey has been marked by a steadfast commitment to shaping the technology sector through innovative intellectual property and standards leadership at SITA. Our team''s efforts in operational data governance have paved the way for responsible AI deployment and transformative digital practices.  At the forefront of digital transformation, we have cultivated successful R&D collaborations and led change programs that have significantly shaped the sector.', 'Tuli Faas is a seasoned consultant and co-founder with over two decades of experience in the computer software industry, specializing in responsible AI and digital transformation. Based in Brighton, UK, Tuli is dedicated to advancing technology through innovative IP and standards leadership at SITA, where he held various senior legal roles. His expertise includes AI governance, data ethics, and stakeholder management, focusing on balancing technological innovation with risk mitigation. Tuli''s vision emphasizes transparency and ethical practices in AI deployment, ensuring that the benefits of technology are accessible and safe for all.', 'Computer Software', '', 'https://www.linkedin.com/in/tuli-faas-37b8674', 'https://media.licdn.com/dms/image/v2/C4E03AQE0hxkuJpb5cQ/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1517084861502?e=1750291200&v=beta&t=gOtm0gR9Oa-X2fn1y0Vr4QGeEWWaoXSPhNLygCHzJMk', 'https://media.licdn.com/dms/image/v2/C4E03AQE0hxkuJpb5cQ/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1517084861537?e=1750291200&v=beta&t=ZOUYJZt8JvEpSuGVSoo_jXCyhM7758qjmQ0vfdjJyiQ', '2025-04-14 15:09:32.782745', NULL);
INSERT INTO public.tb_consultant OVERRIDING SYSTEM VALUE VALUES (2, 'Jean Paul', 'Isson', 'jean-paul-isson@linkedin.com', 'Highly accomplished artificial intelligence (AI) Executive with over 24 years of experience in leveraging innovative analytics and AI to drive business growth and efficiency in aviation, telecommunications, online recruitment-HR and banking sectors. Proven track record in leading global teams developing cutting-edge AI and GenAI solutions achieving cost reductions, revenue growth, operational efficiency, and customer satisfaction. 

Eager to help companies as a key senior management contributor build and implement AI and GenAI strategies and solutions that transform business operations and deliver measurable outcomes. Exceptional communicator and strategic thinker, with a passion for digital revolution to drive results.

Best-selling author of Data Science & People Analytics books, internationally acclaimed keynote speaker, Data Science and AI executive programs professor, and trusted AI expert and advisor to prominent international institutions.                                                           
Coauthored 3 patents in deep learning applied to aviation: aircraft turnaround optimization passenger flow and bag management



	Drove a 15% increase in customer profitability, and 25% improvement in airport operations by delivering AI based aircraft turnaround optimizer, passenger flow simulation and on time performance AI solutions for aviation.. 
	Built and implemented the SITA Air Traffic Index, driving new business increase by 30%.
	Enhanced SITA Cybersecurity Models by 30% (threats detection and prevention) leveraging GenAI
	Transformed Monster.com''s annual revenue from $300M to over $1.3B by implementing AI solutions.
	Reduced high-customer attrition by 50% for Fido and Rogers Wireless.

Best-selling author of Data Science and People Analytics books including:
•	Win With Advanced Business Analytics
•	People Analytics in the Era of Big Data
•	Unstructured Data Analytics
Known as an internationally acclaimed keynote speaker, trusted Data Science & AI expert, and advisor to prominent international institutions. Coauthored three patents in deep learning applied to aviation.
For full bio please visit my website: jpisson.com', 'Jean Paul Isson is a seasoned AI executive with over 24 years of experience in driving business growth across various sectors, including aviation and telecommunications. As a former Vice President at SITA and Global VP at Monster, he has led the development of innovative AI solutions that significantly improved operational efficiency and customer satisfaction. A best-selling author and keynote speaker, he specializes in Data Science and People Analytics. Isson has coauthored three patents in deep learning for aviation and is dedicated to helping companies implement transformative AI strategies.', 'Information Technology & Services', 'Montreal, Quebec', 'https://www.linkedin.com/in/jean-paul-isson', 'https://media.licdn.com/dms/image/v2/C4E03AQFKvPVaDE8yvQ/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1516286975948?e=1750291200&v=beta&t=GFwB3LSxFsZGn0jUrz5EOmeRLfMnpaocM3EfGBcG7Dk', NULL, '2025-04-14 15:09:42.008202', NULL);
INSERT INTO public.tb_consultant OVERRIDING SYSTEM VALUE VALUES (3, 'Mark', 'Preston', 'markcpreston@linkedin.com', 'My name is Mark Preston and I love to help with the transformation of great digital products and software for start-ups, scale-ups, enterprises and government
Balancing agility and control to deliver innovation for commercial results.

How much do you believe that the......?

◆ Disruptive combined forces of mobile, social and low cost cloud computing is causing organisations to re-evaluate what their products are?

◆ Pressure and pace of rapid change are causing product life-cycles to shorten and revenue to fall away faster as the need to adapt technically now or lose out becomes acute?

◆ Uncertainties of managing change at pace are problematic, will it lead to successful incremental growth that is demanded by the business plan?

Who knows how to solve these problems?

Well, I can help!

..................
►   PRODUCT MANAGEMENT PROFESSIONAL HIRE ME AS A MANAGER | DIRECTOR | HEAD OF | CHIEF PRODUCT OFFICER DEPENDING ON YOUR SITUATION

✔ 17 year proven track record in delivering complex digital and Software-as-a-service solutions.

✔ In the private sector enabling many millions of £ growth in annual recurring revenue 

✔ In the public sector delivering low-cost digital journeys for new policies, generating cost savings through digital efficiencies and inclusive services for citizens


► TYPCIALLY HIRED FOR ONE OF THESE FOUR SCENARIOS

1. Unknown market problem and unknown solution

✔ Zero to One – take an idea all the way from validation and concept to get first customer.

✔ Identifying and harvesting the best problems and building MVPs to find growth.

✔Thought lead and hire people who want to discover the future together.

2. Unknown market problem and known solution.

✔ Reverse fit emerging product build to find value propositions.

✔ Undertake a discovery of customer needs.

✔ Galvanise people to story tell their creations that resonates with customers'' needs.

3. More known market problem and unknown solution

✔ Articulate emerging insights to prioritise.

✔ Inspire collaborate technical build out of value incrementally.

✔ Thought lead and hire people who want to follow the vision.

4. More known market problem and known solution

✔ Structure a product backlog.

✔ Granularly define features to direct improvements in UX, design and engineering. 

✔ Optimize product disciplines and mentor the inexperienced.

Ask me to help lets connect.

✉ mark@projectdoers.com

✆ 07828 047 584', 'Mark Preston is an experienced consultant specializing in digital product transformation and software development for various sectors, including start-ups and government. With a 17-year track record in delivering complex SaaS solutions and generating significant revenue growth, he is adept at managing product lifecycles amid rapid market changes. Mark has co-founded multiple companies and held senior roles, focusing on identifying market problems, facilitating product development, and mentoring teams. His expertise spans B2B business development, strategic planning, and improving user experience. Mark is eager to connect with organizations seeking innovative solutions.', 'Computer Software', 'Crondall, England', 'https://www.linkedin.com/in/markcpreston', 'https://media.licdn.com/dms/image/v2/D4E03AQE4Qumdq0eG1w/profile-displayphoto-shrink_200_200/B4EZOmx7S9H0Ac-/0/1733669926584?e=1750291200&v=beta&t=u-VjB5_25lY2AI9TNbwCRw3ry7w6NV8EiAE-vJEjMzs', 'https://media.licdn.com/dms/image/v2/D4E03AQE4Qumdq0eG1w/profile-displayphoto-shrink_400_400/B4EZOmx7S9H0Ak-/0/1733669926613?e=1750291200&v=beta&t=Yfvm9hKqXQ3A702CoPuUDiqn4kX4kBokJ0E-SoQ8rW0', '2025-04-14 15:09:49.784281', NULL);
INSERT INTO public.tb_consultant OVERRIDING SYSTEM VALUE VALUES (4, 'Konrad', 'Jarocinski', 'konradjarocinski@linkedin.com', 'As an experienced operator and generalist, I''ve driven growth across diverse business environments - from leading early-stage startups to contributing to unicorn scaleups and Fortune 500 corporations. At CADLabs and DataGems, I was responsible for operational efficiency and product excellence, leading crucial growth stages. At Booksy, now a unicorn, I used product-led growth techniques and data science strategies to significantly improve user engagement. I''ve also created data science and analytics strategies for major companies like Visa and Emirates, enhancing operational efficiency and strategic decision-making. Throughout my career, I''ve consistently leveraged data and AI to create business value, improving user experiences, refining operations, and uncovering new market opportunities.', 'Konrad Jarocinski is an accomplished consultant in the Information Technology & Services sector, based in the Lodz Metropolitan Area. He has a strong background in driving growth in various business settings, from startups to Fortune 500 companies. Notably, he contributed to the success of Booksy and has crafted data science strategies for firms like Visa and Emirates. His expertise lies in leveraging AI and data analytics to enhance operational efficiency and user engagement. Currently, he holds several roles, including Fractional COO and Co-Founder, and is actively involved as an angel investor.', 'Information Technology & Services', 'Lodz Metropolitan Area', 'https://www.linkedin.com/in/konradjarocinski', 'https://media.licdn.com/dms/image/v2/D4D03AQHJA3aZtRAXGA/profile-displayphoto-shrink_200_200/B4DZSyRCpMGkAY-/0/1738157599839?e=1750291200&v=beta&t=dDD4RC0bxhTrLbWOvNhiUSO3AYSKaaMjq8Q4whsv5rQ', 'https://media.licdn.com/dms/image/v2/D4D03AQHJA3aZtRAXGA/profile-displayphoto-shrink_400_400/B4DZSyRCpMGkAg-/0/1738157599839?e=1750291200&v=beta&t=DZGV633W3VJAxxr5sgzcGKxem2HAU7chbp-kmifc7Yc', '2025-04-14 15:10:02.225866', NULL);
INSERT INTO public.tb_consultant OVERRIDING SYSTEM VALUE VALUES (5, 'Emma', 'Guy', 'emma-c-guy@linkedin.com', 'Highly driven Chief Commercial Officer with over 37 years experience in Managing Board members, Strategic Operations, Marketing, Advertising, Sales Management and Sales Training, as well as building two very successful North West businesses for the last ten years. 

In Aqueous it is important about the overall productivity and effectiveness of our sales organisation, however not forgetting the health & wellbeing of our employees in the workplace. 

Chair of the Board of Trustees for Halton Haven Hopsice and an Ambassador for Prevent Breast Cancer. 

Please feel free to contact me If I can help with any way. 

www.eguy@aqueous-digital.co.uk', 'Emma Guy is a seasoned Chief Commercial Officer with over 37 years of experience in marketing, advertising, and sales management. Based in Runcorn, England, she has successfully built two businesses in the North West. Emma emphasizes the importance of productivity and employee wellbeing in sales organizations. She serves as Chair of the Board of Trustees for Halton Haven Hospice and is an Ambassador for Prevent Breast Cancer. Additionally, she is an author and board advisor, with a focus on executive advisory services and reputation management.', 'Marketing & Advertising', 'Runcorn, England', 'https://www.linkedin.com/in/emma-c-guy', NULL, NULL, '2025-04-14 15:10:12.857842', NULL);
INSERT INTO public.tb_consultant OVERRIDING SYSTEM VALUE VALUES (6, 'Michelle', 'Stephens', 'michelle-stephens-1330702a1@linkedin.com', '', 'Michelle Stephens is a consultant based in Fleet, England, specializing in client services, event planning, customer support, and sales. Although her CV does not list any specific work experiences, her skills indicate a strong foundation in managing client relationships and organizing events. Michelle is looking to leverage her expertise in a consulting role to enhance client engagement and drive sales initiatives.', '', 'Fleet, England', 'https://www.linkedin.com/in/michelle-stephens-1330702a1', 'https://media.licdn.com/dms/image/v2/D4E03AQEiZRyEKkugGg/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1700578665815?e=1750291200&v=beta&t=YBWnagjKPcvbkPBQupFgpcqO44oqtOYk7fKtZZMEESg', 'https://media.licdn.com/dms/image/v2/D4E03AQEiZRyEKkugGg/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1700578665815?e=1750291200&v=beta&t=uTM5iBP5lDEa-c2ZX6UNwEKhjUv1Kf4586t12nrqg08', '2025-04-14 15:10:21.097463', NULL);


--
-- TOC entry 4984 (class 0 OID 0)
-- Dependencies: 219
-- Name: tb_consultant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tb_consultant_id_seq', 6, true);


--
-- TOC entry 4825 (class 2606 OID 27453)
-- Name: tb_consultant tb_consultant_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_consultant
    ADD CONSTRAINT tb_consultant_email_key UNIQUE (email);


--
-- TOC entry 4827 (class 2606 OID 27451)
-- Name: tb_consultant tb_consultant_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tb_consultant
    ADD CONSTRAINT tb_consultant_pkey PRIMARY KEY (id);


--
-- TOC entry 4828 (class 1259 OID 27502)
-- Name: unique_email_ci; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX unique_email_ci ON public.tb_consultant USING btree (lower((email)::text));


-- Completed on 2025-04-14 15:23:22

--
-- PostgreSQL database dump complete
--

