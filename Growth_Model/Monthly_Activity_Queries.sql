/* Monthly question answer activity in Stack Exchange websites */

SELECT site, FLOOR(EXTRACT(DAY FROM posts.creation_date - first_posts.first_creation_date)/30)+1 AS month_id, 

COUNT(CASE WHEN post_type_id = 1 THEN 1 END) AS question_count, COUNT(CASE WHEN post_type_id = 2 THEN 1 END) AS answer_count,

COUNT(DISTINCT (CASE WHEN post_type_id = 1 THEN owner_user_id END)) AS asker_count, COUNT(DISTINCT (CASE WHEN post_type_id = 2 THEN owner_user_id END)) AS answerer_count, 

SUM(CASE WHEN post_type_id = 1 THEN score END) AS question_total_score, SUM(CASE WHEN post_type_id = 2 THEN score END) AS answer_total_score

FROM (posts NATURAL JOIN (SELECT site, MIN(creation_date) AS first_creation_date FROM posts GROUP BY site) AS first_posts)

GROUP BY site, month_id HAVING COUNT(CASE WHEN post_type_id = 1 THEN 1 END) >= 50 ORDER BY site, month_id

/* Save monthly question answer activity in Stack Exchange websites to file */

COPY (SELECT site, FLOOR(EXTRACT(DAY FROM posts.creation_date - first_posts.first_creation_date)/30)+1 AS month_id, 

COUNT(CASE WHEN post_type_id = 1 THEN 1 END) AS question_count, COUNT(CASE WHEN post_type_id = 2 THEN 1 END) AS answer_count,

COUNT(DISTINCT (CASE WHEN post_type_id = 1 THEN owner_user_id END)) AS asker_count, COUNT(DISTINCT (CASE WHEN post_type_id = 2 THEN owner_user_id END)) AS answerer_count, 

SUM(CASE WHEN post_type_id = 1 THEN score END) AS question_total_score, SUM(CASE WHEN post_type_id = 2 THEN score END) AS answer_total_score

FROM (posts NATURAL JOIN (SELECT site, MIN(creation_date) AS first_creation_date FROM posts GROUP BY site) AS first_posts)

GROUP BY site, month_id HAVING COUNT(CASE WHEN post_type_id = 1 THEN 1 END) >= 50 ORDER BY site, month_id) 

TO 'C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Growth_Model/Monthly_QA_Activity.csv' WITH CSV