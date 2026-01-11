Plataforma de Base de Datos Heterogénea

Este repositorio contiene la implementación de una plataforma de bases de datos heterogénea que integra MariaDB, Oracle y SQL Server mediante una capa de interconexión automatizada (ETL) ejecutada sobre un servidor Ubuntu.

Arquitectura

MariaDB: Repositorio de datos maestros (estudiantes, docentes y asignaturas).

Oracle: Base de datos transaccional académica (matrículas y calificaciones).

SQL Server: Repositorio analítico consolidado (modelo dimensional).

Ubuntu Server: Capa ETL y automatización mediante tareas programadas.

Requisitos

Docker y Docker Compose

Python 3

Acceso a instancias de MariaDB, Oracle y SQL Server

Ubuntu Server 22.04

Configuración
1. Clonar el repositorio
git clone https://github.com/USUARIO/db-plataforma-heterogenea.git
cd db-plataforma-heterogenea

2. Configurar variables de entorno

Crear un archivo .env a partir del archivo de ejemplo:

cp .env.example .env


Editar el archivo .env y definir las credenciales y parámetros de conexión de los tres motores de bases de datos:

# MariaDB
MARIADB_HOST=
MARIADB_PORT=
MARIADB_DB=
MARIADB_USER=
MARIADB_PASSWORD=

# Oracle
ORACLE_HOST=
ORACLE_PORT=
ORACLE_SERVICE=
ORACLE_USER=
ORACLE_PASSWORD=

# SQL Server
SQLSERVER_HOST=
SQLSERVER_PORT=
SQLSERVER_DB=
SQLSERVER_USER=
SQLSERVER_PASSWORD=


Nota: Las credenciales no se encuentran hardcodeadas en los scripts, sino que se cargan dinámicamente desde este archivo mediante variables de entorno, siguiendo buenas prácticas de seguridad.

3. Instalar dependencias Python
pip install -r requirements.txt


(o instalar manualmente las librerías necesarias si no se utiliza requirements.txt)

Orden de ejecución de los scripts

Los scripts deben ejecutarse en el siguiente orden:

01_faker_mariadb.py
Genera datos maestros iniciales en MariaDB.

02_faker_oracle.py
Genera datos académicos iniciales en Oracle utilizando identificadores existentes.

03_etl_sqlserver.py
Consolida la información desde MariaDB y Oracle hacia SQL Server.

Automatización del proceso ETL

El script 03_etl_sqlserver.py se ejecuta de forma automática y periódica mediante una tarea programada (cron) en el servidor Ubuntu.

Configuración de la tarea cron

Editar el crontab del usuario:

crontab -e


Agregar la siguiente línea:

* * * * * /usr/bin/python3 /home/usuario/db-plataforma-heterogenea/scripts/03_etl_sqlserver.py >> /home/usuario/db-plataforma-heterogenea/etl.log 2>&1


Esta configuración ejecuta el proceso ETL cada minuto, permitiendo que los cambios realizados en las bases de datos origen se reflejen automáticamente en el repositorio consolidado de SQL Server.

Automatización y funcionamiento

El uso de tareas programadas permite que la capa de interconexión funcione de manera continua y sin intervención manual, cumpliendo con el objetivo de integrar de forma automática una plataforma de bases de datos heterogénea.
