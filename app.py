from fastapi import FastAPI
import mysql.connector
import schemas
import boto3
import csv
import os

app = FastAPI()

# Variables de conexión MySQL
host_name = "3.232.249.9"
port_number = "8008"
user_name = "root"
password_db = "utec"
database_name = "bd_api_python"

# Parámetros para S3
bucket_name = "proyecto-uni"
profesor_file = "profesor.csv"
curso_file = "curso.csv"

# Conectar a AWS S3
s3 = boto3.client('s3')

# Función para exportar datos de una tabla específica a CSV y subir a S3
def export_table_to_csv_and_s3(table_name, file_name):
    conexion = mysql.connector.connect(
        host=host_name,
        port=port_number,
        user=user_name,
        password=password_db,
        database=database_name
    )
    
    cursor = conexion.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    resultados = cursor.fetchall()

    # Escribir los resultados en un archivo CSV
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])  # Escribir el encabezado
        writer.writerows(resultados)  # Escribir los datos

    cursor.close()
    conexion.close()

    # Subir el archivo CSV al bucket S3
    s3.upload_file(file_name, bucket_name, file_name)
    print(f"Archivo {file_name} subido a S3.")

    # Eliminar archivo local una vez subido
    os.remove(file_name)


@app.get("/")
def get_echo_test():
    return {"message": "Echo Test OK"}


# Profesor API:

# Get all profesores
@app.get("/profesores")
def get_profesores():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Profesor")
    result = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"Profesor": result}


# Get un profesor by ID
@app.get("/profesores/{id}")
def get_profesor(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM Profesor WHERE idProfesor = {id}")
    result = cursor.fetchone()
    cursor.close()
    mydb.close()
    return {"Profesor": result}

# Añadir un nuevo profesor
@app.post("/profesores")
def add_profesor(item: schemas.Item):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    nombre = item.nombre
    especialidad = item.especialidad
    dni = item.dni
    telefono = item.telefono
    cursor = mydb.cursor()
    sql = "INSERT INTO Profesor (nombre, especialidad, dni, telefono) VALUES (%s, %s, %s, %s)"
    val = (nombre, especialidad, dni, telefono)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()

    # Exportar los datos de la tabla Profesor a CSV y subir a S3
    export_table_to_csv_and_s3("Profesor", profesor_file)

    return {"message": "Profesor added successfully"}

# Eliminar un profesor
@app.delete("/profesores/{id}")
def delete_profesores(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM Profesor WHERE idProfesor = {id}")
    mydb.commit()
    cursor.close()
    mydb.close()

    # Exportar los datos de la tabla Profesor a CSV y subir a S3
    export_table_to_csv_and_s3("Profesor", profesor_file)

    return {"message": "Profesor deleted successfully"}


# Curso API:

# Get all cursos
@app.get("/cursos")
def get_cursos():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Curso")
    result = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"Curso": result}


# Get un curso by ID
@app.get("/cursos/{id}")
def get_curso(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM Curso WHERE idCurso = {id}")
    result = cursor.fetchone()
    cursor.close()
    mydb.close()
    return {"Curso": result}

# Añadir un nuevo curso
@app.post("/cursos")
def add_curso(item: schemas.Item2):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    nombre_curso = item.nomc
    num_credits = item.numc
    cursor = mydb.cursor()
    sql = "INSERT INTO Curso (nombre_curso, num_creditos) VALUES (%s, %s)"
    val = (nombre_curso, num_credits)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()

    # Exportar los datos de la tabla Curso a CSV y subir a S3
    export_table_to_csv_and_s3("Curso", curso_file)

    return {"message": "Curso added successfully"}

#Eliminar un curso
@app.delete("/cursos/{id}")
def delete_cursos(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM Curso WHERE idCurso = {id}")
    mydb.commit()
    cursor.close()
    mydb.close()

    # Exportar los datos de la tabla Curso a CSV y subir a S3
    export_table_to_csv_and_s3("Curso", curso_file)

    return {"message": "Curso deleted successfully"}
