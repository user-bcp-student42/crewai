---
name: hexagonal
description: Reglas para desarrollar el backend con arquitectura hexagonal (puertos y adaptadores).
---

# Arquitectura hexagonal

Organiza el código bajo `pe.bcp.login` en estas capas:

- `domain/model`: entidades puras, sin dependencias de framework.
- `domain/port/input`: interfaces de casos de uso.
- `domain/port/output`: interfaces hacia repositorios y APIs externas.
- `application/service`: implementa los puertos de entrada y depende solo de `domain`.
- `infrastructure/adapter/input`: recursos REST.
- `infrastructure/adapter/output`: repositorios y clientes externos que implementan los puertos de salida.
- `infrastructure/config`: configuración y beans.

## Reglas

1. Las dependencias solo van hacia adentro: `infrastructure -> application -> domain`.
2. `domain` y `application` nunca importan `infrastructure`.
3. El recurso REST invoca un puerto de entrada, nunca un repositorio.
4. El servicio usa puertos de salida; el adaptador los implementa.
5. Cada archivo Java empieza con `// Nombre.java` y su `package` refleja la capa.
