/* First post date of Stack Exchange websites */

COPY (SELECT site, MIN(creation_date) AS min_creation_date FROM posts GROUP BY site ORDER BY min_creation_date) 

TO 'C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Site_First_Post_Date.csv' WITH CSV

/* Total number of users in Stack Exchange websites */

COPY (SELECT site, COUNT(*) AS user_count FROM users GROUP BY site ORDER BY user_count DESC) 

TO 'C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Site_Total_User.csv' WITH CSV

/*  Monthly stats for Stack Exchange websites */

/* Result Format: site, month_id, question_count, answer_count, answered_question_count, question_with_accepted_answer_count, asker_count, answerer_count, question_total_score, answer_total_score, avg_time_to_first_answer, comment_count, commenter_count, comment_total_score */

COPY (SELECT * FROM

(SELECT site, FLOOR(EXTRACT(DAY FROM posts.creation_date - first_posts.first_creation_date)/30)+1 AS month_id, 

COUNT(CASE WHEN post_type_id = 1 THEN 1 END) AS question_count, COUNT(CASE WHEN post_type_id = 2 THEN 1 END) AS answer_count,

COUNT(CASE WHEN post_type_id = 1 AND answer_count > 0 THEN 1 END) AS answered_question_count, COUNT(accepted_answer_id) AS question_with_accepted_answer_count,

COUNT(DISTINCT (CASE WHEN post_type_id = 1 THEN owner_user_id END)) AS asker_count, COUNT(DISTINCT (CASE WHEN post_type_id = 2 THEN owner_user_id END)) AS answerer_count, 

SUM(CASE WHEN post_type_id = 1 THEN score END) AS question_total_score, SUM(CASE WHEN post_type_id = 2 THEN score END) AS answer_total_score

FROM (posts NATURAL JOIN (SELECT site, MIN(creation_date) AS first_creation_date FROM posts GROUP BY site) AS first_posts)

GROUP BY site, month_id HAVING COUNT(CASE WHEN post_type_id = 1 THEN 1 END) >= 50) AS R1

NATURAL JOIN

(SELECT site, FLOOR(EXTRACT(DAY FROM posts.creation_date - first_posts.first_creation_date)/30)+1 AS month_id, 

AVG(EXTRACT(MINUTE FROM first_answers.first_answer_date - posts.creation_date)) AS avg_time_to_first_answer

FROM (posts NATURAL JOIN (SELECT site, parent_id AS id, MIN(creation_date) AS first_answer_date FROM posts WHERE post_type_id = 2 GROUP BY site, parent_id) AS first_answers

NATURAL JOIN (SELECT site, MIN(creation_date) AS first_creation_date FROM posts GROUP BY site) AS first_posts)

GROUP BY site, month_id) AS R2

NATURAL JOIN

(SELECT site, FLOOR(EXTRACT(DAY FROM comments.creation_date - first_posts.first_creation_date)/30)+1 AS month_id, 

COUNT(*) AS comment_count, COUNT(DISTINCT user_id) AS commenter_count, SUM(score) AS comment_total_score

FROM (comments NATURAL JOIN (SELECT site, MIN(creation_date) AS first_creation_date FROM posts GROUP BY site) AS first_posts)

GROUP BY site, month_id) AS R3

ORDER BY site, month_id) 

TO 'C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Site_Monthly_Stats.csv' WITH CSV




