SELECT
'machine' AS machine,
USER.username AS subject,
CONCAT(CONTENT.name, '(', SESSION.content_start_sec, '-', SESSION.content_end_sec, ')') AS stim,
DATE(SESSION.start_time) AS block,
SESSION.start_time AS start_time,
SESSION.end_time AS end_time,
CASE
WHEN CONTENT.name LIKE 'Rest' THEN 3
WHEN CONTENT.name LIKE '%\_Engage\_%' THEN 2
WHEN CONTENT.name LIKE '%\_Disengage\_%' THEN 1
ELSE 0
END AS cond,
-1 AS score

FROM data_store_session AS SESSION

LEFT JOIN data_store_session_viewers AS SESSION_VIEWER
ON SESSION.id = SESSION_VIEWER.session_id

LEFT JOIN data_store_viewer AS VIEWER
ON SESSION_VIEWER.viewer_id = VIEWER.id

LEFT JOIN auth_user AS USER
ON VIEWER.user_id = USER.id

LEFT JOIN data_store_content AS CONTENT
ON SESSION.content_id = CONTENT.id

WHERE

USER.username = 'kkchang'
AND SESSION.start_time BETWEEN '2014-09-26 19:44:00' AND '2014-09-30'

ORDER BY machine, subject, start_time
;
