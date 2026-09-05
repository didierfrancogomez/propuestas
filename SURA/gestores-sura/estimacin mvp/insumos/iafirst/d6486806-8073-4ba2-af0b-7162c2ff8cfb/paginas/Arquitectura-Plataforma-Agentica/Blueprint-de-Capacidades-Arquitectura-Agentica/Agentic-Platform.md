---
titulo: "Agentic Platform"
id: 5827067919
espacio: AFGLYP
version: 7
actualizado: 2026-04-22T13:00:26.519Z
actualizado_por: "Diego Alexander Corredor Quintero"
etiquetas: []
ruta: "AI First · Gobierno, Lineamientos y Prácticas > [ARQ] AI First: Arquitectura de referencia y lineamientos > Arquitectura Plataforma Agentica > Blueprint de Capacidades Arquitectura Agéntica"
origen: https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/5827067919
---

# Agentic Platform

La **plataforma agéntica** es el conjunto de capacidades compartidas que permite construir, exponer, operar y gobernar agentes de IA de forma consistente a nivel empresarial. Su propósito no es reemplazar los dominios de negocio ni concentrar toda la lógica funcional en una sola plataforma, sino ofrecer una base transversal para que múltiples soluciones agénticas consuman de forma reutilizable servicios especializados de acceso a modelos, herramientas, conocimiento, seguridad, observabilidad, evaluación y operación. Esta visión está alineada con la estrategia AI-First de SURA, que plantea que la IA debe incorporarse desde la concepción de las soluciones, con seguridad, observabilidad, memoria, razonamiento y gobierno integrados desde el inicio.

En esta arquitectura, los agentes funcionan como **runtimes cognitivos** alineados a un dominio, mientras la plataforma asume de manera centralizada el gobierno del acceso a modelos y tools, la gestión del ciclo de vida de prompts y evaluaciones, la aplicación de políticas y guardrails, la observabilidad especializada y el control de costos. La referencia To-Be lo resume al afirmar que la arquitectura objetivo consolida una plataforma de IA empresarial donde los agentes consumen servicios especializados provistos por la plataforma tecnológica de la organización.

La separación entre Control Plane, Domain Layer es una decisión que permite distinguir claramente entre:

- Gobierno y administración.
- Ejecución agéntica.
- Exposición de conocimiento y capacidades de negocio.

**A.**[Control  Plane](../../../paginas/Arquitectura-Plataforma-Agentica/Blueprint-de-Capacidades-Arquitectura-Agentica/Agentic-Platform/Control-Plane.md)

**B.**[Domain Layer](../../../paginas/Arquitectura-Plataforma-Agentica/Blueprint-de-Capacidades-Arquitectura-Agentica/Agentic-Platform/Domain-Layer.md)
