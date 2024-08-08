import pandas as pd
from sqlalchemy import create_engine, text

def run_etl(step):
    # Configuración de la conexión a SQL Server
    server = 'ORMANDYRONY'# Cambia esto según tu configuración
    database = 'AviationDW'# Cambia esto según tu configuración
    username = 'admin'# Cambia esto según tu configuración
    password = 'admin'# Cambia esto según tu configuración
    driver = 'ODBC Driver 17 for SQL Server'# Crear conexión a la base de datos
    engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}')

    # Revisar la conexión y gestionar las transacciones
    with engine.connect() as connection:
        print("Conexión exitosa.")

        if step == 'extract':
            # Extraer los datos del CSV
            file_path = 'data/VuelosDataSet.csv'
            try:
                data = pd.read_csv(file_path)
                print("Datos extraídos correctamente.")
                return data
            except FileNotFoundError:
                print(f"El archivo {file_path} no existe.")
                return None 
        elif step == 'transform':
            # Transformar los datos
            data = pd.read_csv('data/VuelosDataSet.csv')

            # Limpiar datos nulos
            data_cleaned = data.dropna()

            # Normalizar las fechas
            data_cleaned['Departure Date'] = pd.to_datetime(data_cleaned['Departure Date'], format='%m/%d/%Y', errors='coerce')

            # Filtrar filas con fechas no válidas
            data_cleaned = data_cleaned.dropna(subset=['Departure Date'])

            # Estandarizar texto (minúsculas para columnas de texto)
            columns_to_standardize = ['Flight Status', 'Airport Name', 'Country Name', 'Airport Continent', 'Continents']
            for column in columns_to_standardize:
                data_cleaned[column] = data_cleaned[column].str.lower()

            # Renombrar las columnas para que coincidan con la estructura en SQL Server
            column_mapping = {
                "Passenger ID": "PassengerID",
                "First Name": "FirstName",
                "Last Name": "LastName",
                "Gender": "Gender",
                "Age": "Age",
                "Nationality": "Nationality",
                "Airport Name": "AirportName",
                "Airport Country Code": "AirportCountryCode",
                "Country Name": "CountryName",
                "Airport Continent": "AirportContinent",
                "Continents": "Continents",
                "Departure Date": "DepartureDate",
                "Arrival Airport": "ArrivalAirport",
                "Pilot Name": "PilotName",
                "Flight Status": "FlightStatus"
            }
            
            data_cleaned.rename(columns=column_mapping, inplace=True)
            print("Datos transformados correctamente.")
            return data_cleaned

        elif step == 'load':
            # Transformación y carga de datos
            data_cleaned = run_etl('transform')
            
            if data_cleaned is not None:
                # Iniciar una transacción
                trans = connection.begin()

                try:
                    # Eliminar la columna PassengerID antes de la inserción en DimPassenger, ya que es una columna IDENTITY
                    passenger_data = data_cleaned[['FirstName', 'LastName', 'Gender', 'Age', 'Nationality']].drop_duplicates()
                    passenger_data.to_sql('DimPassenger', con=engine, index=False, if_exists='append', method='multi')

                    # Cargar los datos en las otras tablas de dimensiones
                    airport_data = data_cleaned[['AirportName', 'AirportCountryCode', 'CountryName', 'AirportContinent', 'Continents']].drop_duplicates()
                    airport_data.to_sql('DimAirport', con=engine, index=False, if_exists='append', method='multi')

                    date_data = data_cleaned[['DepartureDate']].drop_duplicates()
                    date_data.to_sql('DimDate', con=engine, index=False, if_exists='append', method='multi')

                    status_data = data_cleaned[['FlightStatus']].drop_duplicates()
                    status_data.to_sql('DimFlightStatus', con=engine, index=False, if_exists='append', method='multi')

                    # Cargar los datos en la tabla de hechos (FactFlights)
                    for index, row in data_cleaned.iterrows():
                        # Escapar comillas simples en los valores de texto
                        first_name = row['FirstName'].replace("'", "''")
                        last_name = row['LastName'].replace("'", "''")
                        gender = row['Gender'].replace("'", "''")
                        nationality = row['Nationality'].replace("'", "''")
                        airport_name = row['AirportName'].replace("'", "''")
                        country_code = row['AirportCountryCode'].replace("'", "''")
                        arrival_airport = row['ArrivalAirport'].replace("'", "''")
                        pilot_name = row['PilotName'].replace("'", "''")
                        flight_status = row['FlightStatus'].replace("'", "''")

                        # Obtener las claves foráneas correspondientes
                        passenger_id = connection.execute(text(f"SELECT PassengerID FROM DimPassenger WHERE FirstName='{first_name}' AND LastName='{last_name}' AND Gender='{gender}' AND Age={row['Age']} AND Nationality='{nationality}'")).scalar()
                        airport_id = connection.execute(text(f"SELECT AirportID FROM DimAirport WHERE AirportName='{airport_name}' AND AirportCountryCode='{country_code}'")).scalar()
                        date_id = connection.execute(text(f"SELECT DateID FROM DimDate WHERE DepartureDate='{row['DepartureDate']}'")).scalar()
                        status_id = connection.execute(text(f"SELECT StatusID FROM DimFlightStatus WHERE FlightStatus='{flight_status}'")).scalar()

                        # Insertar los valores en la tabla de hechos
                        print(f"INSERT INTO FactFlights (PassengerID, AirportID, DateID, StatusID, ArrivalAirport, PilotName) VALUES ({passenger_id}, {airport_id}, {date_id}, {status_id}, '{arrival_airport}', '{pilot_name}')")
                        connection.execute(text(f"""
                            INSERT INTO FactFlights (PassengerID, AirportID, DateID, StatusID, ArrivalAirport, PilotName)
                            VALUES ({passenger_id}, {airport_id}, {date_id}, {status_id}, '{arrival_airport}', '{pilot_name}')
                        """))

                    # Confirmar la transacción si todo fue bien
                    trans.commit()
                    print("Datos cargados correctamente en las tablas de dimensiones y en FactFlights.")
                    
                except Exception as e:
                    # Revertir la transacción en caso de error
                    trans.rollback()
                    print(f"Error al cargar los datos: {e}")
            else:
                print("No se pudo cargar los datos porque no se completó la transformación.")
