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
SELECT ���촦�ص� FROM ʧ�����촦 WHERE �˺� = id INTO foundandlostplace;
INSERT INTO ʧ����Ϣ(��Ʒ����, ʰ��ʱ��, ʰ���ص�, ��Ҫ����, ��ϸ����, ���촦�ص�) VALUES(name, date, place, brief, detail, foundandlostplace);
END;

