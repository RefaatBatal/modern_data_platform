# Modern Data Platform

End-to-end data platform built from scratch using modern open-source tools.

## Architecture

Open-Meteo API (Free Weather Data)
    -> Python Extract (Airflow DAG)
    -> PostgreSQL (Raw Data)
    -> dbt (Transformations + Tests)
    -> PostgreSQL (Clean Data)
    -> Grafana (Dashboards + Monitoring)

## Tech Stack

- Orchestration: Apache Airflow
- Transformation: dbt (data build tool)
- Database: PostgreSQL
- Monitoring: Grafana
- Containerization: Docker

## Getting Started

Start all services: docker-compose up -d

Run dbt models: cd dbt && dbt run && dbt test

Access Grafana: http://localhost:3000

## Project Status

Work in progress - transforming from Fundamentals to Production-ready