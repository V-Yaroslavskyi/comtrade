CREATE TABLE data
(
    "Classification" VARCHAR(50) NOT NULL,
    "Year" INTEGER,
    "Period Desc." VARCHAR(50),
    "Aggregate Level" INTEGER,
    "Is Leaf Code" INTEGER,
    "Trade Flow Code" INTEGER NOT NULL,
    "Trade Flow" VARCHAR(50),
    "Reporter Code" INTEGER NOT NULL,
    "Reporter" VARCHAR(50),
    "Reporter ISO" VARCHAR(50),
    "Partner Code" INTEGER NOT NULL,
    "Partner" VARCHAR(50),
    "Partner ISO" VARCHAR(50),
    "2nd Partner Code" INTEGER,
    "2nd Partner" VARCHAR(50),
    "2nd Partner ISO" VARCHAR(50),
    "Customs Proc. Code" INTEGER,
    "Customs" VARCHAR(50),
    "Mode of Transport Code" INTEGER,
    "Mode of Transport" VARCHAR(50),
    "Commodity Code" INTEGER NOT NULL,
    "Commodity" VARCHAR(255),
    "Qty Unit Code" INTEGER,
    "Qty Unit" VARCHAR(50),
    "Qty" INTEGER,
    "Alt Qty Unit Code" INTEGER,
    "Alt Qty Unit" VARCHAR(50),
    "Alt Qty" INTEGER,
    "Netweight (kg)" DOUBLE PRECISION,
    "Gross weight (kg)" DOUBLE PRECISION,
    "Trade Value (US$)" BIGINT,
    "CIF Trade Value (US$)" BIGINT,
    "FOB Trade Value (US$)" BIGINT,
    "Flag " INTEGER,
    "Period" BIGINT NOT NULL
);
CREATE UNIQUE INDEX "data_Classification_Period_Reporter Code_Commodity Code_Partner" ON data ("Classification", "Reporter Code", "Commodity Code", "Partner Code", "Trade Flow Code");
