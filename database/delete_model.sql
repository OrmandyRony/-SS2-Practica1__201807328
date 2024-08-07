-- Eliminar la tabla de hechos primero para evitar conflictos de claves foráneas
DROP TABLE IF EXISTS FactVuelo;

-- Eliminar las tablas dimensionales en el orden correcto
DROP TABLE IF EXISTS DimPiloto;
DROP TABLE IF EXISTS DimContinente;
DROP TABLE IF EXISTS DimAeropuerto;
DROP TABLE IF EXISTS DimPais;
DROP TABLE IF EXISTS DimPasajero;
