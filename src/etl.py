from pathlib import Path
import pyodbc

# Configuración de la conexión a SQL Server
servidor = "localhost"
base_datos = "etl_practica1"
usuario = "sa"
contrasena = "BaseDatos2+"
cadena_conexion = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={servidor};"
    f"DATABASE={base_datos};"
    f"UID={usuario};"
    f"PWD={contrasena}"
)

# Función para ejecutar un script SQL
def ejecutar_script_sql(ruta_script):
    if not ruta_script:
        print("Ruta nula")
        return

    try:
        # Crear una conexión a la base de datos
        with pyodbc.connect(cadena_conexion) as conexion:
            # Crear un cursor
            with conexion.cursor() as cursor:
                # Leer y ejecutar el script SQL
                with open(ruta_script, "r", encoding="utf-8") as archivo:
                    script_sql = archivo.read().strip()
                    instrucciones_sql = script_sql.split(";")
                    for instruccion in instrucciones_sql:
                        instruccion_limpia = instruccion.strip()
                        if instruccion_limpia:
                            cursor.execute(instruccion_limpia)
                            if cursor.description:
                                columnas = [columna[0] for columna in cursor.description]
                                print(" | ".join(columnas))
                                print("-" * 50)
                                filas = cursor.fetchall()
                                for fila in filas:
                                    print(" | ".join(str(valor) for valor in fila))
                                print("-" * 50)
                conexion.commit()
                print("Todos los scripts se ejecutaron correctamente.")
    except Exception as error:
        # Manejo de errores
        print(f"Ocurrió un error: {error}")

# Función para extraer información y obtener las rutas de los scripts SQL
def extraer_informacion(ruta_borrar_modelo, ruta_crear_modelo, ruta_cargar_info, ruta_consultas):
    menu_extraer = """
1. Script para Borrar Modelo
2. Script para Crear Modelo
3. Script para Cargar Información
4. Script para Consultas
5. Salir
"""
    while True:
        print(menu_extraer)
        try:
            opcion = int(input("Selecciona una opción: "))
            if opcion == 1:
                ruta_borrar_modelo = Path(input("Ruta del script para borrar modelo: ")).resolve()
                print(ruta_borrar_modelo)
            elif opcion == 2:
                ruta_crear_modelo = Path(input("Ruta del script para crear modelo: ")).resolve()
                print(ruta_crear_modelo)
            elif opcion == 3:
                ruta_cargar_info = Path(input("Ruta del script para cargar información: ")).resolve()
                print(ruta_cargar_info)
            elif opcion == 4:
                ruta_consultas = Path(input("Ruta del script para consultas: ")).resolve()
                print(ruta_consultas)
            elif opcion == 5:
                return ruta_borrar_modelo, ruta_crear_modelo, ruta_cargar_info, ruta_consultas
            else:
                print("Opción no válida")
        except ValueError:
            print("Opción no válida")

def main():
    ruta_borrar_modelo = None
    ruta_crear_modelo = None
    ruta_cargar_info = None
    ruta_consultas = None

    menu_principal = """
1. Borrar Modelo
2. Crear Modelo
3. Extraer Información
4. Cargar Información
5. Consultas
6. Salir
"""
    while True:
        print(menu_principal)
        try:
            opcion = int(input("Selecciona una opción: "))
            if opcion == 1:
                ejecutar_script_sql(ruta_borrar_modelo)
            elif opcion == 2:
                ejecutar_script_sql(ruta_crear_modelo)
            elif opcion == 3:
                ruta_borrar_modelo, ruta_crear_modelo, ruta_cargar_info, ruta_consultas = extraer_informacion(
                    ruta_borrar_modelo, ruta_crear_modelo, ruta_cargar_info, ruta_consultas
                )
            elif opcion == 4:
                ejecutar_script_sql(ruta_cargar_info)
            elif opcion == 5:
                ejecutar_script_sql(ruta_consultas)
            elif opcion == 6:
                break
            else:
                print("Opción no válida")
        except ValueError:
            print("Opción no válida")

if __name__ == "__main__":
    main()
