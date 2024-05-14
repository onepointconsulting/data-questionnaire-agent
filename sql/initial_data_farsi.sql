-- Add language
INSERT INTO public.tb_language(language_code) VALUES ('en');

-- Initial question

INSERT INTO TB_QUESTION(QUESTION, PREFERRED_QUESTION_ORDER, LANGUAGE_ID)
VALUES('شما نگران کدام بخش از اکوسیستم داده‌های خود هستید؟', 1, (SELECT ID FROM TB_LANGUAGE WHERE language_code = 'fa'));

-- Initial question
INSERT INTO TB_QUESTION(QUESTION, PREFERRED_QUESTION_ORDER)
VALUES('با چه چالش هایی به عنوان یک پناهنده در حال حاضر روبرو هستید؟', 1);

-- Suggestions
INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('document-related-issues.jpg', 'مشکلات مربوط به مدارک', 'مشکلات مربوط به مدارک', 'با مدارک قانونی یا شناسایی خود مشکل دارم.',
	(SELECT ID FROM TB_QUESTION WHERE QUESTION = 'با چه چالش هایی به عنوان یک پناهنده در حال حاضر روبرو هستید؟'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('family-separation.jpg', 'جدایی از خانواده', 'جدایی از خانواده', 'با اعضای خانواده ارتباط خود را از دست داده ام یا در reunir شدن با آنها با مشکل روبرو هستم.',(SELECT ID FROM TB_QUESTION WHERE QUESTION = 'با چه چالش هایی به عنوان یک پناهنده در حال حاضر روبرو هستید؟'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('healthcare-access.jpg', 'دسترسی به خدمات درمانی', 'دسترسی به خدمات درمانی', 'به کمک پزشکی نیاز دارم یا در مورد دسترسی به خدمات بهداشتی درمانی نگرانی دارم.',(SELECT ID FROM TB_QUESTION WHERE QUESTION = 'با چه چالش هایی به عنوان یک پناهنده در حال حاضر روبرو هستید؟'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('safety-and-harassment.jpg', 'امنیت و آزار و اذیت', 'امنیت و آزار و اذیت', 'در حال حاضر مورد آزار و اذیت قرار گرفته ام یا احساس ناامنی می کنم.',(SELECT ID FROM TB_QUESTION WHERE QUESTION = 'با چه چالش هایی به عنوان یک پناهنده در حال حاضر روبرو هستید؟'));

-- Additional Topics
INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
VALUES('language-barriers.jpg', 'موانع زبانی', 'موانع زبانی', 'در برقراری ارتباط یا درک زبان محلی با مشکل روبرو هستم.', (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'با چه چالش هایی به عنوان یک پناهنده در حال حاضر روبرو هستید؟'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
VALUES('employment-opportunities.jpg', 'فرصت های شغلی', 'فرصت های شغلی', 'برای یافتن فرصت های شغلی با مشکل روبرو هستم یا با موانعی برای اشتغال روبرو هستم.', (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'با چه چالش هایی به عنوان یک پناهنده در حال حاضر روبرو هستید؟'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
VALUES('housing-difficulties.jpg', 'مشکلات مسکن', 'مشکلات مسکن', 'در یافتن مسکن مناسب با مشکل روبرو هستم.', (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'با چه چالش هایی به عنوان یک پناهنده در حال حاضر روبرو هستید؟'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
VALUES('legal-assistance-needs.jpg', 'حمایت حقوقی', 'حمایت حقوقی', 'به حمایت حقوقی یا مشاوره در مورد مسائل مهاجرت و پناهندگی نیاز دارم.', (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'با چه چالش هایی به عنوان یک پناهنده در حال حاضر روبرو هستید؟'));
