drop function if exists Id2Name;

create function Id2Name(id varchar(20))
returns varchar(40)
begin
declare a SMALLINT UNSIGNED DEFAULT 0;
declare name varchar(40);
select Ȩ�� from �˻� where �˺� = id into a;
IF a = 1
THEN
select �û��� from ��ͨ�û� where �˺� = id into name;
ELSE
select ���촦�ص� from ʧ�����촦 where �˺� = id into name;	
END IF;
return name;
end;

 