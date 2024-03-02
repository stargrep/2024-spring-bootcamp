-- Database commands --
.databases
$sqlite3 testDB.db .dump > testDB.sql
$sqlite3 testDB.db < testDB.sql
-- in windows use `testDB.db -init demo1.sql`

sqlite> .read db.sql
.mode csv
-- use '.separator SOME_STRING' for something other than a comma.
.headers on
.out file.csv

.mode insert <target_table_name>
.out file.sql

PRAGMA foreign_keys = ON;

-- Data Type -- https://www.tutorialspoint.com/sqlite/sqlite_data_types.htm

CREATE TABLE exchange (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    symbol TEXT NOT NULL,
    create_at INTEGER NOT NULL,
    status TEXT NOT NULL
    -- address VARCHAR(255) --
);


CREATE TABLE stock (
    id INTEGER NOT NULL,
    symbol TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    e_id INTEGER NOT NULL, -- which exchange --
    ipo_at INTEGER NOT NULL,
    FOREIGN KEY (e_id) REFERENCES exchange (id)
);


CREATE TABLE price (
    id INTEGER PRIMARY KEY NOT NULL,
    symbol TEXT NOT NULL,
    trade_time INTEGER NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    volume INTEGER NOT NULL,
    FOREIGN KEY (symbol) REFERENCES stock (symbol)
);

INSERT INTO exchange (id, name, symbol, create_at, status)
VALUES (1, 'New York', 'NYSE', -4800764658, 'ACTIVE');

INSERT INTO exchange (id, name, symbol, create_at, status)
VALUES (2, 'Chicago', 'CME', 1184198400, 'ACTIVE');

INSERT INTO exchange (id, name, symbol, create_at, status)
VALUES (NULL, 'Test', 'TEST', 1184198400, 'INACTIVE');

sqlite>.header on
sqlite>.mode column
sqlite> SELECT * FROM exchange;

INSERT INTO stock (id, symbol, status, e_id, ipo_at)
VALUES (2, 'GOOG', 'LISTED', 1, 12345);
INSERT INTO stock (id, symbol, status, e_id, ipo_at)
VALUES (3, 'APPL', 'LISTED', 2, 12345);


INSERT INTO price (id, symbol, trade_time, open, high, low, close, volume)
VALUES (1, 'GOOG', 1001, 999.0, 999.5, 999.9, 999.1, 1550);

INSERT INTO price (id, symbol, trade_time, open, high, low, close, volume)
VALUES (2, 'GOOG', 1002, 999.0, 999.5, 999.9, 999.1, 1650);

INSERT INTO price (id, symbol, trade_time, open, high, low, close, volume)
VALUES (3, 'GOOG', 1002, 100.0, 101.0, 95.0, 100.5, 2000);

INSERT INTO price (id, symbol, trade_time, open, high, low, close, volume)
VALUES (4, 'APPL', 1005, 1200.0, 1101.0, 1295.0, 1100.5, 3000);
-- DROP / DELETE
-- UPDATE
-- search tutorial --


-- SEARCH - WHERE / LIKE
SELECT * FROM price WHERE open > 500;

-- JOIN
-- 找到在price里面Exchange symbol的list
-- GOOG ->
-- NYSE

SELECT symbol, count(*) FROM price GROUP BY symbol;

SELECT ... FROM table1 [INNER] JOIN table2 ON conditional_expression

SELECT DISTINCT e.symbol FROM
    (
        SELECT * FROM
            price p JOIN stock s
            ON p.symbol = s.symbol
    ) t
    JOIN exchange e
    ON t.e_id = e.id;