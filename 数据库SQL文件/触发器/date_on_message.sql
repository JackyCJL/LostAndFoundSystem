DROP TRIGGER IF EXISTS date_on_message_table_before_insert;

CREATE TRIGGER date_on_message_table_before_insert 
 BEFORE INSERT
 ON 失物信息 FOR EACH ROW
BEGIN
 IF NEW.拾到时间 > curdate() THEN
  SET NEW.拾到时间 = curdate();
 END IF;
END;

DROP TRIGGER IF EXISTS date_on_message_table_before_update;

CREATE TRIGGER date_on_message_table_before_update 
 BEFORE UPDATE
 ON 失物信息 FOR EACH ROW
BEGIN
 IF NEW.拾到时间 > curdate() THEN
  SET NEW.拾到时间 = curdate();
 END IF;
END;

