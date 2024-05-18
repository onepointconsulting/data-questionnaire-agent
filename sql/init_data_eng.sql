
-- Initial question
INSERT INTO TB_QUESTION(QUESTION, PREFERRED_QUESTION_ORDER)
VALUES('Com qual área do seu ecossistema de dados você está mais preocupado?', 1);

-- Suggestions
INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('poor_data_quality.png', 'Má qualidade dos dados', 'Má qualidade dos dados', 'Dados de baixa qualidade podem levar a insights incorretos e má tomada de decisões.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Com qual área do seu ecossistema de dados você está mais preocupado?'));
	   
INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('compliance_risks.png', 'Riscos de conformidade e segurança', 'Riscos de conformidade e segurança', 'O manuseio incorreto de dados pode levar a problemas legais e danos à reputação.',
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Com qual área do seu ecossistema de dados você está mais preocupado?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('data_silos.png', 'Banco de dados', 'Banco de dados', 'Dados presos em silos departamentais podem ser inacessíveis para outras partes.',
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Com qual área do seu ecossistema de dados você está mais preocupado?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('lack_of_skilled_personnel.png', 'Falta de pessoal qualificado', 'Falta de pessoal qualificado', 'Habilidades ausentes em ciência de dados, análise, IA e ML podem impedir o uso eficaz dos dados.',	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Com qual área do seu ecossistema de dados você está mais preocupado?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
VALUES('data_overload.png', 'Sobrecarga de dados', 'Sobrecarga de dados', '"Excesso de dados" pode retardar processos e dificultar a identificação de quais dados são realmente úteis.',
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Com qual área do seu ecossistema de dados você está mais preocupado?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('cost_and_complexity.png', 'Custo e complexidade', 'Custo e complexidade', 'Uma infraestrutura robusta de análise de dados requer um investimento significativo de recursos.',
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Com qual área do seu ecossistema de dados você está mais preocupado?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('inconsistent_data_strategies.png', 'Estratégias de dados inconsistentes', 'Estratégias de dados inconsistentes', 'Difícil de alinhar com conceitos modernos como Data Fabric, Mesh e IA generativa.',
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Com qual área do seu ecossistema de dados você está mais preocupado?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('resistence_to_change.png', 'Resistência à mudança', 'Resistência à mudança', 'Os funcionários precisam se adaptar a novas formas de operar para fazer a transformação baseada em dados funcionar.',
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Com qual área do seu ecossistema de dados você está mais preocupado?'));