drop function if exists ThingNum;

create function ThingNum(name varchar(20))
returns SMALLINT
begin
declare a SMALLINT UNSIGNED DEFAULT 0;
select COUNT(物品名称) from 失物信息 where 物品名称 = name into a;
return a;
end;

 