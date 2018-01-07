
SET FOREIGN_KEY_CHECKS=0;


DROP TABLE IF EXISTS `失物招领处`;
Create Table `失物招领处`
(`招领处地点` varchar(40) PRIMARY KEY,
`账号` varchar(20),
FOREIGN KEY(账号) REFERENCES 账户(账号),
UNIQUE INDEX (`账号`)
)ENGINE=InnoDB DEFAULT CHARACTER SET gb2312;

INSERT INTO 失物招领处 VALUES ('校内3号学生公寓', 'place1');
INSERT INTO 失物招领处 VALUES ('校内7号学生公寓', 'place2');
INSERT INTO 失物招领处 VALUES ('合一食堂3楼', 'place3');
INSERT INTO 失物招领处 VALUES ('学二食堂', 'place4');