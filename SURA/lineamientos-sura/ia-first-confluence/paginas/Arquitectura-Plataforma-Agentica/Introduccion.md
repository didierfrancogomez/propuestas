---
titulo: "Introducción"
id: 5823758365
espacio: AFGLYP
version: 1
actualizado: 2026-04-17T21:31:13.865Z
actualizado_por: "Helbert Sebastian Cubillos Avila"
etiquetas: []
ruta: "AI First · Gobierno, Lineamientos y Prácticas > [ARQ] AI First: Arquitectura de referencia y lineamientos > Arquitectura Plataforma Agentica"
origen: https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/5823758365
---

# Introducción

# 1. Objetivo del documento

El presente documento tiene como propósito establecer el Modelo de Evolución de la Arquitectura para la Plataforma Agéntica de SURA, definiendo los principios, lineamientos, mecanismos de control y roadmap de implementación necesarios para operar agentes de IA de manera segura, auditable, escalable y alineada con la estrategia AI-First de la organización.

De manera específica, este documento busca:

- Partir del entendimiento de la situación actual (As-Is) de la arquitectura de Agentes de Sura para entender las definiciones y decisiones de arquitectura existentes y desde este punto evaluar las necesidades de evolución de dicha arquitectura.
- Establecer un roadmap estructurado de implementación, que permita evolucionar desde las implementaciones de las arquitecturas iniciales de hacia una plataforma agéntica empresarial consolidada, gobernada y sostenible.
- Escalar el uso de agentes generativos más allá de casos aislados, consolidando una plataforma común, interoperable y reutilizable que evite fragmentación tecnológica y reduzca riesgos de proliferación descontrolada de soluciones.
- Integrar desarrollos e implementaciones existentes (agentes desarrollados con frameworks y soluciones basadas en LLMs) dentro de un modelo unificado de gobierno, observabilidad y control.
- Brindar lineamientos para el uso óptimo de los componentes y capacidades existentes en la compañía, promoviendo configuraciones arquitectónicas coherentes con la Línea Base de Arquitectura (LBA), maximizando el costo-beneficio y evitando lock-in tecnológico innecesario.
- Sentar las bases para la observabilidad, seguridad y despliegue controlado de todos los componentes involucrados en el ciclo de vida de los agentes, incluyendo LLMs, prompts, memoria, herramientas, datos, pipelines y mecanismos de evaluación.
- Asegurar la alineación con principios de IA Responsable y cumplimiento regulatorio, mediante la incorporación de mecanismos como matriz de riesgos, trazabilidad de decisiones, control de identidad, guardrails y evaluación continua.

# 2. Alcance y audiencia

El documento abarca el diseño conceptual y técnico del core de la plataforma de agentes generativos de SURA, incluyendo la descripción de sus componentes principales, la evaluación de tecnologías candidatas y las recomendaciones de adopción.

El alcance incluye:

- El relevamiento del estado actual.
- La definición de los componentes estructurales de la plataforma para habilitar la creación y uso de agentes.
- La evaluación comparativa de herramientas y tecnologías habilitantes.

Audiencia principal:

- Arquitectos de soluciones y líderes técnicos de SURA involucrados en el diseño y despliegue de soluciones de IA generativa.
- Equipos de infraestructura y operaciones (DevOps / MLOps).
- Áreas de innovación y tecnología que impulsan la adopción de GenAI.
