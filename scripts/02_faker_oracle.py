"""
SCRIPT: 02_faker_oracle.py
OBJETIVO:
Generar datos académicos transaccionales en Oracle
(matrículas, asignación de materias y calificaciones),
utilizando datos maestros previamente creados en MariaDB.

Este script representa la lógica real de un sistema académico.
"""

# -----------------------------
# IMPORTS
# -----------------------------
import pymysql
import oracledb
import random
from faker import Faker
from datetime import date
from dotenv import load_dotenv
import os

# -----------------------------
# CARGA DE VARIABLES DE ENTORNO
# -----------------------------
load_dotenv()
fake = Faker("es_ES")

# -----------------------------
# LECTURA DE DATOS MAESTROS DESDE MARIADB
# -----------------------------
# Aquí NO se crean datos, solo se leen IDs existentes
maria_conn = pymysql.connect(
    host=os.getenv("MARIADB_HOST"),
    port=int(os.getenv("MARIADB_PORT")),
    user=os.getenv("MARIADB_USER"),
    password=os.getenv("MARIADB_PASSWORD"),
    database=os.getenv("MARIADB_DB")
)

maria_cur = maria_conn.cursor()

# Obtener IDs de estudiantes
maria_cur.execute("SELECT id_estudiante FROM estudiante")
estudiantes = [row[0] for row in maria_cur.fetchall()]

# Obtener IDs de asignaturas
maria_cur.execute("SELECT id_asignatura FROM asignatura")
asignaturas = [row[0] for row in maria_cur.fetchall()]

# Obtener IDs de docentes
maria_cur.execute("SELECT id_docente FROM docente")
docentes = [row[0] for row in maria_cur.fetchall()]

maria_cur.close()
maria_conn.close()

print(f"✔ Estudiantes leídos: {len(estudiantes)}")
print(f"✔ Asignaturas leídas: {len(asignaturas)}")
print(f"✔ Docentes leídos: {len(docentes)}")

# -----------------------------
# CONEXIÓN A ORACLE
# -----------------------------
dsn = f"{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/{os.getenv('ORACLE_SERVICE')}"

oracle_conn = oracledb.connect(
    user=os.getenv("ORACLE_USER"),
    password=os.getenv("ORACLE_PASSWORD"),
    dsn=dsn
)

oracle_cur = oracle_conn.cursor()

# -----------------------------
# VERIFICAR / CREAR PERÍODO ACADÉMICO
# -----------------------------
oracle_cur.execute(
    "SELECT id_periodo FROM periodo_academico WHERE nombre = :1",
    ("2025-1",)
)

row = oracle_cur.fetchone()

# Si no existe el período, se crea
if row is None:
    oracle_cur.execute(
        """
        INSERT INTO periodo_academico
        (nombre, fecha_inicio, fecha_fin, estado)
        VALUES (:1, :2, :3, 'ACTIVO')
        """,
        ("2025-1", date(2025, 1, 1), date(2025, 6, 30))
    )
    oracle_conn.commit()

    oracle_cur.execute(
        "SELECT id_periodo FROM periodo_academico WHERE nombre = :1",
        ("2025-1",)
    )
    row = oracle_cur.fetchone()

id_periodo = row[0]
print(f"✔ Período académico ID: {id_periodo}")

# -----------------------------
# MATRÍCULAS Y CALIFICACIONES
# -----------------------------
print("⏳ Insertando matrículas y calificaciones...")

contador = 0

for id_estudiante in estudiantes:
    # 1️⃣ Crear matrícula
    oracle_cur.execute(
        """
        INSERT INTO matricula
        (id_estudiante, id_periodo, fecha_matricula, estado)
        VALUES (:1, :2, SYSDATE, 'ACTIVO')
        """,
        (id_estudiante, id_periodo)
    )

    # 2️⃣ Obtener ID de la matrícula recién creada
    oracle_cur.execute(
        """
        SELECT MAX(id_matricula)
        FROM matricula
        WHERE id_estudiante = :1
        """,
        (id_estudiante,)
    )
    id_matricula = oracle_cur.fetchone()[0]

    # 3️⃣ Asignar 3 materias aleatorias
    for id_asignatura in random.sample(asignaturas, 3):
        id_docente = random.choice(docentes)

        oracle_cur.execute(
            """
            INSERT INTO matricula_asignatura
            (id_matricula, id_asignatura, id_docente)
            VALUES (:1, :2, :3)
            """,
            (id_matricula, id_asignatura, id_docente)
        )

        # 4️⃣ Generar calificaciones
        p1 = round(random.uniform(5, 10), 2)
        p2 = round(random.uniform(5, 10), 2)
        final = round((p1 + p2) / 2, 2)

        oracle_cur.execute(
            """
            INSERT INTO calificacion
            (id_matricula, id_asignatura, nota_parcial_1,
             nota_parcial_2, nota_final, estado)
            VALUES (:1, :2, :3, :4, :5, :6)
            """,
            (
                id_matricula,
                id_asignatura,
                p1,
                p2,
                final,
                "APROBADO" if final >= 7 else "REPROBADO"
            )
        )

    contador += 1

    # Commit por bloques para evitar sobrecarga
    if contador % 100 == 0:
        oracle_conn.commit()
        print(f"✔ {contador} matrículas procesadas")

oracle_conn.commit()

oracle_cur.close()
oracle_conn.close()

print("🎉 Oracle poblado correctamente con lógica académica")
