SELECT
VIDEOCONTENT.video_url AS url,
CONTENT.name AS name

FROM data_store_content AS CONTENT

LEFT JOIN data_store_videocontent AS VIDEOCONTENT
ON CONTENT.id = VIDEOCONTENT.content_ptr_id

WHERE CONTENT.name LIKE 'TrailerDrug%'
;
