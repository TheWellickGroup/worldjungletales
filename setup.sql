-- SQL SCRIPT TO SETUP A LOCAL DEV ENVIRONMENT
-- RUN THIS ON YOUR POSTGRES INSTANCE WITH psql
-- e.g psql < setup.sql
DROP USER IF EXISTS worldjungletales_user;

CREATE USER worldjungletales_user WITH CREATEDB CREATEROLE SUPERUSER LOGIN PASSWORD 'worldjungletales_pass';

DROP DATABASE IF EXISTS worldjungletales;

CREATE DATABASE worldjungletales WITH OWNER postgres;

GRANT ALL ON DATABASE worldjungletales TO worldjungletales_user;
