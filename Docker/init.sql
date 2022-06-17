CREATE USER postgres;
CREATE DATABASE fabrique;
ALTER ROLE fabrique SET client_encoding TO 'utf8';
ALTER ROLE fabrique SET default_transaction_isolation TO 'read committed';
ALTER ROLE fabrique SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE fabrique TO postsgres;
