-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "Region" (
    "Region_Id" int   NOT NULL,
    "Name" varchar(150)   NULL,
    "Lat" float   NULL,
    "Lon" float   NULL,
    "Country_Id" int   NULL,
    "Population" int   NULL,
    CONSTRAINT "pk_Region" PRIMARY KEY (
        "Region_Id"
     )
);

CREATE TABLE "Country" (
    "Country_Id" int   NOT NULL,
    "Name" varchar(150)   NOT NULL,
    "ISO_2" char(2)   NULL,
    "ISO_3" char(3)   NULL,
    "Lat" float   NULL,
    "Lon" float   NULL,
    "Population" int   NULL,
    CONSTRAINT "pk_Country" PRIMARY KEY (
        "Country_Id"
     )
);

CREATE TABLE "Country_Synonym" (
    "Country_Id" int   NOT NULL,
    "Synonym_Id" int   NOT NULL,
    "Synonym" varchar(150)   NOT NULL,
    CONSTRAINT "pk_Country_Synonym" PRIMARY KEY (
        "Country_Id","Synonym_Id"
     )
);

CREATE TABLE "COVID_19" (
    "Region_Id" int   NOT NULL,
    "Date" date   NOT NULL,
    "Confirmed" int   NULL,
    "Deaths" int   NULL,
    "Recovered" int   NULL,
    "Update" timestamp   NULL,
    CONSTRAINT "pk_COVID_19" PRIMARY KEY (
        "Region_Id","Date"
     )
);

ALTER TABLE "Region" ADD CONSTRAINT "fk_Region_Country_Id" FOREIGN KEY("Country_Id")
REFERENCES "Country" ("Country_Id");

ALTER TABLE "Country_Synonym" ADD CONSTRAINT "fk_Country_Synonym_Country_Id" FOREIGN KEY("Country_Id")
REFERENCES "Country" ("Country_Id");

ALTER TABLE "COVID_19" ADD CONSTRAINT "fk_COVID_19_Region_Id" FOREIGN KEY("Region_Id")
REFERENCES "Region" ("Region_Id");

