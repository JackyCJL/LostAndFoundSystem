DROP TRIGGER IF EXISTS date_on_message_table_before_insert;

CREATE TRIGGER date_on_message_table_before_insert 
 BEFORE INSERT
 ON ʧ����Ϣ FOR EACH ROW
BEGIN
 IF NEW.ʰ��ʱ�� > curdate() THEN
  SET NEW.ʰ��ʱ�� = curdate();
 END IF;
END;

DROP TRIGGER IF EXISTS date_on_message_table_before_update;

CREATE TRIGGER date_on_message_table_before_update 
 BEFORE UPDATE
 ON ʧ����Ϣ FOR EACH ROW
BEGIN
 IF NEW.ʰ��ʱ�� > curdate() THEN
  SET NEW.ʰ��ʱ�� = curdate();
 END IF;
END;

