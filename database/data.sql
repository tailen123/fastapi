
drop table message_table；
create TABLE IF NOT EXISTS message_table(
id INT PRIMARY KEY AUTO_INCREMENT,
dialog_id INT,
text TEXT(65000),
text_zh TEXT(65000),
created_at VARCHAR (255),
stage INT,
from_user BOOLEAN,
reason VARCHAR(255),
reason_type VARCHAR(255),
is_del BOOLEAN,
message_id INT) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

drop table result_table；
create TABLE IF NOT EXISTS result_table(
id INT PRIMARY KEY ,
message_id INT,
text TEXT(65000),
text_zh TEXT(65000),
score INT,
source VARCHAR(255),
group_id INT,
batch_id INT,
prompt_name TEXT(65000),
prompt TEXT(65000),
is_del BOOLEAN,
result_id INT) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE VIEW acc_view AS
SELECT
    message_id,
    source,
    SUM(case when score=0 Then 1 else 0 end) as todonums,
    SUM(CASE WHEN score = 1 THEN 1 ELSE 0 END) AS onenums,
    SUM(CASE When score=2 Then 1 else 0 end) as twonums,
    COUNT(*) AS total
FROM result_table
GROUP BY message_id, source;

