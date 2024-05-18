
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