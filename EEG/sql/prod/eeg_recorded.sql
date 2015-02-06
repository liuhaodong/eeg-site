SELECT
'machine' AS machine,
USER.username AS subject,
DATE(RAW.start_time) AS date,
COUNT(*) AS num_sec

FROM data_store_raw AS RAW

LEFT JOIN data_store_viewer AS VIEWER
ON RAW.subject_id = VIEWER.id

LEFT JOIN auth_user AS USER
ON VIEWER.user_id = USER.id

WHERE

RAW.start_time BETWEEN '2014-09-26 19:44:00' AND '2014-09-30'

GROUP BY machine, subject, date
;
