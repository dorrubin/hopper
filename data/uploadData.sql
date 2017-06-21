CREATE DATABASE IF NOT EXIST hopper;

CREATE TABLE flights (
    search_id VARCHAR(36),
    trip_index INT UNSIGNED,
    received_date DATE,
    received_ms BIGINT UNSIGNED,
    origin TEXT(3),
    destination TEXT(3),
    total_usd NUMERIC(10,2),
    pax_type TEXT,
    refundable TEXT,
    validating_carrier TEXT,
    departure_odate DATE,
    departure_ms BIGINT UNSIGNED,
    outgoing_duration INT UNSIGNED,
    outgoing_stops INT(1),
    return_odate DATE,
    return_ms BIGINT UNSIGNED,
    returning_duration INT(5) UNSIGNED,
    returning_stops INT(1) UNSIGNED,
    major_carrier_id TEXT(2),
    total_stops INT(1),
    advance INT(5),
    length_of_stay INT(5),
    includes_saturday_night_stay TEXT,
    available_seats INT(5) UNSIGNED,
    lowest_cabin_class TEXT(1),
    highest_cabin_class TEXT(1)
);

LOAD DATA INFILE '/Users/DorRubin/dev/fightforflight/data/boscun-longitudinal.csv' INTO TABLE flights
  FIELDS TERMINATED BY ','
  IGNORE 1 LINES;


