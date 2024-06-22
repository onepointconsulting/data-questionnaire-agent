-- Add language
INSERT INTO public.tb_language(language_code) VALUES ('en');

-- Initial question
INSERT INTO TB_QUESTION(QUESTION, PREFERRED_QUESTION_ORDER, LANGUAGE_ID)
VALUES('What challenges are you currently facing as a refugee?', 1, (SELECT ID FROM TB_LANGUAGE WHERE language_code = 'en'));


INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('healthcare-access.jpg', 'Document-related issues', 'Document-related issues', 'I require medical assistance or have concerns about accessing healthcare services.',
	(SELECT ID FROM TB_QUESTION WHERE QUESTION = 'What challenges are you currently facing as a refugee?'));


INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('family-separation.jpg', 'Family separation or loss', 'Family separation or loss', 'I have lost contact with family members or face challenges in reuniting with them.',
	(SELECT ID FROM TB_QUESTION WHERE QUESTION = 'What challenges are you currently facing as a refugee?'));


INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('safety-and-harassment.jpg', 'Safety and harassment', 'Safety and harassment', 'I am experiencing bullying, harassment, or feel unsafe in my current environment.',
	(SELECT ID FROM TB_QUESTION WHERE QUESTION = 'What challenges are you currently facing as a refugee?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('employment-opportunities.jpg', 'Employment opportunities', 'Employment opportunities', 'I am struggling to find job opportunities or face barriers to employment.',
	(SELECT ID FROM TB_QUESTION WHERE QUESTION = 'What challenges are you currently facing as a refugee?'));


	
INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('housing-difficulties.jpg', 'Housing difficulties', 'Housing difficulties', 'I am experiencing challenges with finding adequate housing or accommodations.',
	(SELECT ID FROM TB_QUESTION WHERE QUESTION = 'What challenges are you currently facing as a refugee?'));



INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('legal-assistance-needs.jpg', 'Legal assistance needs', 'Legal assistance needs', 'I require legal support or advice on immigration and asylum matters.',
	(SELECT ID FROM TB_QUESTION WHERE QUESTION = 'What challenges are you currently facing as a refugee?'));


INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('interview-preparation.jpg', 'Interview preparation', 'Interview preparation', 'I require legal support or advice on preparing for my asylum interview process.',
	(SELECT ID FROM TB_QUESTION WHERE QUESTION = 'What challenges are you currently facing as a refugee?'));


