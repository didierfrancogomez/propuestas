---
titulo: "Arquitectura Agentes V1.1."
id: 5666930707
espacio: AFGLYP
version: 4
actualizado: 2026-07-28T19:26:00.195Z
actualizado_por: "Daniela Garcia Cataño"
etiquetas: []
ruta: "AI First · Gobierno, Lineamientos y Prácticas > [ARQ] AI First: Arquitectura de referencia y lineamientos > [ARQ] AI First: Arquitectura de referencia"
origen: https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/5666930707
---

# Arquitectura Agentes V1.1.

## Introducción

Esta sección reúne la documentación arquitectónica completa para la construcción de agentes de IA en SURA, en el marco de la estrategia **AI First**. Su objetivo es proporcionar una visión integral —desde los fundamentos conceptuales y las decisiones de diseño, hasta la materialización tecnológica— que permita entender cómo se conciben, diseñan, implementan y operan agentes singulares en la organización.

Esta página actúa como un **punto de entrada** al modelo arquitectónico: resume el propósito del espacio y orienta el recorrido por los documentos detallados. El contenido principal se desarrolla en dos documentos complementarios, alojados como subpáginas:

1. [Arquitectura de Referencia V1.1.](../../paginas/ARQ-AI-First-Arquitectura-de-referencia/Arquitectura-Agentes-V1.1/Arquitectura-de-Referencia-V1.1.md) — Define el *qué* y el *por qué* de la arquitectura de agentes. Parte de los antecedentes y la aproximación AI First, identifica los retos de negocio y técnicos que justifican el uso de agentes, y establece los patrones arquitectónicos (Agente Singular, Agente con Roles, Multi‑Agentes) junto con los modelos de decisión para seleccionar el más adecuado. Presenta las vistas de contexto y contenedores (C4 niveles 1 y 2) del Sistema de Agente Singular, los atributos de calidad priorizados, la ruta de evolución hacia la arquitectura deseada (To‑Be), los lineamientos de gobierno —incluyendo la Matriz de Riesgos de IA— y las prácticas de excelencia en DevOps, LLMOps, evaluación de agentes y gestión de prompts.
2. [Arquitectura de implementación v1.1](../../paginas/ARQ-AI-First-Arquitectura-de-referencia/Arquitectura-Agentes-V1.1/Arquitectura-de-implementacion-v1.1.md) — Define el *cómo* y el *con qué* se materializa la arquitectura de referencia. Presenta la vista de despliegue con el *stack* tecnológico seleccionado (Azure Container Apps, Azure AI Foundry, Cosmos DB, Azure AI Search, Databricks, Apigee), las decisiones clave de implementación —como el rol de AI Foundry como LLM Gateway, la ubicación de Databricks fuera del *runtime* del agente y la elección de Container Apps frente a AKS—, y la vista de componentes (C4 nivel 3) del Orquestador Agente Singular, con el detalle de cada componente interno y los *Legos* MCP Server en Java y Python listos para acelerar nuevos desarrollos.

En términos prácticos, se recomienda el siguiente orden de lectura:

1. Iniciar por la **Arquitectura de Referencia V1.1.** para comprender los principios, decisiones, restricciones de diseño y el modelo conceptual completo.
2. Continuar con la **Arquitectura de implementación v1.1** para entender las decisiones tecnológicas concretas, la arquitectura de despliegue y los componentes reutilizables que permiten llevar la referencia a un entorno real.
