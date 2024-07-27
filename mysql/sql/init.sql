USE mysql;
CREATE DATABASE IF NOT EXISTS order_db;

USE order_db;
CREATE TABLE IF NOT EXISTS order_table (
    OrderID INT PRIMARY KEY,
    OrderDate DATETIME,
    ProductId VARCHAR(255),
    ProductName VARCHAR(255),
    Quantity DECIMAL(10,2),
    Unit VARCHAR(255)
);