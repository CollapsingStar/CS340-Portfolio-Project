-- Flask/SQL interaction for Cascade Castles

-- GUEST TABLE

-- list all guests
SELECT * FROM guests;

-- insert a guest
INSERT INTO guests (guest_name, email, phone_num)
VALUES (:guest_name_input, :guest_email_input, :phone_num_input);

-- edit a guest
UPDATE guests SET guest_name = :guest_name_input, email = :email_input, phone_num = :phone_num_input)
WHERE guest_id = :guest_id_input;

-- delete a guest
DELETE FROM guests WHERE guest_id = :guest_id_input;

--------------------------------------------------------------------------

-- ORDERS TABLE

-- list all orders
SELECT * FROM orders;

-- insert an order
INSERT INTO `orders` (`season_pass_holder`, `guest_id`, `date`, `ticket`)
VALUES (FALSE, 
        (SELECT guest_id FROM guests WHERE guest_id=:guest_id_input), 
        (SELECT date FROM dates WHERE date=:date_input), 
        TRUE);

-- edit an order
UPDATE orders SET guest_id = :guest_id_input, date = :date_input, ticket = :ticket_input, season_pass_holder = :season_pass_holder_input
WHERE order_id = :order_id_input;

-- delete an order
DELETE FROM orders WHERE order_id = :order_id_input;

--------------------------------------------------------------------------

-- ATTRACTIONS table

-- list of all attractions
SELECT * FROM attractions;

-- insert an attraction
INSERT INTO `attractions` (`ride_id`, `num_riders`, `date_created`, `ride_name`)
VALUES (:ride_id_input(AI), 
        :num_riders_input, 
        (SELECT date FROM dates WHERE date=:date_input), 
        :ride_name_input);

-- edit an attraction
UPDATE attractions SET ride_name = :ride_name_input, date_created = (SELECT date FROM dates WHERE date=:date_created_input), num_riders = :num_riders_input
WHERE ride_id = :ride_id_input;

-- delete an attraction
DELETE FROM attractions WHERE ride_id = :ride_id_input;

--------------------------------------------------------------------------

-- DATE table

-- list all dates
SELECT * FROM dates;

-- insert a date
INSERT INTO dates (date, holiday, weather)
VALUES (:date_input, :holiday_input, :weather_input);

-- edit a date
UPDATE dates SET date = :date_input, holiday = :holiday_input, weather = :weather_input
WHERE date = :date_input;

-- delete date
DELETE FROM dates WHERE date = :date_input;


--------------------------------------------------------------------------


-- GUESTS_HAS_ATTRACTIONS table

-- list all guests_has_attractions entries
SELECT * FROM guests_has_attractions;

-- insert guests_has_attractions
INSERT INTO `guests_has_attractions` (`guest_id`, `ride_id`, `date`)
VALUES ((SELECT guest_id FROM guests where guest_id = :guest_id_input),
        (SELECT ride_id FROM attractions WHERE ride_id = :ride_id_input), 
        (SELECT date FROM dates WHERE date=:date_input));

-- delete guest_has_attractions
DELETE FROM guests_has_attractions WHERE guest_attraction_id = :guest_attraction_id_input;

--------------------------------------------------------------------------

--  MASTER_TABLE table

-- list all master table entries
SELECT * FROM master_table;

-- insert master table record
INSERT INTO master_table (total_guests, total_riders, date)
VALUES (:total_guests, :total_riders, (SELECT date FROM dates WHERE date=:date_input));

-- update master table record
UPDATE master_table SET total_guests = :total_guests_input, total_riders = :total_riders, date = (SELECT date FROM dates WHERE date=:date_input)
WHERE date = :date_input;

-- delete master table record
DELETE FROM master_table WHERE date = :date_input;