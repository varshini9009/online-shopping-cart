--- create database---
create database shopping_db;

--- use database---
use shopping_db;

--- create tables---
create table stock
(product_id int auto_increment primary key,
product_name varchar(100)unique,
product_quantity int,
price float);

create table cart
(cart_id int auto_increment primary key,
product_name varchar(100),
product_quantity int,
foreign key(product_name)references stock(product_name));

