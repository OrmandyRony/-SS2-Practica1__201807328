-- Contar registros en cada tabla dimensional y la tabla de hechos
SELECT 'DimPasajero' AS NombreTabla, COUNT(*) AS ConteoRegistros FROM DimPasajero
UNION ALL
SELECT 'DimPais', COUNT(*) FROM DimPais
UNION ALL
SELECT 'DimAeropuerto', COUNT(*) FROM DimAeropuerto
UNION ALL
SELECT 'DimContinente', COUNT(*) FROM DimContinente
UNION ALL
SELECT 'DimPiloto', COUNT(*) FROM DimPiloto
UNION ALL
SELECT 'FactVuelo', COUNT(*) FROM FactVuelo;

-- Contar pasajeros por género y calcular el porcentaje
SELECT 
    Genero,
    COUNT(*) AS ConteoPasajeros,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS DECIMAL(5, 2)) AS Porcentaje
FROM DimPasajero
GROUP BY Genero;

-- Número de salidas mensuales por país para el año 2022
WITH SalidasMensuales AS (
    SELECT 
        p.NombrePais,
        FORMAT(v.FechaSalida, 'MM-yyyy') AS MesAnio,
        COUNT(*) AS ConteoSalidas
    FROM FactVuelo v
    JOIN DimPais p ON v.NacionalidadID = p.PaisID
    WHERE YEAR(v.FechaSalida) = 2022
    GROUP BY p.NombrePais, FORMAT(v.FechaSalida, 'MM-yyyy')
)
SELECT 
    NombrePais,
    ISNULL([01-2022], 0) AS '01-2022',
    ISNULL([02-2022], 0) AS '02-2022',
    ISNULL([03-2022], 0) AS '03-2022',
    ISNULL([04-2022], 0) AS '04-2022',
    ISNULL([05-2022], 0) AS '05-2022',
    ISNULL([06-2022], 0) AS '06-2022',
    ISNULL([07-2022], 0) AS '07-2022',
    ISNULL([08-2022], 0) AS '08-2022',
    ISNULL([09-2022], 0) AS '09-2022',
    ISNULL([10-2022], 0) AS '10-2022',
    ISNULL([11-2022], 0) AS '11-2022',
    ISNULL([12-2022], 0) AS '12-2022'
FROM 
    SalidasMensuales
PIVOT 
(
    SUM(ConteoSalidas)
    FOR MesAnio IN (
        [01-2022], [02-2022], [03-2022], 
        [04-2022], [05-2022], [06-2022], 
        [07-2022], [08-2022], [09-2022], 
        [10-2022], [11-2022], [12-2022]
    )
) AS TablaPivot
ORDER BY 
    NombrePais ASC;

-- Contar vuelos por país de origen y ordenar por la cantidad de vuelos
SELECT 
    p.NombrePais,
    COUNT(*) AS ConteoVuelos
FROM FactVuelo v
JOIN DimPais p ON v.NacionalidadID = p.PaisID
GROUP BY p.NombrePais
ORDER BY ConteoVuelos DESC;

-- Top 5 aeropuertos con más pasajeros
SELECT TOP 5
    a.NombreAeropuerto,
    COUNT(*) AS ConteoPasajeros
FROM FactVuelo v
JOIN DimAeropuerto a ON v.AeropuertoLlegadaID = a.AeropuertoID
GROUP BY a.NombreAeropuerto
ORDER BY ConteoPasajeros DESC;

-- Top 5 países con más visitas
SELECT TOP 5
    p.NombrePais,
    COUNT(*) AS ConteoVisitas
FROM FactVuelo v
JOIN DimPais p ON v.NacionalidadID = p.PaisID
GROUP BY p.NombrePais
ORDER BY ConteoVisitas DESC;

-- Contar vuelos por estado del vuelo
SELECT 
    v.EstadoVuelo,
    COUNT(*) AS ConteoVuelos
FROM FactVuelo v
GROUP BY v.EstadoVuelo;

-- Top 5 continentes con más visitas
SELECT TOP 5
    c.NombreContinente,
    COUNT(*) AS ConteoVisitas
FROM FactVuelo v
JOIN DimContinente c ON v.ContinenteID = c.ContinenteID
GROUP BY c.NombreContinente
ORDER BY ConteoVisitas DESC;

-- Top 5 grupos de edad y género con más viajes
SELECT TOP 5
    p.Edad,
    p.Genero,
    COUNT(*) AS ConteoViajes
FROM FactVuelo v
JOIN DimPasajero p ON v.PasajeroID = p.PasajeroID
GROUP BY p.Edad, p.Genero
ORDER BY ConteoViajes DESC;

-- Contar vuelos por mes y año
SELECT 
    FORMAT(FechaSalida, 'MM-yyyy') AS MesAnio,
    COUNT(*) AS ConteoVuelos
FROM FactVuelo
GROUP BY FORMAT(FechaSalida, 'MM-yyyy')
ORDER BY FORMAT(FechaSalida, 'MM-yyyy');