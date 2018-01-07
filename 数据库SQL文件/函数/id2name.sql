drop function if exists Id2Name;

create function Id2Name(id varchar(20))
returns varchar(40)
begin
declare a SMALLINT UNSIGNED DEFAULT 0;
declare name varchar(40);
select 权限 from 账户 where 账号 = id into a;
IF a = 1
THEN
select 用户名 from 普通用户 where 账号 = id into name;
ELSE
select 招领处地点 from 失物招领处 where 账号 = id into name;	
END IF;
return name;
end;

 