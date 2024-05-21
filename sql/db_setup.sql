-- DROP DATABASE data_wellness_companion;

-- CREATE DATABASE data_wellness_companion
--     WITH
--     OWNER = postgres
--     ENCODING = 'UTF8'
--     LOCALE_PROVIDER = 'libc'
--     CONNECTION LIMIT = -1
--     IS_TEMPLATE = False;

DROP TABLE IF EXISTS PUBLIC.TB_SESSION_CONFIGURATION;
DROP TABLE IF EXISTS PUBLIC.TB_QUESTION_SUGGESTIONS;
DROP TABLE IF EXISTS PUBLIC.TB_QUESTION;
DROP TABLE IF EXISTS PUBLIC.TB_QUESTIONNAIRE_STATUS_SUGGESTIONS;
DROP TABLE IF EXISTS PUBLIC.TB_QUESTIONNAIRE_STATUS;


CREATE TABLE PUBLIC.TB_LANGUAGE (
	ID serial NOT NULL,
	LANGUAGE_CODE CHARACTER VARYING(2) NOT NULL UNIQUE,
	PRIMARY KEY (ID)
);

CREATE TABLE PUBLIC.TB_QUESTIONNAIRE_STATUS (
	ID serial NOT NULL,
	SESSION_ID CHARACTER VARYING(36) NOT NULL,
	QUESTION CHARACTER VARYING(65535) NOT NULL,
	ANSWER CHARACTER VARYING(4096) NULL,
	FINAL_REPORT boolean, 
	CREATED_AT TIMESTAMP DEFAULT NOW(),
	UPDATED_AT TIMESTAMP DEFAULT NOW(),
	TOTAL_COST NUMERIC(9, 5) NULL,
	PRIMARY KEY (ID)
);

CREATE TABLE PUBLIC.TB_QUESTION (
	ID serial NOT NULL,
	QUESTION CHARACTER VARYING(1024) NOT NULL,
	PREFERRED_QUESTION_ORDER int NULL,
	LANGUAGE_ID INTEGER NULL,
	PRIMARY KEY (ID),
	CONSTRAINT LANGUAGE_ID
		FOREIGN KEY (LANGUAGE_ID) REFERENCES PUBLIC.TB_LANGUAGE (ID) 
		MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE
);

-- ALTER TABLE TB_QUESTION ADD LANGUAGE_ID INTEGER NULL;
-- ALTER TABLE TB_QUESTION ADD CONSTRAINT LANGUAGE_ID
--     FOREIGN KEY (LANGUAGE_ID) REFERENCES PUBLIC.TB_LANGUAGE (ID) 
--     MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE;

CREATE TABLE PUBLIC.TB_QUESTION_SUGGESTIONS(
	ID serial NOT NULL,
	IMG_SRC CHARACTER VARYING(100) NOT NULL,
	IMG_ALT CHARACTER VARYING(256) NOT NULL,
	TITLE CHARACTER VARYING(256) NOT NULL,
	MAIN_TEXT CHARACTER VARYING(1024) NOT NULL,
	QUESTION_ID integer NOT NULL,
	PRIMARY KEY (ID),
	CONSTRAINT QUESTION_ID
		FOREIGN KEY (QUESTION_ID) REFERENCES PUBLIC.TB_QUESTION (ID) 
		MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION NOT VALID
);

CREATE TABLE PUBLIC.TB_SESSION_CONFIGURATION(
	ID serial NOT NULL,
	SESSION_ID CHARACTER VARYING(36) NOT NULL,
	CONFIG_KEY CHARACTER VARYING(36) NOT NULL,
	CONFIG_VALUE CHARACTER VARYING(255) NOT NULL,
	PRIMARY KEY (ID)
);

CREATE TABLE PUBLIC.TB_QUESTIONNAIRE_STATUS_SUGGESTIONS(
	ID serial NOT NULL,
	QUESTIONNAIRE_STATUS_ID INTEGER NOT NULL,
	MAIN_TEXT CHARACTER VARYING(2048) NOT NULL,
	PRIMARY KEY (ID),
	CONSTRAINT QUESTIONNAIRE_STATUS_ID
		FOREIGN KEY (QUESTIONNAIRE_STATUS_ID) REFERENCES PUBLIC.TB_QUESTIONNAIRE_STATUS (ID) 
		MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE
);




-- Initial question
INSERT INTO TB_QUESTION(QUESTION, PREFERRED_QUESTION_ORDER)
VALUES('Which area of your data ecosystem are you most concerned about?', 1);

-- Suggestions
INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('poor_data_quality.png', 'Poor data quality', 'Poor data quality', 'Low-quality data can lead to incorrect insights and poor decision-making.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosystem are you most concerned about?'));
	   
INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('compliance_risks.png', 'Compliance and security risks', 'Compliance and security risks', 'Mishandling data can lead to legal troubles and reputational damage.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosystem are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('data_silos.png', 'Data silos', 'Data silos', 'Data trapped in departmental silos can be inaccessible to other parts.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosystem are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('lack_of_skilled_personnel.png', 'Lack of skilled personnel', 'Lack of skilled personnel', 'Missing skills in data science, analytics, AI and ML can impede the effective use of data.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosystem are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('data_overload.png', 'Data overload', 'Data overload', '"Data glut" can slow down processes and make it difficult to identify what data is actually useful.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosystem are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('cost_and_complexity.png', 'Cost and complexity', 'Cost and complexity', 'A robust data analytics infrastructure requires significant investment of resources.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosystem are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('inconsistent_data_strategies.png', 'Inconsistent data strategies', 'Inconsistent data strategies', 'Difficult to align with modern concepts like Data Fabric, Mesh and Generative AI.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosystem are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('resistence_to_change.png', 'Resistance to change', 'Resistance to change', 'Employees need to adapt to new ways of operating to make data-driven transformation work.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosystem are you most concerned about?'));