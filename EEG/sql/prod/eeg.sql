SELECT
'machine' AS machine,
USER.username AS subject,
'muse' AS sensor,
RAW.sensor AS location,
RAW.start_time AS start_time,
RAW.end_time AS end_time,
RAW.rawwave AS rawwave

FROM data_store_raw AS RAW

LEFT JOIN data_store_viewer AS VIEWER
ON RAW.subject_id = VIEWER.id

LEFT JOIN auth_user AS USER
ON VIEWER.user_id = USER.id

WHERE

RAW.start_time BETWEEN '2014-09-26 19:44:00' AND '2014-09-30'
;
