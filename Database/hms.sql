create database hms;

USE hms;

CREATE TABLE user_login (
    id VARCHAR(100)  PRIMARY KEY NOT NULL ,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL
);
drop table user_login;


INSERT INTO user_login (id, username, password)
VALUES ('1', 'zahid', 'zahid');

CREATE TABLE doctor_record (
    id VARCHAR(100) primary key NOT NULL,
    DoctorName TEXT(100) NOT NULL,
    Specialization TEXT(100) NOT NULL
);
SELECT * FROM doctor_record WHERE id = '01';

drop table doctor_record;

select * from doctor_record;

CREATE TABLE patient_record (
    id VARCHAR(50) primary key NOT NULL,
    Name VARCHAR(100) NOT NULL,
    Disease VARCHAR(100) NOT NULL,
    Date VARCHAR(30) NOT NULL
);
select * from patient_record;

drop table patient_record;
