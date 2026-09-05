---
titulo: "Separación de Suscripciones entre Dominio de Agentes y Dominio de Información/Conocimiento"
id: 6150193162
espacio: AFGLYP
version: 1
actualizado: 2026-07-28T19:30:09.033Z
actualizado_por: "Daniela Garcia Cataño"
etiquetas: []
ruta: "AI First · Gobierno, Lineamientos y Prácticas > [ARQ] AI First: Arquitectura de referencia y lineamientos > [LIN] Infraestructura"
origen: https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/6150193162
---

# Separación de Suscripciones entre Dominio de Agentes y Dominio de Información/Conocimiento

## Objetivo

Establecer la segmentación obligatoria de suscripciones cloud para las soluciones de IA, separando las capacidades de agentes de los activos de información y conocimiento, con el fin de garantizar un modelo escalable, seguro, gobernado y financieramente controlado.

---

## :edit:

Toda solución de IA deberá implementar una separación explícita entre las suscripciones que soportan las capacidades de agentes y aquellas que soportan los activos de información o conocimiento.

Esta separación constituye un principio estructural de arquitectura y gobierno, permitiendo que cada dominio evolucione, opere y sea gestionado de manera independiente.

---

## :building_construction:

### :robot-face:

Contiene los componentes responsables de la ejecución y comportamiento de los agentes de IA.

Ejemplos:

| **Componente** |
| --- |
| Agentes y asistentes |
| Servicios de orquestación |
| Prompts y herramientas |
| Capacidades de automatización |
| Observabilidad y monitoreo de agentes |
| Configuraciones de modelos |

**Propósito:** habilitar la capacidad de razonamiento, interacción y ejecución de acciones.

---

### :books:

Contiene los componentes responsables de almacenar, procesar, gobernar y disponibilizar información utilizada por los agentes.

Ejemplos:

| **Componente** |
| --- |
| Productos de datos |
| Procesos de indexación |
| Bases de conocimiento |
| Vector stores |
| Catálogos semánticos |
| Documentos y repositorios especializados |

Ejemplos:

- `indexacionia-dll`
- `cotizadomovi-dll`

**Propósito:** gestionar el conocimiento y los activos de información de forma independiente a los consumidores de dicho conocimiento.

---

## :blue-star:

### :handshake:

Permite asignar propietarios distintos para:

| **Área** |
| --- |
| Plataformas de agentes |
| Productos de datos |
| Bases de conocimiento |
| Infraestructura asociada |

---

### :shield:

Facilita:

| **Aspecto** | **Beneficio** |
| --- | --- |
| Controles de acceso | Diferenciados |
| Aislamiento de información | Sensible |
| Auditoría | De accesos y consumos |
| Aplicación de políticas | Específicas por dominio |

---

### :blue-star:

Permite identificar y controlar de forma independiente:

| **Tipo de Costo** |
| --- |
| Costos de ejecución de agentes |
| Costos de almacenamiento e indexación |
| Costos de procesamiento de datos |
| Costos asociados al consumo de IA |

---

### Evolución independiente

Los dominios pueden evolucionar sin generar dependencias innecesarias:

- Un mismo dominio de conocimiento puede ser consumido por múltiples agentes.
- Un agente puede consumir múltiples dominios de conocimiento.
- Los cambios en conocimiento no requieren cambios en los agentes y viceversa.

---

## :forbidden:

> **[NOTA]**
> No está permitido:
>
>
> - Alojar agentes y activos de conocimiento dentro de la misma suscripción sin una justificación arquitectónica aprobada.
> - Acoplar el ciclo de vida de los agentes al ciclo de vida de los productos de datos o dominios de conocimiento.
> - Asignar la propiedad de los activos de conocimiento al equipo responsable del agente cuando ambos dominios tengan responsabilidades distintas.
