drop function if exists ThingNum;

create function ThingNum(name varchar(20))
returns SMALLINT
begin
declare a SMALLINT UNSIGNED DEFAULT 0;
select COUNT(��Ʒ����) from ʧ����Ϣ where ��Ʒ���� = name into a;
return a;
end;

 