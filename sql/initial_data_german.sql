-- Add language
INSERT INTO public.tb_language(language_code) VALUES ('en');

-- Initial question
INSERT INTO TB_QUESTION(QUESTION, PREFERRED_QUESTION_ORDER, LANGUAGE_ID)
VALUES('Mit welchen Herausforderungen sehen Sie sich als Flüchtling derzeit konfrontiert?', 1, (SELECT ID FROM TB_LANGUAGE WHERE language_code = 'de'));


INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('healthcare-access.jpg', 'Zugang zur Gesundheitsversorgung', 'Zugang zur Gesundheitsversorgung', 'I require medical assistance or have concerns about accessing healthcare services.',
	(SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Mit welchen Herausforderungen sehen Sie sich als Flüchtling derzeit konfrontiert?'));


INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('family-separation.jpg', 'Trennung oder Verlust der Familie', 'Trennung oder Verlust der Familie', 'Ich habe den Kontakt zu Familienmitgliedern verloren oder stehe vor der Herausforderung, wieder mit ihnen zusammenzukommen.',
	(SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Mit welchen Herausforderungen sehen Sie sich als Flüchtling derzeit konfrontiert?'));


INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('safety-and-harassment.jpg', 'Sicherheit und Belästigung', 'Sicherheit und Belästigung', 'Ich erlebe Mobbing, Belästigung oder fühle mich in meinem aktuellen Umfeld unsicher.',
	(SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Mit welchen Herausforderungen sehen Sie sich als Flüchtling derzeit konfrontiert?'));



INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('language-barriers.jpg', 'Sprachbarrieren', 'Sprachbarrieren', 'Ich finde es schwierig, die Landessprache zu kommunizieren oder zu verstehen.',
	(SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Mit welchen Herausforderungen sehen Sie sich als Flüchtling derzeit konfrontiert?'));


INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('legal-assistance-needs.jpg', 'Bedarf an rechtlicher Unterstützung', 'Bedarf an rechtlicher Unterstützung', 'Ich benötige rechtliche Unterstützung oder Beratung in Einwanderungs- und Asylangelegenheiten.',
	(SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Mit welchen Herausforderungen sehen Sie sich als Flüchtling derzeit konfrontiert?'));


INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('interview-preparation.jpg', 'Interviewvorbereitung', 'Interviewvorbereitung', 'Ich benötige rechtliche Unterstützung oder Beratung bei der Vorbereitung meines Asyl-Interviewprozesses.',
	(SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Mit welchen Herausforderungen sehen Sie sich als Flüchtling derzeit konfrontiert?'));
