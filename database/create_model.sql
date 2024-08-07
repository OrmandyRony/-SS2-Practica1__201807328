-- Tabla DimPasajero
CREATE TABLE DimPasajero (
    PasajeroID NVARCHAR(50) PRIMARY KEY,
    Nombre NVARCHAR(100),
    Apellido NVARCHAR(100),
    Genero NVARCHAR(10)
);

-- Tabla DimPais
CREATE TABLE DimPais (
    PaisID INT PRIMARY KEY IDENTITY,
    NombrePais NVARCHAR(100),
    CodigoPais NVARCHAR(50)
);

-- Tabla DimAeropuerto
CREATE TABLE DimAeropuerto (
    AeropuertoID INT PRIMARY KEY IDENTITY,
    NombreAeropuerto NVARCHAR(200),
    CodigoPaisAeropuerto NVARCHAR(50),
    PaisID INT,
    FOREIGN KEY (PaisID) REFERENCES DimPais(PaisID)
);

-- Tabla DimContinente
CREATE TABLE DimContinente (
    ContinenteID INT PRIMARY KEY IDENTITY,
    NombreContinente NVARCHAR(50)
);

-- Tabla DimPiloto
CREATE TABLE DimPiloto (
    PilotoID INT PRIMARY KEY IDENTITY,
    NombrePiloto NVARCHAR(100)
);

-- Tabla FactVuelo
CREATE TABLE FactVuelo (
    VueloID INT PRIMARY KEY IDENTITY,
    PasajeroID NVARCHAR(50),
    FechaSalida DATE,
    AeropuertoLlegadaID INT,
    PilotoID INT,
    EstadoVuelo NVARCHAR(50),
    Edad INT,
    NacionalidadID INT,
    CodigoPaisAeropuerto NVARCHAR(50),
    NombrePais NVARCHAR(100),
    ContinenteID INT,
    FOREIGN KEY (PasajeroID) REFERENCES DimPasajero(PasajeroID),
    FOREIGN KEY (AeropuertoLlegadaID) REFERENCES DimAeropuerto(AeropuertoID),
    FOREIGN KEY (PilotoID) REFERENCES DimPiloto(PilotoID),
    FOREIGN KEY (NacionalidadID) REFERENCES DimPais(PaisID),
    FOREIGN KEY (ContinenteID) REFERENCES DimContinente(ContinenteID)
);
