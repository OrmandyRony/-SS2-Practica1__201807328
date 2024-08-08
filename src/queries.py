import pandas as pd
from sqlalchemy import create_engine

def run_queries():
    # Configuración de la conexión a SQL Server
    server = 'ORMANDYRONY'# Cambia esto según tu configuración
    database = 'AviationDW'# Cambia esto según tu configuración
    username = 'admin'# Cambia esto según tu configuración
    password = 'admin'# Cambia esto según tu configuración
    driver = 'ODBC Driver 17 for SQL Server'

    engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}')

    # Revisar la conexión y ejecutar las consultas
    with engine.connect() as connection:
        print("Conexión exitosa.")
        
        # Definir las consultas
        queries = {
            "Total Flights": """
                SELECT COUNT(*) AS TotalFlights FROM FactFlights;
            """,
            "Passengers by Gender": """
                SELECT Gender, COUNT(*) AS TotalPassengers 
                FROM DimPassenger 
                GROUP BY Gender;
            """,
            "Flights by Country": """
                SELECT AirportCountryCode, COUNT(*) AS TotalFlights 
                FROM DimAirport a 
                JOIN FactFlights f ON a.AirportID = f.AirportID 
                GROUP BY AirportCountryCode;
            """,
            "Top 5 Airports by Passengers": """
                SELECT TOP 5 AirportName, COUNT(*) AS PassengerCount 
                FROM DimAirport a 
                JOIN FactFlights f ON a.AirportID = f.AirportID 
                GROUP BY AirportName 
                ORDER BY PassengerCount DESC;
            """,
            "Flight Status Count": """
                SELECT FlightStatus, COUNT(*) AS TotalFlights 
                FROM DimFlightStatus s 
                JOIN FactFlights f ON s.StatusID = f.StatusID 
                GROUP BY FlightStatus;
            """,
            "Top 5 Most Visited Countries": """
                SELECT TOP 5 AirportCountryCode, COUNT(*) AS VisitCount 
                FROM DimAirport a 
                JOIN FactFlights f ON a.AirportID = f.AirportID 
                GROUP BY AirportCountryCode 
                ORDER BY VisitCount DESC;
            """,
            "Top 5 Most Visited Continents": """
                SELECT TOP 5 AirportContinent, COUNT(*) AS VisitCount 
                FROM DimAirport a 
                JOIN FactFlights f ON a.AirportID = f.AirportID 
                GROUP BY AirportContinent 
                ORDER BY VisitCount DESC;
            """,
            "Top 5 Ages by Gender": """
                SELECT TOP 5 Gender, Age, COUNT(*) AS FlightCount 
                FROM DimPassenger p 
                JOIN FactFlights f ON p.PassengerID = f.PassengerID 
                GROUP BY Gender, Age 
                ORDER BY FlightCount DESC;
            """,
            "Flight Count by Month and Year": """
                SELECT CONCAT(MONTH(DepartureDate), '-', YEAR(DepartureDate)) AS MonthYear, COUNT(*) AS TotalFlights 
                FROM DimDate d 
                JOIN FactFlights f ON d.DateID = f.DateID 
                GROUP BY MONTH(DepartureDate), YEAR(DepartureDate) 
                ORDER BY YEAR(DepartureDate), MONTH(DepartureDate);
            """
        }

        # Ejecutar las consultas y guardar los resultados
        results = []
        for query_name, query in queries.items():
            result = pd.read_sql(query, con=engine)
            results.append((query_name, result))

        # Guardar los resultados en un archivo de texto
        with open('logs/query_results.txt', 'w') as file:
            for query_name, result in results:
                file.write(f"Consulta: {query_name}\n")
                file.write(result.to_string(index=False))
                file.write("\n\n")
                
        print("Consultas ejecutadas y resultados guardados en logs/query_results.txt.")
