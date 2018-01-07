DROP PROCEDURE IF EXISTS `insertuser`;

CREATE PROCEDURE `insertuser` (
in userid varchar(20), 
in userpass varchar(20), 
in userpremission int, 
in username varchar(40)
)BEGIN
INSERT INTO 账户 VALUES(userid, userpass, userpremission);
IF userpremission = 1
THEN
INSERT INTO 普通用户 VALUES(username, userid);
ELSE
INSERT INTO 失物招领处 VALUES(username, userid);	
END IF;
END;

