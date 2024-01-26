
CREATE DATABASE IF NOT EXISTS llama;
USE DATABASE llama;

CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

USE SCHEMA llama.bronze;

CREATE TABLE IF NOT EXISTS bronze.fmp_income_statements (
    symbol VARCHAR,
    calendar_year VARCHAR,
    period VARCHAR,
    accepted_datetime VARCHAR,
    statement VARCHAR
);
CREATE TABLE IF NOT EXISTS bronze.fmp_balance_sheet_statements (
    symbol VARCHAR,
    calendar_year VARCHAR,
    period VARCHAR,
    accepted_datetime VARCHAR,
    statement VARCHAR
);
CREATE TABLE IF NOT EXISTS bronze.fmp_cash_flow_statements (
    symbol VARCHAR,
    calendar_year VARCHAR,
    period VARCHAR,
    accepted_datetime VARCHAR,
    statement VARCHAR
);

CREATE TABLE IF NOT EXISTS silver.fundamentals (
    symbol VARCHAR,
    statement_year VARCHAR,
    statement_period VARCHAR,
    statement_date VARCHAR,
    revenue FLOAT,
    net_income FLOAT,
    cash_and_cash_equivalents FLOAT,
    total_debt FLOAT,
    dividends_paid FLOAT,
    free_cash_flow FLOAT
);
