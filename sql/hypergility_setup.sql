
-- Initial question
INSERT INTO TB_QUESTION(QUESTION, PREFERRED_QUESTION_ORDER, LANGUAGE_ID)
VALUES('Which area of Responsible AI are you most concerned about?', 1, 
	(SELECT ID FROM public.tb_language language_code where language_code='en'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('', '', 'Ethical AI Culture', 'Does the organisation have clearly defined ethical principles for AI which are embedded into AI development and deployment processes?', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of Responsible AI are you most concerned about?'));
	   
INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('', '', 'Fairness & Bias Monitoring', 'Are there mechanisms to identify, measure, and mitigate biases to ensure fairness in data and AI models?', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of Responsible AI are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('', '', 'Transparency, Explainability & Interpretability', 'Can the organisation explain how its AI systems make decisions so that its AI models can be interpretable to users and stakeholders?', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of Responsible AI are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('', '', 'Privacy & Data Protection', 'Are data privacy and protection measures in place, compliant with regulations such as GDPR or CCPA using data anonymisation or minimisation techniques where necessary?', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of Responsible AI are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('', '', 'Accountability', 'Is there clear accountability for AI decisions and their impacts including clear roles and processes for auditing AI systems and addressing errors or harm?', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of Responsible AI are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('', '', 'Robustness & Safety', 'Are AI systems stress-tested to ensure they perform reliably under various conditions and measures in place to prevent adversarial attacks or misuse?', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of Responsible AI are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('', '', 'Predictability & Stakeholder Focus', 'Are diverse stakeholders (e.g., end users, communities, regulators) consulted in AI design and deployment to ensure their concerns are addressed?', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of Responsible AI are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('', '', 'Risk Monitoring & Continuous Improvement', 'Are there ongoing processes to monitor AI systems for performance, bias, and ethical concerns and to ensure updates or corrections are managed over time?', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of Responsible AI are you most concerned about?'));

-- configuration

INSERT INTO PUBLIC.TB_GLOBAL_CONFIGURATION(CONFIG_KEY, CONFIG_VALUE, DESCRIPTION)
VALUES('MESSAGE_UPPER_LIMIT', 14, 'Maximum number of messages after which the report is generated.');

INSERT INTO PUBLIC.TB_GLOBAL_CONFIGURATION(CONFIG_KEY, CONFIG_VALUE, DESCRIPTION)
VALUES('MESSAGE_LOWER_LIMIT', 8, 'Number of messages after which the user is given the option of stopping the questionnaire before time');