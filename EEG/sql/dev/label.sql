SELECT

'machine' AS machine,
USER.username AS subject,
DATETIME(TAG.start_time) AS start_time,
DATETIME(TAG.end_time) AS end_time,
LABELTYPE.name AS label_type,
LABEL.true AS Y,
LABEL.predicted AS eY

FROM data_store_label AS LABEL

LEFT JOIN data_store_labeltype AS LABELTYPE
ON LABEL.label_type_id = LABELTYPE.id

LEFT JOIN data_store_tag AS TAG
ON LABEL.tag_id = TAG.id

LEFT JOIN data_store_viewer AS VIEWER
ON TAG.subject_id = VIEWER.id

LEFT JOIN auth_user AS USER
ON VIEWER.user_id = USER.id
;
