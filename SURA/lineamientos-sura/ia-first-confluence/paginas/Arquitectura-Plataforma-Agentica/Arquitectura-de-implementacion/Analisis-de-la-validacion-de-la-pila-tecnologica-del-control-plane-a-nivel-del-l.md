---
titulo: "Análisis de la validación de la pila tecnológica del control plane a nivel del licencimiento"
id: 6266486824
espacio: AFGLYP
version: 4
actualizado: 2026-09-04T19:04:44.284Z
actualizado_por: "Víctor Daniel Martínez Olier"
etiquetas: []
ruta: "AI First · Gobierno, Lineamientos y Prácticas > [ARQ] AI First: Arquitectura de referencia y lineamientos > Arquitectura Plataforma Agentica > Arquitectura de implementación"
origen: https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/6266486824
---

# Análisis de la validación de la pila tecnológica del control plane a nivel del licencimiento

<!-- [macro: tabla de contenido] -->

## Preliminares

Para la materialización de la plataforma agéntica se ha uso de componentes tecnológicos Open Source que soportan capacidades fundamentales en la arquitectura, tanto en la capa de dominio, como el control plane. Este análisis no cubre la pertinencia técnica de ningún componente definido en la arquitectura, ni aspectos legales que se derivan del uso de servicios administrados ofrecidos por algún CSP (*Cloud Service Provider*).

## Componentes analizados

La siguiente es los componentes analizados de la pila tecnológica definidas en la [Arquitectura de implementación](../../../paginas/Arquitectura-Plataforma-Agentica/Arquitectura-de-implementacion.md) :

<!-- [macro: tabla de contenido] -->

### Java

Hace parte de la [LBA - Línea Base de Arquitectura](https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/), a nivel de licenciamiento garantizar que se hace uso de la distribución JRE o JDK de Eclipse Temurin ([https://adoptium.net/temurin](https://adoptium.net/temurin)) tal como esta definido en [Gestión imágenes Docker](https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/) .

### Python

Hace parte de la [LBA - Línea Base de Arquitectura](https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/) . No se tienen comentarios adicionales siempre y cuando su use esté enmarcado en lo establecido en la LBA.

### LiteLLM

Este componente cuenta con diferentes criterios para el licenciamiento, tal como se declara en el archivo [https://github.com/BerriAI/litellm/blob/10f4033437df30b91b5dbf2b64711d0a8683fc52/LICENSE](https://github.com/BerriAI/litellm/blob/10f4033437df30b91b5dbf2b64711d0a8683fc52/LICENSE) .

- Las características propias de LiteLLM Enteprise, tienen la licencia [https://github.com/BerriAI/litellm/blob/10f4033437df30b91b5dbf2b64711d0a8683fc52/enterprise/LICENSE.md](https://github.com/BerriAI/litellm/blob/10f4033437df30b91b5dbf2b64711d0a8683fc52/enterprise/LICENSE.md), y por tanto a no ser que ya se cuente con una licencia comercial vigente para su uso, de ninguna manera se deben referenciar, incluir, y mucho menos usar características relacionadas.
- El resto del código está bajo la licencia MIT License, que es válido su uso tal como está definido en [Políticas sobre licencias para el uso de librerías externas y componentes](https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/).

### Langfuse

### ClickHouse

### LangGraph
