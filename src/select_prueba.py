from sqlalchemy import create_engine, text

def select_prueba():
    server = 'ORMANDYRONY'# Cambia esto según tu configuración
    database = 'AviationDW'# Cambia esto según tu configuración
    username = 'admin'# Cambia esto según tu configuración
    password = 'admin'# Cambia esto según tu configuración
    driver = 'ODBC Driver 17 for SQL Server'

    engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}')

    # Revisar la conexión
    with engine.connect() as connection:
        print("Conexión exitosa.")

        # Iniciar una transacción
        trans = connection.begin()

        try:
            # Realizar el CREATE TABLE
            query = """
            CREATE TABLE DimAirport (
                AirportID INT IDENTITY(1,1) PRIMARY KEY,
                AirportName NVARCHAR(100),
                AirportCountryCode NVARCHAR(10),
                CountryName NVARCHAR(100),
                AirportContinent NVARCHAR(50),
                Continents NVARCHAR(50)
            );
            """
            connection.execute(text(query))

            # Confirmar la transacción
            trans.commit()
            print("Tabla 'DimAirport' creada correctamente.")

        except Exception as e:
            # Revertir la transacción en caso de error
            trans.rollback()
            print(f"Error al crear la tabla: {e}")