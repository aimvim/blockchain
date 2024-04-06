
create table userinfo(
    id varchar(8) not null primary key,
    password char(64) not null,
    register_code varchar(64) not null,
    proof varchar(32) not null,
    checked varchar(3) check(checked in ("yes","not"))
    --proof目前按照一个url处理
);