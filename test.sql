create table admininfo(
    id varchar(8) not null primary key,
    password char(64) not null,
    register_code varchar(64) not null,
    invite_code varchar(64),
    status int check(status in(0,1))
);