
SET FOREIGN_KEY_CHECKS=0;


DROP TABLE IF EXISTS `�˻�`;
Create Table `�˻�`
(`�˺�` varchar(20) PRIMARY KEY,
`����` varchar(20) NOT NULL,
`Ȩ��` int NOT NULL,
UNIQUE INDEX (`�˺�`)
)ENGINE=InnoDB DEFAULT CHARACTER SET gb2312;

INSERT INTO �˻�(�˺�,����,Ȩ��) VALUES ('testman', '123456', '1');
INSERT INTO �˻�(�˺�,����,Ȩ��) VALUES ('418193459', '19960626', '1');
INSERT INTO �˻�(�˺�,����,Ȩ��) VALUES ('place1', '960626', '2');
INSERT INTO �˻�(�˺�,����,Ȩ��) VALUES ('place2', '20171222', '2');
INSERT INTO �˻�(�˺�,����,Ȩ��) VALUES ('place3', 'database', '2');
INSERT INTO �˻�(�˺�,����,Ȩ��) VALUES ('place4', 'Database', '2');
INSERT INTO �˻�(�˺�,����,Ȩ��) VALUES ('Jacky_CJL', 'cjl960626', '1');
