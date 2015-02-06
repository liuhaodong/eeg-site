SELECT
--'machine' AS machine,
DATE(RAW.start_time) AS date,
--USER.username AS subject,
--RAW.sensor AS sensor,
COUNT(*) / 60 AS num_min

FROM data_store_raw AS RAW

LEFT JOIN data_store_viewer AS VIEWER
ON RAW.subject_id = VIEWER.id

LEFT JOIN auth_user AS USER
ON VIEWER.user_id = USER.id

--WHERE

--start_time > DATETIME('now', '-12 hours')

--GROUP BY date, subject
--ORDER BY date, subject

GROUP BY date
ORDER BY date
;
