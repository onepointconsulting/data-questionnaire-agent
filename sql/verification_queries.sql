select min(ordinal), max(ordinal), session_id, question, min(created_at), max(created_at) from
    (select ROW_NUMBER() OVER (PARTITION BY session_id ORDER BY created_at) ordinal, session_id, question, created_at 
        from tb_questionnaire_status
        where session_id in (select distinct session_id from tb_questionnaire_status where final_report is true)) q
group by session_id, question having count(*) > 1 order by min(created_at);

-- Check duplicate questions
select lower(question), count(*) from tb_questionnaire_status where session_id = '01JD748MW7FKMZ2FY5H87WWQ8B' 
group by lower(question) having count(*) > 1;

-- Select all questions in session
select question from tb_questionnaire_status where session_id = '01JD748MW7FKMZ2FY5H87WWQ8B';