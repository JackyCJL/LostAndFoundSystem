DROP PROCEDURE IF EXISTS `updaterecord`;

CREATE PROCEDURE `updaterecord` (
in ind int,
in name varchar(20), 
in date varchar(40), 
in place varchar(40), 
in brief varchar(50),
in detail varchar(255)
)BEGIN
UPDATE ʧ����Ϣ SET ��Ʒ���� = name, ʰ��ʱ�� = date, ʰ���ص� = place, ��Ҫ���� = brief, ��ϸ���� = detail WHERE ʧ���� = ind;
END;

