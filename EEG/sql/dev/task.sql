SELECT
'machine' AS machine,
USER.username AS subject,
CONTENT.name || '(' || SESSION.content_start_sec || '-' || SESSION.content_end_sec || ')' AS stim,
CONTENT.name AS block,
--DATE(SESSION.start_time) AS block,
DATETIME(SESSION.start_time) AS start_time,
DATETIME(SESSION.end_time) AS end_time,
CASE
WHEN CONTENT.name LIKE 'Rest' THEN 3
WHEN CONTENT.name LIKE '%\_Engage\_%' ESCAPE '\' THEN 2
WHEN CONTENT.name LIKE '%\_Disengage\_%' ESCAPE '\' THEN 1
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

--Train engage (TrailerDrug)
--username = 'kkchang'
--AND start_time BETWEEN '2014-09-29' AND '2014-10-01 01:20:00'

--Train engage (TrailerCalculus)
--username = 'kkchang'
--AND start_time BETWEEN '2014-10-14 03:02:26' AND '2014-10-14 03:30:51'

--Train engage (TrailerCalculus)
--username = 'yuerany'
--AND start_time BETWEEN '2014-10-03 02:46:29' AND '2014-10-03 03:10:06'

--Apply 2hr Godzilla
--(username = 'kkchang' OR username = 'yuerany')
--AND start_time BETWEEN '2014-10-02 02:11:00' AND '2014-10-02 04:08:33'

--Apply DOTA BIC
--username = 'qiwenz'
--AND start_time BETWEEN '2014-10-03 20:02:28' AND '2014-10-03 20:46:46'

--Apply 3min Up
--username = 'kkchang'
--AND start_time BETWEEN '2014-10-11 02:56:27' AND '2014-10-11 02:59:09'

--Apply 15min Godzilla BIC
--(username = 'qiwenz' OR username = 'haodongl' OR username = 'jiacongh')
--AND start_time BETWEEN '2014-10-11 21:17:43' AND '2014-10-11 21:34:56'

--Apply 3hr NFL 2014-10-16 Jets vs Patriots
--(username = 'kkchang' OR username = 'yuerany')
--username = 'kkchang'
--AND (start_time BETWEEN '2014-10-17 00:25:46' AND '2014-10-17 00:26:16'
--OR start_time BETWEEN '2014-10-17 00:26:16' AND '2014-10-17 03:30:35')

--Apply 30min Movie The Lego Movie
--(username = 'qiwenz' OR username = 'haodongl' OR username = 'jiacongh')
--AND (start_time BETWEEN '2014-10-17 17:43:37' AND '2014-10-17 17:44:07'
--OR start_time BETWEEN '2014-10-17 17:44:07' AND '2014-10-17 18:19:11')

--Apply 1hr NFL 2014-10-19 Falcons vs Ravens
--(username = 'kkchang' OR username = 'yuerany')
--AND (start_time BETWEEN '2014-10-19 17:59:26' AND '2014-10-19 17:59:56'
--OR start_time BETWEEN '2014-10-19 17:59:56' AND '2014-10-19 19:08:46')

--Apply 10min NFL 2014-10-19 Giants vs Cowboys
--username = 'kkchang'
--AND (start_time BETWEEN '2014-10-19 22:15:23' AND '2014-10-19 22:15:53'
--OR start_time BETWEEN '2014-10-19 22:15:53' AND '2014-10-19 22:24:25')

--Apply 3hr NFL 2014-10-20 Texans vs Steelers
--username = 'kkchang'
--AND (start_time BETWEEN '2014-10-21 00:31:47' AND '2014-10-21 00:32:17'
--OR start_time BETWEEN '2014-10-21 00:32:17' AND '2014-10-21 03:38:45')

--Apply 3hr NFL 2014-11-09 Jets vs Steelers
username = 'kkchang'
AND (start_time BETWEEN '2014-11-09 17:58:47' AND '2014-11-09 17:59:17'
OR start_time BETWEEN '2014-11-09 17:59:17' AND '2014-11-09 21:01:20')

--start_time BETWEEN '2014-10-31' AND '2014-11-01'

ORDER BY machine, subject, start_time
;
