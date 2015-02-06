SELECT
'machine' AS machine,
USER.username AS subject,
SURVEYANSWER.question AS 'stim',
DATE(SURVEYANSWER.start_time) AS block,
DATETIME(SURVEYANSWER.start_time) AS start_time,
DATETIME(SURVEYANSWER.end_time) AS end_time,
0 AS cond,
SURVEYANSWER.answer AS event

FROM data_store_surveyanswer AS SURVEYANSWER

LEFT JOIN data_store_viewer AS VIEWER
ON SURVEYANSWER.subject_id = VIEWER.id

LEFT JOIN auth_user AS USER
ON VIEWER.user_id = USER.id

WHERE

--Train winning
--(username = 'kkchang' OR username = 'yuerany')
--AND start_time BETWEEN '2014-10-06 04:17:45' AND '2014-10-06 05:00:00'

--Train winning
username = 'kkchang'
AND start_time BETWEEN '2014-10-10 00:49:00' AND '2014-10-10 01:00:01'

ORDER BY machine, subject, start_time
;
