"""
SCRIPT: 01_faker_mariadb.py
OBJETIVO:
Poblar la base de datos MariaDB con datos maestros académicos
(estudiantes, docentes y asignaturas) utilizando Faker.

Este script se ejecuta directamente en el servidor Ubuntu y
no depende de ningún otro motor.
"""

# -----------------------------
# IMPORTS
# -----------------------------
from faker import Faker
import pymysql
import random
from dotenv import load_dotenv
import os

# -----------------------------
# CARGA DE VARIABLES DE ENTORNO
# -----------------------------
# Lee el archivo .env ubicado en el mismo directorio
load_dotenv()

# Inicializa Faker en español
fake = Faker("es_ES")

# -----------------------------
# CONEXIÓN A MARIADB
# -----------------------------
conn = pymysql.connect(
    host=os.getenv("MARIADB_HOST"),
    port=int(os.getenv("MARIADB_PORT")),
    user=os.getenv("MARIADB_USER"),
    password=os.getenv("MARIADB_PASSWORD"),
    database=os.getenv("MARIADB_DB"),
    autocommit=True  # Commit automático por simplicidad
)

cursor = conn.cursor()

# -----------------------------
# INSERCIÓN DE ESTUDIANTES
# -----------------------------
print("📌 Insertando estudiantes en MariaDB...")

for _ in range(5000):
    cursor.execute(
        """
        INSERT INTO estudiante
        (cedula, nombres, apellidos, correo, telefono, carrera)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            fake.unique.numerify("##########"),   # Cédula única
            fake.first_name(),                    # Nombre
            fake.last_name(),                     # Apellido
            fake.unique.email(),                  # Correo único
            fake.phone_number(),                  # Teléfono
            random.choice([
                "Ingeniería en Sistemas",
                "Ingeniería en Software",
                "Ingeniería en Telecomunicaciones"
            ])
        )
    )

print("✔ Estudiantes insertados")

# -----------------------------
# INSERCIÓN DE DOCENTES
# -----------------------------
print("📌 Insertando docentes...")

for _ in range(300):
    cursor.execute(
        """
        INSERT INTO docente
        (nombres, apellidos, correo, especialidad)
        VALUES (%s, %s, %s, %s)
        """,
        (
            fake.first_name(),
            fake.last_name(),
            fake.unique.email(),
            random.choice([
                "Bases de Datos",
                "Programación",
                "Redes",
                "Seguridad Informática"
            ])
        )
    )

print("✔ Docentes insertados")

# -----------------------------
# INSERCIÓN DE ASIGNATURAS
# -----------------------------
print("📌 Insertando asignaturas...")

for i in range(200):
    cursor.execute(
        """
        INSERT INTO asignatura
        (codigo, nombre, creditos)
        VALUES (%s, %s, %s)
        """,
        (
            f"ASG{i+1:03}",        # Código único
            fake.catch_phrase(),  # Nombre ficticio
            random.randint(3, 6)  # Créditos
        )
    )

print("✔ Asignaturas insertadas")

# -----------------------------
# CIERRE DE CONEXIÓN
# -----------------------------
cursor.close()
conn.close()

print("🎉 MariaDB poblado correctamente con Faker")
