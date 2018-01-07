DROP PROCEDURE IF EXISTS `updaterecord`;

CREATE PROCEDURE `updaterecord` (
in ind int,
in name varchar(20), 
in date varchar(40), 
in place varchar(40), 
in brief varchar(50),
in detail varchar(255)
)BEGIN
UPDATE 失物信息 SET 物品名称 = name, 拾到时间 = date, 拾到地点 = place, 简要描述 = brief, 详细描述 = detail WHERE 失物编号 = ind;
END;

