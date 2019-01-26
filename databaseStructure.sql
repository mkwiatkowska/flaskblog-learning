--
-- File generated with SQLiteStudio v3.2.1 on czw. gru 20 00:44:30 2018
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: PerfumeInfo
CREATE TABLE PerfumeInfo (perfumeId INTEGER PRIMARY KEY NOT NULL, perfumeName VARCHAR (50) NOT NULL, perfumeBrand VARCHAR (50) NOT NULL);

-- Table: PerfumeScent
CREATE TABLE PerfumeScent (perfumeId INTEGER REFERENCES PerfumeInfo (perfumeId) ON DELETE SET NULL ON UPDATE CASCADE, scentId INTEGER REFERENCES Scents (scentId) ON DELETE SET NULL ON UPDATE CASCADE);

-- Table: Scents
CREATE TABLE Scents (scentId INTEGER PRIMARY KEY NOT NULL, scentName VARCHAR (50) NOT NULL);

-- Table: Users
CREATE TABLE Users (userId INTEGER PRIMARY KEY NOT NULL, userName VARCHAR (50) NOT NULL, password VARCHAR (50) NOT NULL, email VARCHAR (50) NOT NULL);

-- Table: UsersPreferences
CREATE TABLE UsersPreferences (userId INTEGER REFERENCES Users (userId) ON DELETE SET NULL ON UPDATE CASCADE, perfumeId INTEGER REFERENCES PerfumeInfo (perfumeId) ON DELETE SET NULL ON UPDATE CASCADE);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
