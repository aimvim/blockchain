create table pkadress(
    pk varchar(150) not null primary key,
    adress varchar(40) not null,
    tx_nonce int not null default 0,
    amount double default 0,
    id varchar(8) not null
);

create table volunteerinfo(
    id varchar(8) not null primary key,
    password char(64) not null
);

create table admininfo(
    id varchar(8) not null primary key,
    password char(64) not null,
    register_code varchar(64) not null,
    invite_code varchar(64),
    status int check(status in(0,1))
);

create table userinfo(
    id varchar(8) not null primary key,
    password char(64) not null,
    register_code varchar(64) not null,
    proof varchar(32) not null,
    checked varchar(3) check(checked in ("yes","not"))
    --proof目前按照一个url处理
);

create table register_code(
    code varchar(64),
    company varchar(32) not null
);

create table mission_published(
    id int auto_increment primary key,
    name varchar(64) not null,
    area varchar(64),
    begintime datetime,
    endtime datetime,
    activitytime float not null,
    award double not null,
    mcharacter varchar(64) check(mcharacter in ("ABCD","EFGH","IJKL","MNOP")),
    details varchar(1000),
    status varchar(16) check(status in ("not finished","finished")) default "not finished",
    checked varchar(3) check(checked in ("not","yes")) default "not",
    uploader varchar(8) not null,
    uploader_company varchar(32) not null
);

create table proof_table(
    name varchar(64),
    area varchar(64),
    proof varchar(64),
    constraint fkk foreign key(name,area)
    references mission_published(name,area)
    on update cascade
);
