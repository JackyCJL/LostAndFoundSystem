drop function if exists DateNum;

create function DateNum(date varchar(40))
returns SMALLINT
begin
declare a SMALLINT UNSIGNED DEFAULT 0;
select COUNT(ʰ��ʱ��) from ʧ����Ϣ where ʰ��ʱ�� = date into a;
return a;
end;

 