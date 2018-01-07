DROP PROCEDURE IF EXISTS `insertrecord`;

CREATE PROCEDURE `insertrecord` (
in name varchar(20), 
in date varchar(40), 
in place varchar(40), 
in brief varchar(50),
in detail varchar(255),
in id varchar(20)
)BEGIN
DECLARE foundandlostplace varchar(40);
SELECT 招领处地点 FROM 失物招领处 WHERE 账号 = id INTO foundandlostplace;
INSERT INTO 失物信息(物品名称, 拾到时间, 拾到地点, 简要描述, 详细描述, 招领处地点) VALUES(name, date, place, brief, detail, foundandlostplace);
END;

