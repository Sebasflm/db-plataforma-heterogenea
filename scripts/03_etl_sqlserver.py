"""
SCRIPT: 03_etl_sqlserver.py
OBJETIVO:
Consolidar datos académicos desde MariaDB y Oracle
hacia SQL Server utilizando un modelo dimensional.

Este script representa el proceso ETL del sistema.
"""

# -----------------------------
# IMPORTS
# -----------------------------
import pymysql
import oracledb
import pyodbc
from dotenv import load_dotenv
import os

# -----------------------------
# CARGA DE VARIABLES DE ENTORNO
# -----------------------------
load_dotenv()

# -----------------------------
# CONEXIÓN A SQL SERVER (DESTINO)
# -----------------------------
sqlserver_conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={os.getenv('SQLSERVER_HOST')},{os.getenv('SQLSERVER_PORT')};"
    f"DATABASE={os.getenv('SQLSERVER_DB')};"
    f"UID={os.getenv('SQLSERVER_USER')};"
    f"PWD={os.getenv('SQLSERVER_PASSWORD')};"
    f"TrustServerCertificate=yes;"
)
sql_cur = sqlserver_conn.cursor()

# -----------------------------
# LIMPIEZA DE TABLAS (REEJECUTABLE)
# -----------------------------
print("🧹 Limpiando tablas en SQL Server...")

sql_cur.execute("DELETE FROM fact_calificaciones")
sql_cur.execute("DELETE FROM dim_estudiante")
sql_cur.execute("DELETE FROM dim_docente")
sql_cur.execute("DELETE FROM dim_asignatura")
sql_cur.execute("DELETE FROM dim_periodo")

sqlserver_conn.commit()

# -----------------------------
# CONEXIÓN A MARIADB (MAESTROS)
# -----------------------------
maria_conn = pymysql.connect(
    host=os.getenv("MARIADB_HOST"),
    port=int(os.getenv("MARIADB_PORT")),
    user=os.getenv("MARIADB_USER"),
    password=os.getenv("MARIADB_PASSWORD"),
    database=os.getenv("MARIADB_DB")
)
maria_cur = maria_conn.cursor()

# -----------------------------
# CARGA DIM_ESTUDIANTE
# -----------------------------
print("📥 Cargando dim_estudiante...")

maria_cur.execute("SELECT id_estudiante, carrera FROM estudiante")
for id_est, carrera in maria_cur.fetchall():
    sql_cur.execute(
        "INSERT INTO dim_estudiante VALUES (?, ?)",
        id_est, carrera
    )

# -----------------------------
# CARGA DIM_DOCENTE
# -----------------------------
print("📥 Cargando dim_docente...")

maria_cur.execute("SELECT id_docente, especialidad FROM docente")
for id_doc, esp in maria_cur.fetchall():
    sql_cur.execute(
        "INSERT INTO dim_docente VALUES (?, ?)",
        id_doc, esp
    )

# -----------------------------
# CARGA DIM_ASIGNATURA
# -----------------------------
print("📥 Cargando dim_asignatura...")

maria_cur.execute("SELECT id_asignatura, nombre, creditos FROM asignatura")
for id_asg, nom, cred in maria_cur.fetchall():
    sql_cur.execute(
        "INSERT INTO dim_asignatura VALUES (?, ?, ?)",
        id_asg, nom, cred
    )

maria_cur.close()
maria_conn.close()

# -----------------------------
# CONEXIÓN A ORACLE (TRANSACCIONAL)
# -----------------------------
dsn = f"{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/{os.getenv('ORACLE_SERVICE')}"

oracle_conn = oracledb.connect(
    user=os.getenv("ORACLE_USER"),
    password=os.getenv("ORACLE_PASSWORD"),
    dsn=dsn
)
oracle_cur = oracle_conn.cursor()

# -----------------------------
# CARGA DIM_PERIODO
# -----------------------------
print("📥 Cargando dim_periodo...")

oracle_cur.execute("SELECT id_periodo, nombre FROM periodo_academico")
for id_per, nom in oracle_cur.fetchall():
    sql_cur.execute(
        "INSERT INTO dim_periodo VALUES (?, ?)",
        id_per, nom
    )

sqlserver_conn.commit()

# -----------------------------
# CARGA FACT_CALIFICACIONES
# -----------------------------
print("📥 Cargando fact_calificaciones...")

oracle_cur.execute(
    """
    SELECT
        m.id_estudiante,
        ma.id_docente,
        c.id_asignatura,
        m.id_periodo,
        c.nota_final,
        c.estado
    FROM matricula m
    JOIN matricula_asignatura ma ON m.id_matricula = ma.id_matricula
    JOIN calificacion c
      ON c.id_matricula = m.id_matricula
     AND c.id_asignatura = ma.id_asignatura
    """
)

contador = 0

for row in oracle_cur.fetchall():
    sql_cur.execute(
        """
        INSERT INTO fact_calificaciones
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        row
    )
    contador += 1

sqlserver_conn.commit()

oracle_cur.close()
oracle_conn.close()
sql_cur.close()
sqlserver_conn.close()

print(f"🎉 ETL finalizado correctamente ({contador} registros en fact_calificaciones)")
