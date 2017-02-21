/* Temporal action sequence for each user */

SELECT * FROM

((SELECT site, owner_user_id AS user_id, creation_date, post_type_id AS activity_type FROM posts)

UNION 

(SELECT site, user_id, creation_date, 3 AS activity_type FROM comments)) AS R 

WHERE user_id IS NOT NULL AND user_id <> -1

ORDER BY site, user_id, creation_date

/* Temporal action sequence view */

CREATE VIEW temporal_action_sequence AS

(SELECT * FROM

((SELECT site, owner_user_id AS user_id, creation_date, post_type_id AS activity_type FROM posts)

UNION 

(SELECT site, user_id, creation_date, 3 AS activity_type FROM comments)) AS R 

WHERE user_id IS NOT NULL AND user_id <> -1

ORDER BY site, user_id, creation_date)

/* Save temporal action sequence view to file */

COPY (SELECT * FROM temporal_action_sequence) TO 'C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/User_Session/Temporal_Action_Sequence.csv' WITH CSV