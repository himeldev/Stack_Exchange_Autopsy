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


COPY (SELECT site, FLOOR(EXTRACT(DAY FROM posts.creation_date - first_posts.first_creation_date)/30)+1 AS month_id, 

owner_user_id AS user_id, COUNT(*) AS answer_count

FROM (posts NATURAL JOIN (SELECT site, MIN(creation_date) AS first_creation_date FROM posts GROUP BY site) AS first_posts)

WHERE post_type_id = 2 AND owner_user_id IS NOT NULL AND owner_user_id <> -1

GROUP BY site, month_id, user_id ORDER BY site, month_id, answer_count DESC) 

TO 'C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Growth_Model/Contribution_of_Top_Answerers.csv' WITH CSV

COPY (SELECT site, FLOOR(EXTRACT(DAY FROM posts.creation_date - first_posts.first_creation_date)/30)+1 AS month_id, 

owner_user_id AS user_id, COUNT(*) AS question_count

FROM (posts NATURAL JOIN (SELECT site, MIN(creation_date) AS first_creation_date FROM posts GROUP BY site) AS first_posts)

WHERE post_type_id = 1 AND owner_user_id IS NOT NULL AND owner_user_id <> -1

GROUP BY site, month_id, user_id ORDER BY site, month_id, question_count DESC) 

TO 'C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Growth_Model/Contribution_of_Top_Askers.csv' WITH CSV

COPY (SELECT site, FLOOR(EXTRACT(DAY FROM posts.creation_date - first_posts.first_creation_date)/30)+1 AS month_id, 

parent_id AS question_id, COUNT(*) AS answer_count

FROM (posts NATURAL JOIN (SELECT site, MIN(creation_date) AS first_creation_date FROM posts GROUP BY site) AS first_posts)

WHERE post_type_id = 2 AND parent_id IS NOT NULL AND parent_id <> -1

GROUP BY site, month_id, question_id ORDER BY site, month_id, answer_count DESC) 

TO 'C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Growth_Model/Contribution_of_Top_Questions.csv' WITH CSV


COPY (SELECT site, owner_user_id AS user_id, 

FLOOR(EXTRACT(DAY FROM posts.creation_date - first_posts.first_creation_date)/30)+1 AS month_id, COUNT(*) AS answer_count

FROM (posts NATURAL JOIN (SELECT site, MIN(creation_date) AS first_creation_date FROM posts GROUP BY site) AS first_posts)

WHERE post_type_id = 2 AND owner_user_id IS NOT NULL AND owner_user_id <> -1

GROUP BY site, month_id, user_id ORDER BY site, user_id, month_id) 

TO 'C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Death_Answerer.csv' WITH CSV


