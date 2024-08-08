from sqlalchemy import create_engine, text

def drop_model():
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
            # Eliminar las tablas si existen
            connection.execute(text("""
                IF OBJECT_ID('FactFlights', 'U') IS NOT NULL
                DROP TABLE FactFlights;
            """))

            connection.execute(text("""
                IF OBJECT_ID('DimFlightStatus', 'U') IS NOT NULL
                DROP TABLE DimFlightStatus;
            """))

            connection.execute(text("""
                IF OBJECT_ID('DimDate', 'U') IS NOT NULL
                DROP TABLE DimDate;
            """))

            connection.execute(text("""
                IF OBJECT_ID('DimAirport', 'U') IS NOT NULL
                DROP TABLE DimAirport;
            """))

            connection.execute(text("""
                IF OBJECT_ID('DimPassenger', 'U') IS NOT NULL
                DROP TABLE DimPassenger;
            """))

            # Confirmar la transacción si todo fue bien
            trans.commit()
            print("Modelo eliminado correctamente.")

        except Exception as e:
            # Revertir la transacción en caso de error
            trans.rollback()
            print(f"Error al eliminar el modelo: {e}")


#   with open('C:\Dev\Semi2_P1\src\sql\create_tables.sql', 'r') as file: