## SQL, Models, and Migrations

https://cs50.harvard.edu/web/2020/notes/4/

---

- SQL - database language used to interact with databases
 - Django provides an abstraction layer on top of SQL - interact not by writing direct SQL queries but by interacting with Python classes and objects (models)
- Migration - technique that allows updating the database in response to changes made to the underlying models

### SQLite Tpes

- TEXT
- NUMERIC
- INTEGER
- REAL - decimal point
- BLOB - any type of binary data file (e.g. images, audio etc.)

### MySQL Types

- CHAR (size)
- VARCHAR (size)
- SMALLINT
- INT
- BIGINT
- FLOAT
- DOUBLE
- etc.

### Constraints

- CHECK
- DEFAULT
- NOT NULL
- PRIMARY KEY
- UNIQUE
- etc.

### Functions

- AVERAGE
- COUNT
- MAX
- MIN
- SUM
- etc.

### Other clauses

- LIMIT
- ORDER BY
- GROUP BY
- HAVING
- etc.

### Syntax

#### Table creation

```
CREATE TABLE flights(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    duration INTEGER NOT NULL
);
```

#### Insert

```
INSERT INTO flights
    (origin, destination, duration) 
    VALUES ("New York", "London", 415);
```

#### Select

```
SELECT * FROM flights;

SELECT origin, destination FROM flights;

SELECT * FROM flights where id = 3;

SELECT * FROM flights WHERE origin = 'New York';

SELECT * FROM flights WHERE duration > 500;

SELECT * FROM flights WHERE duration > 500 AND destination = 'Paris';

SELECT * FROM flights WHERE duration > 500 OR destination = 'Paris';

SELECT * FROM flights WHERE origin IN ('New York', 'Lima');

SELECT * FROM flights WHERE origin LIKE '%a%';
```

#### Update

```
UPDATE flights
    SET duration = 430
    WHERE origin = 'New York'
    AND destination = 'London';
```

#### Delete

```
DELETE FROM flights WHERE destination = 'Tokyo';
```

### Foreign Keys and Joins

```
SELECT first, origin, destination FROM flights JOIN passengers on passengers.flight_id = flights.id;
```

- JOIN / INNER JOIN
- LEFT OUTER JOIN
- RIGHT OUTER JOIN
- FULL OUTER JOIN

### Index

```
CREATE INDEX name_index ON passengers (last);
```

### SQL Injection

- based on a web page form

```
SELECT * FROM users WHERE username = username AND password = password;
```

- input for password: hacker" --
- in SQL '--' is the start of a comment

```
SELECT * FROM users WHERE username = "hacker"--" AND password = password;
```

- one strategy is to escape these kind of characters
- another strategy is to use an abstraction layer on top of SQL so we don't have to write the SQL queries at all - e.g. with Django

### Race conditions

- multiple events happening in parallel threads for the same piece of data
- solution e.g. - lock the database to finish a transaction

### Migrations

- applying changes to the database
    - create the migration - instructions for manipulating the db (python3 manage.py makemigrations)
    - execute that migration step (python3 manage.py migrate)