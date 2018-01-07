
SET FOREIGN_KEY_CHECKS=0;


DROP TABLE IF EXISTS `普通用户`;
Create Table `普通用户`
(`用户名` varchar(20) PRIMARY KEY,
`账号` varchar(20),
FOREIGN KEY(账号) REFERENCES 账户(账号),
UNIQUE INDEX(账号)
)ENGINE=InnoDB DEFAULT CHARACTER SET gb2312;

INSERT INTO 普通用户(用户名,账号) VALUES ('测试普通用户','testman');
INSERT INTO 普通用户(用户名,账号) VALUES ('长颈鹿','418193459');
INSERT INTO 普通用户(用户名,账号) VALUES ('JackyChen', 'Jacky_CJL');
