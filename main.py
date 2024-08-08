import os
from src.create_model import create_model
from src.drop_model import drop_model
from src.extract_transform_load import run_etl
from src.queries import run_queries
from src.select_prueba import select_prueba

def main_menu():
    print("### Menú del Proceso ETL ###")
    print("1. Borrar modelo")
    print("2. Crear modelo")
    print("3. Extraer información")
    print("4. Cargar información")
    print("5. Realizar consultas")
    print("6. Prueba")
    print("0. Salir")
    return input("Seleccione una opción: ")

def main():
    while True:
        choice = main_menu()

        if choice == '1':
            print("Borrando el modelo...")
            drop_model()
        elif choice == '2':
            print("Creando el modelo...")
            create_model()
        elif choice == '3':
            print("Extrayendo información...")
            run_etl('extract')
        elif choice == '4':
            print("Cargando información...")
            run_etl('load')
        elif choice == '5':
            print("Ejecutando consultas...")
            run_queries()
        elif choice == '6':
            print("Realizando prueba...")
            select_prueba()
        elif choice == '0':
            print("Saliendo...")
            break
        else:
            print("Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    main()
