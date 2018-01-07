drop function if exists DateNum;

create function DateNum(date varchar(40))
returns SMALLINT
begin
declare a SMALLINT UNSIGNED DEFAULT 0;
select COUNT(拾到时间) from 失物信息 where 拾到时间 = date into a;
return a;
end;

 