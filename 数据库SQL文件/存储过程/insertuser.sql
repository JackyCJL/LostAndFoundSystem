DROP PROCEDURE IF EXISTS `insertuser`;

CREATE PROCEDURE `insertuser` (
in userid varchar(20), 
in userpass varchar(20), 
in userpremission int, 
in username varchar(40)
)BEGIN
INSERT INTO �˻� VALUES(userid, userpass, userpremission);
IF userpremission = 1
THEN
INSERT INTO ��ͨ�û� VALUES(username, userid);
ELSE
INSERT INTO ʧ�����촦 VALUES(username, userid);	
END IF;
END;

