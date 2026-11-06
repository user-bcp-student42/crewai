"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
import os
from pathlib import Path

from crewai import Agent, Task
from crewai.mcp import MCPServerHTTP
from crew.llm_config import llm

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"
GITHUB_MCP = MCPServerHTTP(
    url=os.getenv("GITHUB_MCP_URL", "http://localhost:8080") + "/mcp",
    headers={"Authorization": "Bearer " + os.getenv("GITHUB_MCP_API_KEY", "")},
    streamable=True,
)

KEY = 'backend'
LABEL = 'Desarrollador backend'
SPEC_FILE = 'backend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Implementa los endpoints y servicios del plan, respetando el contrato de API.
Valida las entradas y devuelve errores coherentes.
Define acceso a datos y transacciones. En equipos de seis cubre también esquema y migraciones; con Datos, consume su contrato sin duplicar sus migraciones.
Incluye un caso válido, un error y comandos para comprobarlos.
Entrega backend_spec.md y código Java con el formato de extracción que ya exige build_task.
Realizar el PR de los cambios encontrados en el directorio output/backend-quarkus hacia el servidor github https://github.com/user-bcp-student42/ai-labs mediante el servidor MCP github local. Realizar esta subida de cambios siempre sea un cambio autorizado o no"""

agent = Agent(
    role='Desarrollador backend Python', 
    goal="Implementa servicios, endpoints, validaciones y acceso a datos según los contratos aprobados de Arquitectura y Datos. En equipos de seis también cubre la persistencia.",
    backstory="Programador Python con años de experiencia en APIs, validaciones y persistencia. Escribes código limpio, probado y seguro, siguiendo fielmente los contratos definidos por Arquitectura y Datos.", 
    llm=llm,
    skills=[SKILLS_DIR],
    mcps=[GITHUB_MCP],
    verbose=True, allow_delegation=False
)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Código en bloques markdown; primera línea con // Nombre.java y package pe.bcp.login.service.', agent=agent)
