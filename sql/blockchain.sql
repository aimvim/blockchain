create table pkadress(
    pk varchar(150) not null primary key,
    adress varchar(40) not null,
    tx_nonce int not null default 0,
    amount double default 0
);

create table userinfo(
    id varchar(8) not null primary key,
    password char(64) not null
);

create table admininfo(
    id varchar(8) not null primary key,
    password char(64) not null
);

create table volunteerinfo(
    id varchar(8) not null primary key,
    password char(64) not null
);

create table register_code(
    code varchar(64)
);