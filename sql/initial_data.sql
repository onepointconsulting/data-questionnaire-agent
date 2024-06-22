-- Add language
INSERT INTO public.tb_language(language_code) VALUES ('fa');

-- update TB_QUESTION_SUGGESTIONS set main_text = 'Ich benötige medizinische Hilfe oder habe Bedenken hinsichtlich des Zugangs zu Gesundheitsdiensten.' where id = 16 

-- Initial question
INSERT INTO TB_QUESTION(QUESTION, PREFERRED_QUESTION_ORDER, LANGUAGE_ID)
VALUES('بیشتر نگران کدام ناحیه از اکوسیستم داده خود هستید؟', 1, (SELECT ID FROM TB_LANGUAGE WHERE language_code = 'en'));

INSERT INTO TB_QUESTION(QUESTION, PREFERRED_QUESTION_ORDER, LANGUAGE_ID)
VALUES('شما نگران کدام بخش از اکوسیستم داده‌های خود هستید؟', 1, (SELECT ID FROM TB_LANGUAGE WHERE language_code = 'fa'));

-- Suggestions
INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('poor_data_quality.png', 'کیفیت داده ضعیف', 'کیفیت داده ضعیف', '.داده های با کیفیت پایین می تواند منجر به بینش نادرست و تصمیم گیری ضعیف شود', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'بیشتر نگران کدام ناحیه از اکوسیستم داده خود هستید؟'));
	   
INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('compliance_risks.png', 'انطباق و خطرات امنیتی', 'انطباق و خطرات امنیتی', '.سوء استفاده از داده ها می تواند منجر به مشکلات قانونی و آسیب به اعتبار شود', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'Which area of your data ecosys, ()tem are you most concerned about?'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('data_silos.png', 'سیلوهای داده', 'سیلوهای داده', '.داده های به دام افتاده در سیلوهای دپارتمان می تواند برای سایر قسمت ها غیرقابل دسترسی باشد', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'بیشتر نگران کدام ناحیه از اکوسیستم داده خود هستید؟'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('lack_of_skilled_personnel.png', 'کمبود پرسنل ماهر', '.کمبود پرسنل ماهر', 'فقدان مهارت در علم داده، تجزیه و تحلیل، هوش مصنوعی و ML می تواند مانع استفاده موثر از داده ها شود.', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'بیشتر نگران کدام ناحیه از اکوسیستم داده خود هستید؟'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('data_overload.png', 'اضافه بار داده ها', 'اضافه بار داده ها', '."افزایش داده ها" می تواند فرآیندها را کند کند و تشخیص اینکه چه داده هایی واقعا مفید هستند را دشوار می کند', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'بیشتر نگران کدام ناحیه از اکوسیستم داده خود هستید؟'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('cost_and_complexity.png', 'هزینه و پیچیدگی', 'هزینه و پیچیدگی', '.یک زیرساخت قوی تجزیه و تحلیل داده ها به سرمایه گذاری قابل توجهی در منابع نیاز دارد', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'بیشتر نگران کدام ناحیه از اکوسیستم داده خود هستید؟'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('inconsistent_data_strategies.png', 'استراتژی های داده ناسازگار', 'استراتژی های داده ناسازگار', '.این موارد سخت است که با مفاهیم مدرن مانند ساختار داده، شبکه و هوش مصنوعی تولیدی هماهنگ شوند', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'بیشتر نگران کدام ناحیه از اکوسیستم داده خود هستید؟'));

INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('resistence_to_change.png', 'مقاومت در برابر تغییرات', 'مقاومت در برابر تغییرات', '.کارمندان باید خود را با روش‌های جدید کار تطبیق دهند تا تحول مبتنی بر داده‌ها عملی شود', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'بیشتر نگران کدام ناحیه از اکوسیستم داده خود هستید؟'));


INSERT INTO TB_QUESTION_SUGGESTIONS(IMG_SRC, IMG_ALT, TITLE, MAIN_TEXT, QUESTION_ID)
	VALUES('document-related-issues.jpg', 'مراحل درخواست پناهندگی', 'مراحل درخواست پناهندگی', 'من علاقه مند هستم در مورد روش درخواست پناهندگی بیشتر بدانم', 
	   (SELECT ID FROM TB_QUESTION WHERE QUESTION = 'بیشتر نگران کدام ناحیه از اکوسیستم داده خود هستید؟'));
