-- Extract the content of specific sessions
select final_report, session_id, question, answer from tb_questionnaire_status where session_id in
(select distinct c.session_id from tb_session_configuration c inner join tb_questionnaire_status s on s.session_id = c.session_id
where c.config_key = 'session-client-id' 
and c.config_value in ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpEMkpXTkhBNTZGN1lHRENDU1czRjJaQiIsIm5hbWUiOiJHaWwiLCJpYXQiOjE3MzIwMzI0ODR9.r8LTAiuORLPk2QnrS8YMcX7dHdlYKndHuXc3PEY6Msw')
and s.final_report = true)
order by id asc;