# Plataforma de Base de Datos Heterogénea

Este repositorio contiene la implementación de una plataforma de bases de datos heterogénea que integra MariaDB, Oracle y SQL Server mediante una capa de interconexión automatizada.

## Arquitectura
- MariaDB: Datos maestros
- Oracle: Operaciones académicas
- SQL Server: Repositorio analítico
- Ubuntu Server: Capa ETL y automatización

## Requisitos
- Docker y Docker Compose
- Python 3
- Acceso a MariaDB, Oracle y SQL Server
- Ubuntu Server 22.04

## Configuración
1. Clonar el repositorio
2. Crear un archivo `.env` basado en `.env.example`
3. Instalar dependencias Python
4. Ejecutar los scripts en el orden indicado

## Orden de ejecución
1. 01_faker_mariadb.py
2. 02_faker_oracle.py
3. 03_etl_sqlserver.py (automatizado con cron)

## Automatización
El proceso ETL se ejecuta automáticamente cada minuto mediante tareas programadas (cron).

## Diagramas
Los diagramas de arquitectura y despliegue se encuentran en la carpeta `/diagrams`.
