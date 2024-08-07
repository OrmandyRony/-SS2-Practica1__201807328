# [SS2] Primera Práctica de Laboratorio - Proceso ETL

## Universidad de San Carlos de Guatemala
**Facultad de Ingeniería - Escuela de Ciencias y Sistemas**  
**Seminario de Sistemas 2 - Segundo Semestre 2024**  
**Catedráticos:**  
- Ing. Luis Alberto Vettorazzi Espana  
- Ing. Fernando Jose Paz Gonzales  
**Auxiliares:**  
- Aux. Jose Fernando Alvarez Morales  
- Aux. Sergio Enrique Cubur  

---

## Descripción General

Esta práctica se centra en el desarrollo de un proceso ETL (Extract, Transform, Load) utilizando Python y SQL Server. El objetivo es extraer datos de archivos proporcionados, transformarlos y cargarlos en un modelo de datos previamente diseñado. Además, se deben realizar consultas específicas sobre los datos cargados.

## Estructura del Proyecto

- **database/**: Contiene scripts SQL para la creación y eliminación de las tablas del modelo de datos.
- **input/**: Carpeta destinada a almacenar los archivos de entrada que se utilizarán en el proceso ETL.
- **src/**: Contiene el código fuente en Python que realiza las operaciones ETL.
- **.gitignore**: Archivo de configuración para evitar la inclusión de archivos no deseados en el control de versiones.
- **docker-sql-server.ps1**: Script de PowerShell para configurar un contenedor Docker con SQL Server.
- **output_results.txt**: Archivo donde se almacenan los resultados de las consultas realizadas.
- **Pipfile**: Archivo para la gestión de dependencias del proyecto utilizando Pipenv.
- **Pipfile.lock**: Archivo de bloqueo de dependencias generado por Pipenv.
- **README.md**: Este archivo, que proporciona una descripción general del proyecto y sus instrucciones de uso.

## Funcionalidades Principales

1. **Borrar Modelo**: Elimina cualquier tabla que haya sido creada previamente.
2. **Crear Modelo**: Crea las tablas necesarias para almacenar los datos transformados.
3. **Extraer Información**: Extrae los datos de los archivos de entrada.
4. **Cargar Información**: Transforma los datos extraídos y los carga en las tablas creadas.
5. **Realizar Consultas**: Ejecuta consultas sobre los datos cargados y guarda los resultados en `output_results.txt`.

## Requisitos

- **Python 3.x**: Lenguaje de programación utilizado para la implementación del proceso ETL.
- **SQL Server**: Sistema de gestión de bases de datos utilizado para almacenar los datos transformados.
- **Docker**: Utilizado para ejecutar SQL Server en un contenedor.
- **Pipenv**: Utilizado para la gestión de dependencias del proyecto.

## Ejecución del Proyecto

1. **Instalación de Dependencias:**
   ```sh
   pipenv install
