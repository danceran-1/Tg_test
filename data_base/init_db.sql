DROP TABLE users;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE device_states (
    user_id BIGINT PRIMARY KEY,
    water_on BOOLEAN DEFAULT FALSE,
    fan_on BOOLEAN DEFAULT FALSE
);

CREATE TABLE notification_users (
    user_id BIGINT PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    receive_alerts BOOLEAN DEFAULT TRUE
);