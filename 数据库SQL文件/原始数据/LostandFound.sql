
SET FOREIGN_KEY_CHECKS=0;


DROP TABLE IF EXISTS `ʧ�����촦`;
Create Table `ʧ�����촦`
(`���촦�ص�` varchar(40) PRIMARY KEY,
`�˺�` varchar(20),
FOREIGN KEY(�˺�) REFERENCES �˻�(�˺�),
UNIQUE INDEX (`�˺�`)
)ENGINE=InnoDB DEFAULT CHARACTER SET gb2312;

INSERT INTO ʧ�����촦 VALUES ('У��3��ѧ����Ԣ', 'place1');
INSERT INTO ʧ�����촦 VALUES ('У��7��ѧ����Ԣ', 'place2');
INSERT INTO ʧ�����촦 VALUES ('��һʳ��3¥', 'place3');
INSERT INTO ʧ�����촦 VALUES ('ѧ��ʳ��', 'place4');