
SET FOREIGN_KEY_CHECKS=0;


DROP TABLE IF EXISTS `��ͨ�û�`;
Create Table `��ͨ�û�`
(`�û���` varchar(20) PRIMARY KEY,
`�˺�` varchar(20),
FOREIGN KEY(�˺�) REFERENCES �˻�(�˺�),
UNIQUE INDEX(�˺�)
)ENGINE=InnoDB DEFAULT CHARACTER SET gb2312;

INSERT INTO ��ͨ�û�(�û���,�˺�) VALUES ('������ͨ�û�','testman');
INSERT INTO ��ͨ�û�(�û���,�˺�) VALUES ('����¹','418193459');
INSERT INTO ��ͨ�û�(�û���,�˺�) VALUES ('JackyChen', 'Jacky_CJL');
