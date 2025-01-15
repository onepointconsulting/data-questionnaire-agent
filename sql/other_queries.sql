-- Extract the content of specific sessions
select final_report, session_id, question, answer from tb_questionnaire_status where session_id in
(select distinct c.session_id from tb_session_configuration c inner join tb_questionnaire_status s on s.session_id = c.session_id
where c.config_key = 'session-client-id' 
and c.config_value in ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpEMkpXTkhBNTZGN1lHRENDU1czRjJaQiIsIm5hbWUiOiJHaWwiLCJpYXQiOjE3MzIwMzI0ODR9.r8LTAiuORLPk2QnrS8YMcX7dHdlYKndHuXc3PEY6Msw')
and s.final_report = true)
order by id asc;

-- Get some statistics on sessions
select * from
(select t.email, sc.session_id, count(*), min(created_at), max(created_at) from tb_session_configuration sc
inner join tb_jwt_token t on sc.config_value = t.jwt_token
inner join tb_questionnaire_status qs on qs.session_id = sc.session_id
where t.id > 100
group by sc.session_id, t.email 
order by count(*)) q where max > '2025-01-15';