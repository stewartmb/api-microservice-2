from fastapi import FastAPI
import mysql.connector
import schemas

app = FastAPI()

host_name = "52.204.168.191" # CAMBIAR!!!!!!
port_number = "8008" 
user_name = "root"
password_db = "utec"
database_name = "bd_api_python" 

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

# Anadir un nuevo profesor
@app.post("/profesores")
def add_profesor(item:schemas.Item):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    nombre = item.nombre
    especialidad = item.especialidad
    dni = item.dni
    telefono = item.telefono
    cursor = mydb.cursor()
    sql = "INSERT INTO Profesor (nombre, especialidad, dni, telefono) VALUES (%s, %s, %s, %s)"
    val = (nombre,especialidad,dni,telefono)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()
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

# Anadir un nuevo profesor
@app.post("/cursos")
def add_profesor(item:schemas.Item2):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
    nombre_curso = item.nomc
    num_credits = item.numc
    cursor = mydb.cursor()
    sql = "INSERT INTO Curso (nombre_curso, num_creditos) VALUES (%s, %s)"
    val = (nombre_curso,num_credits)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()
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
    return {"message": "Curso deleted successfully"}