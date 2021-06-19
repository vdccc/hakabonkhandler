CREATE TABLE prices (
	id SERIAL PRIMARY KEY,
	date timestamp,
	item_id int,
	misses int
);
