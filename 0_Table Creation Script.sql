-- Table: public.airport_traffic

-- DROP TABLE IF EXISTS public.airport_traffic;

CREATE TABLE IF NOT EXISTS public.airport_traffic
(
    "Airport_Code_0" text COLLATE pg_catalog."default",
    "Airport_Code_1" text COLLATE pg_catalog."default",
    "Year" bigint,
    "Month" text COLLATE pg_catalog."default",
    "Revenue_Passenger" bigint,
    "Aircraft_Trips" integer,
    "Rev_Pax_LF_Perc" double precision,
    "Distance_klm" integer,
    "RPKs" integer,
    "ASKs" integer,
    "Seats" integer,
    "Annual_Revenue_Passenger" bigint,
    "Annual_Aircraft_Trips" integer,
    "Annual_Rev_Pax_LF_Perc" double precision,
    "Annual_RPKs" integer,
    "Annual_ASKs" integer,
    "Annual_Seats" integer,
    "City_Pair_Route" text COLLATE pg_catalog."default",
    "MM" bigint
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.airport_traffic
    OWNER to postgres;
	
	
	
-- Table: public.airports

-- DROP TABLE IF EXISTS public.airports;

CREATE TABLE IF NOT EXISTS public.airports
(
    id bigint NOT NULL,
    ident text COLLATE pg_catalog."default" NOT NULL,
    type text COLLATE pg_catalog."default",
    name text COLLATE pg_catalog."default",
    latitude double precision,
    longitude double precision,
    region text COLLATE pg_catalog."default",
    municipality text COLLATE pg_catalog."default",
    gps_code text COLLATE pg_catalog."default",
    iata_code text COLLATE pg_catalog."default",
    CONSTRAINT airports_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.airports
    OWNER to postgres;
	
	
-- Table: public.city

-- DROP TABLE IF EXISTS public.city;

CREATE TABLE IF NOT EXISTS public.city
(
    id bigint,
    city text COLLATE pg_catalog."default",
    lat double precision,
    lng double precision,
    state_code text COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.city
    OWNER to postgres;
	
-- Table: public.road_fatalities

-- DROP TABLE IF EXISTS public.road_fatalities;

CREATE TABLE IF NOT EXISTS public.road_fatalities
(
    "Crash ID" bigint,
    "State" text COLLATE pg_catalog."default",
    "Month" text COLLATE pg_catalog."default",
    "Year" bigint,
    "Dayweek" text COLLATE pg_catalog."default",
    "Time" text COLLATE pg_catalog."default",
    "Crash Type" text COLLATE pg_catalog."default",
    "Bus Involvement" text COLLATE pg_catalog."default",
    "Heavy Rigid Truck Inv" text COLLATE pg_catalog."default",
    "Articulated Truck Inv" text COLLATE pg_catalog."default",
    "Speed Limit" text COLLATE pg_catalog."default",
    "Road User" text COLLATE pg_catalog."default",
    "Gender" text COLLATE pg_catalog."default",
    "Age" bigint,
    "National Remoteness Areas" text COLLATE pg_catalog."default",
    "SA4 Name 2016" text COLLATE pg_catalog."default",
    "National LGA Name 2017" text COLLATE pg_catalog."default",
    "National Road Type" text COLLATE pg_catalog."default",
    "Christmas Period" text COLLATE pg_catalog."default",
    "Easter Period" text COLLATE pg_catalog."default",
    "Age Group" text COLLATE pg_catalog."default",
    "Day of week" text COLLATE pg_catalog."default",
    "Time of day" text COLLATE pg_catalog."default",
    "MM" bigint
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.road_fatalities
    OWNER to postgres;
	
-- Table: public.states

-- DROP TABLE IF EXISTS public.states;

CREATE TABLE IF NOT EXISTS public.states
(
    "State_or_Territory" text COLLATE pg_catalog."default",
    state_code text COLLATE pg_catalog."default" NOT NULL,
    "Capital" text COLLATE pg_catalog."default",
    "Population_Dec_2021" bigint,
    "Area_km2" bigint,
    CONSTRAINT states_pkey PRIMARY KEY (state_code)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.states
    OWNER to postgres;