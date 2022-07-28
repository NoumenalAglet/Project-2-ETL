CREATE SCHEMA "project2";

CREATE TABLE "project2"."airports" (
  "id" int PRIMARY KEY,
  "ident" varchar,
  "type" varchar,
  "name" varchar,
  "latitude" varchar,
  "longitude" varchar,
  "region" varchar,
  "municipality" varchar,
  "gps_code" varchar,
  "iata_code" varchar
);

CREATE TABLE "project2"."airport_traffic" (
  "Airport_Code_0" varchar,
  "Airport_Code_1" varchar,
  "Year" int,
  "Month" int,
  "Revenue_Passenger" int,
  "Aircraft_Trips" int,
  "Rev_Pax_LF_Perc" float,
  "Distance_klm" int,
  "RPKs" int,
  "ASKs" int,
  "Seats" int,
  "Annual_Revenue_Passenger" int,
  "Annual_Aircraft_Trips" int,
  "Annual_Rev_Pax_LF_Perc" int,
  "Annual_RPKs" int,
  "Annual_ASKs" int,
  "Annual_Seats" int,
  "City_Pair_Route" varchar
);

ALTER TABLE "project2"."airports" ADD FOREIGN KEY ("iata_code") REFERENCES "project2"."airport_traffic" ("Airport_Code_1");

ALTER TABLE "project2"."airports" ADD FOREIGN KEY ("iata_code") REFERENCES "project2"."airport_traffic" ("Airport_Code_0");
