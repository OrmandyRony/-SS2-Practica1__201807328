-- CREAR TABLA TEMPORAL PARA VUELOS
CREATE TABLE #VuelosTemporales(
    PasajeroID NVARCHAR(50) NOT NULL,
    Nombre NVARCHAR(50) NOT NULL,
    Apellido NVARCHAR(50) NOT NULL,
    Genero NVARCHAR(50) NOT NULL,
    Edad TINYINT NOT NULL,
    Nacionalidad NVARCHAR(50) NOT NULL,
    NombreAeropuerto NVARCHAR(100) NOT NULL,
    CodigoPaisAeropuerto NVARCHAR(50) NOT NULL,
    NombrePais NVARCHAR(50) NOT NULL,
    ContinenteAeropuerto NVARCHAR(50) NOT NULL,
    Continente NVARCHAR(50) NOT NULL,
    FechaSalida VARCHAR(50) NOT NULL,
    AeropuertoLlegada NVARCHAR(50) NOT NULL,
    NombrePiloto NVARCHAR(50) NOT NULL,
    EstadoVuelo NVARCHAR(50) NOT NULL
) ON [PRIMARY];

-- CARGAR DATOS DESDE UN ARCHIVO CSV
BULK INSERT #VuelosTemporales
FROM '/data/pasajeros.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2,
    TABLOCK
);

-- ELIMINAR DUPLICADOS DE LA TABLA TEMPORAL
WITH CTE_Duplicados AS (
    SELECT PasajeroID, 
           ROW_NUMBER() OVER (PARTITION BY PasajeroID ORDER BY (SELECT NULL)) AS NumFila
    FROM #VuelosTemporales
)
DELETE FROM CTE_Duplicados
WHERE NumFila > 1;

-- ELIMINAR REGISTROS DONDE EL AEROPUERTO DE LLEGADA ES '0'
DELETE FROM #VuelosTemporales
WHERE AeropuertoLlegada = '0';

-- TRANSFORMAR Y CARGAR DATOS EN LAS TABLAS DIMENSIONALES

-- Cargar datos en DimPasajero
INSERT INTO DimPasajero (PasajeroID, Nombre, Apellido, Genero)
SELECT DISTINCT PasajeroID, Nombre, Apellido, Genero
FROM #VuelosTemporales;

-- Cargar datos en DimPais
INSERT INTO DimPais (NombrePais, CodigoPais)
SELECT DISTINCT REPLACE(NombrePais, '"', '') AS NombrePais, CodigoPaisAeropuerto
FROM #VuelosTemporales;

-- Cargar datos en DimAeropuerto
INSERT INTO DimAeropuerto (NombreAeropuerto, CodigoPais, PaisID)
SELECT DISTINCT REPLACE(NombreAeropuerto, '"', '') AS NombreAeropuerto, CodigoPaisAeropuerto, dp.PaisID
FROM #VuelosTemporales vt
JOIN DimPais dp ON vt.NombrePais = dp.NombrePais;

-- Cargar datos en DimContinente
INSERT INTO DimContinente (NombreContinente)
SELECT DISTINCT Continente
FROM #VuelosTemporales;

-- Cargar datos en DimPiloto
INSERT INTO DimPiloto (NombrePiloto)
SELECT DISTINCT NombrePiloto
FROM #VuelosTemporales;

-- CARGAR DATOS EN LA TABLA DE HECHOS FactVuelo
INSERT INTO FactVuelo (PasajeroID, FechaSalida, AeropuertoLlegadaID, PilotoID, EstadoVuelo, Edad, NacionalidadID, CodigoPais, NombrePais, ContinenteID)
SELECT 
    vt.PasajeroID,
    TRY_CONVERT(DATE, vt.FechaSalida, 101) AS FechaSalida, -- Conversión segura de la fecha
    da.AeropuertoID,
    dp.PilotoID,
    vt.EstadoVuelo,
    vt.Edad,
    dpais.PaisID,
    vt.CodigoPaisAeropuerto,
    vt.NombrePais,
    dc.ContinenteID
FROM #VuelosTemporales vt
JOIN DimAeropuerto da ON vt.NombreAeropuerto = da.NombreAeropuerto
JOIN DimPiloto dp ON vt.NombrePiloto = dp.NombrePiloto
JOIN DimPais dpais ON vt.NombrePais = dpais.NombrePais
JOIN DimContinente dc ON vt.Continente = dc.NombreContinente;