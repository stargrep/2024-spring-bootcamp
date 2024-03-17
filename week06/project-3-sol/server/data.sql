CREATE TABLE IF NOT EXISTS client_rates (
    id INTEGER PRIMARY KEY,
    client_id TEXT,
    rate REAL
);

CREATE TABLE IF NOT EXISTS stock_price (
    symbol TEXT,
    trade_date TEXT,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume REAL
);

CREATE TABLE IF NOT EXISTS strategy_return (
    strategy TEXT,
    start_date TEXT,
    end_date TEXT,
    annual_return REAL,
    asset REAL,
    cost REAL,
    symbol TEXT
);

INSERT INTO client_rates
VALUES
    (1, 'client1', 0.1),
    (2, 'client2', 0.12),
    (3, 'client3', 0.2),
    (4, 'client4', 0.15);

