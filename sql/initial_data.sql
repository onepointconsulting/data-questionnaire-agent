-- Add language
INSERT INTO public.tb_language(language_code) VALUES ('en');
INSERT INTO public.tb_language(language_code) VALUES ('pt');


-- Initial question
INSERT INTO TB_QUESTION(QUESTION, PREFERRED_QUESTION_ORDER, LANGUAGE_ID)
VALUES('Which area of your data ecosystem are you most concerned about?', 1, (SELECT ID FROM TB_LANGUAGE WHERE language_code = 'en'));

INSERT INTO TB_QUESTION(QUESTION, PREFERRED_QUESTION_ORDER, LANGUAGE_ID)
VALUES('Com qual parte do seu ecossistema de dados você está preocupado?', 1, (SELECT ID FROM TB_LANGUAGE WHERE language_code = 'pt'));

-- Suggestions
INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('poor_data_quality.png','Má qualidade dos dados', 'Má qualidade dos dados', 'Dados de má qualidade podem levar a insights imprecisos e má tomada de decisões',
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Com qual área do seu ecossistema de dados você está mais preocupado?'));
	   
INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('compliance_risks.png', 'Riscos de conformidade e segurança', 'Riscos de conformidade e segurança', '.O uso indevido de dados pode levar a problemas legais e danos à reputação',
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosys, ()tem are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('data_silos.png', 'silos de dados', 'silos de dados', 'dados presos em silos departamentais podem ser inacessíveis a outros departamentos',
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Com qual área do seu ecossistema de dados você está mais preocupado?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('lack_of_skilled_personnel.png', 'Falta de pessoal qualificado', '.Falta de pessoal qualificado', 'Falta de habilidades em ciência de dados, análise, inteligência artificial e ML pode dificultar o uso eficaz dos dados.',
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Com qual área do seu ecossistema de dados você está mais preocupado?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('data_overload.png', 'Data Overload', 'Data Overload', '"Data Overload" pode retardar processos e dificultar a determinação de quais dados são realmente úteis',
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Com qual área do seu ecossistema de dados você está mais preocupado?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('cost_and_complexity.png', 'Custo e complexidade', 'Custo e complexidade', 'Uma infraestrutura robusta de análise de dados requer um investimento significativo em recursos',
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Com qual área do seu ecossistema de dados você está mais preocupado?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('inconsistent_data_strategies.png', 'estratégias de dados inconsistentes', 'estratégias de dados inconsistentes', '.Estas são difíceis de conciliar com conceitos modernos, como estruturas de dados, redes e inteligência artificial',
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Com qual área do seu ecossistema de dados você está mais preocupado?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('resistence_to_change.png', 'Resistência às mudanças', 'Resistência às mudanças', 'Os funcionários devem se adaptar às novas formas de trabalhar para que a transformação baseada em dados possa ocorrer',
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Com qual área do seu ecossistema de dados você está mais preocupado?'));


INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('document-related-issues.jpg','Processo de pedido de asilo', 'Processo de pedido de asilo', 'Estou interessado em saber mais sobre o processo de pedido de asilo',
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Com qual área do seu ecossistema de dados você está mais preocupado?'));
