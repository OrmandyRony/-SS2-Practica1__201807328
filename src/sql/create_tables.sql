CREATE TABLE DimPassenger (
    PassengerID INT IDENTITY(1,1) PRIMARY KEY,
    FirstName NVARCHAR(100),
    LastName NVARCHAR(100),
    Gender NVARCHAR(10),
    Age INT,
    Nationality NVARCHAR(50)
);


CREATE TABLE DimAirport (
    AirportID INT IDENTITY(1,1) PRIMARY KEY,
    AirportName NVARCHAR(100),
    AirportCountryCode NVARCHAR(10),
    CountryName NVARCHAR(100),
    AirportContinent NVARCHAR(50),
    Continents NVARCHAR(50)
);

CREATE TABLE DimDate (
    DateID INT IDENTITY(1,1) PRIMARY KEY,
    DepartureDate DATE,
    Day INT,
    Month INT,
    Year INT,
    DayOfWeek NVARCHAR(10)
);

CREATE TABLE DimFlightStatus (
    StatusID INT IDENTITY(1,1) PRIMARY KEY,
    FlightStatus NVARCHAR(50)
);

CREATE TABLE FactFlights (
    FlightID INT IDENTITY(1,1) PRIMARY KEY,
    PassengerID INT,
    AirportID INT,
    DateID INT,
    StatusID INT,
    ArrivalAirport NVARCHAR(100),
    PilotName NVARCHAR(100),
    FOREIGN KEY (PassengerID) REFERENCES DimPassenger(PassengerID),
    FOREIGN KEY (AirportID) REFERENCES DimAirport(AirportID),
    FOREIGN KEY (DateID) REFERENCES DimDate(DateID),
    FOREIGN KEY (StatusID) REFERENCES DimFlightStatus(StatusID)
);
