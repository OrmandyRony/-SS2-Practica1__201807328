from sqlalchemy import create_engine, text

def create_model():
    server = 'ORMANDYRONY'# Cambia esto según tu configuración
    database = 'AviationDW'# Cambia esto según tu configuración
    username = 'admin'# Cambia esto según tu configuración
    password = 'admin'# Cambia esto según tu configuración
    driver = 'ODBC Driver 17 for SQL Server'# Crear conexión a la base de datos
    engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}')

    # Revisar la conexión y gestionar las transacciones
    with engine.connect() as connection:
        print("Conexión exitosa.")

        # Iniciar una transacción
        trans = connection.begin()

        try:
            # Ejecutar sentencias SQL individuales
            connection.execute(text("""
                CREATE TABLE DimPassenger (
                    PassengerID INT IDENTITY(1,1) PRIMARY KEY,
                    FirstName NVARCHAR(100),
                    LastName NVARCHAR(100),
                    Gender NVARCHAR(10),
                    Age INT,
                    Nationality NVARCHAR(50)
                );
            """))
            connection.execute(text("""
                CREATE TABLE DimAirport (
                    AirportID INT IDENTITY(1,1) PRIMARY KEY,
                    AirportName NVARCHAR(100),
                    AirportCountryCode NVARCHAR(10),
                    CountryName NVARCHAR(100),
                    AirportContinent NVARCHAR(50),
                    Continents NVARCHAR(50)
                );
            """))
            connection.execute(text("""
                CREATE TABLE DimDate (
                    DateID INT IDENTITY(1,1) PRIMARY KEY,
                    DepartureDate DATE,
                    Day INT,
                    Month INT,
                    Year INT,
                    DayOfWeek NVARCHAR(10)
                );
            """))
            connection.execute(text("""
                CREATE TABLE DimFlightStatus (
                    StatusID INT IDENTITY(1,1) PRIMARY KEY,
                    FlightStatus NVARCHAR(50)
                );
            """))
            connection.execute(text("""
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
            """))

            # Confirmar la transacción si todo fue bien
            trans.commit()
            print("Modelo creado correctamente.")

        except Exception as e:
            # Revertir la transacción en caso de error
            trans.rollback()
            print(f"Error al crear el modelo: {e}")
