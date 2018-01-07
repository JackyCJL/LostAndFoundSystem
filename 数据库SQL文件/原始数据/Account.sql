
SET FOREIGN_KEY_CHECKS=0;


DROP TABLE IF EXISTS `账户`;
Create Table `账户`
(`账号` varchar(20) PRIMARY KEY,
`密码` varchar(20) NOT NULL,
`权限` int NOT NULL,
UNIQUE INDEX (`账号`)
)ENGINE=InnoDB DEFAULT CHARACTER SET gb2312;

INSERT INTO 账户(账号,密码,权限) VALUES ('testman', '123456', '1');
INSERT INTO 账户(账号,密码,权限) VALUES ('418193459', '19960626', '1');
INSERT INTO 账户(账号,密码,权限) VALUES ('place1', '960626', '2');
INSERT INTO 账户(账号,密码,权限) VALUES ('place2', '20171222', '2');
INSERT INTO 账户(账号,密码,权限) VALUES ('place3', 'database', '2');
INSERT INTO 账户(账号,密码,权限) VALUES ('place4', 'Database', '2');
INSERT INTO 账户(账号,密码,权限) VALUES ('Jacky_CJL', 'cjl960626', '1');
