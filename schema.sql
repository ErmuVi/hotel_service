
CREATE TABLE bookings_room (
    id BIGSERIAL PRIMARY KEY,
    room_description TEXT NOT NULL,
    price_room NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL    
);


CREATE TABLE bookings_booking (
    id BIGSERIAL PRIMARY KEY,
    date_start DATE NOT NULL,
    date_end DATE NOT NULL,
    room_id BIGINT NOT NULL REFERENCES bookings_room(id) ON DELETE CASCADE
);
