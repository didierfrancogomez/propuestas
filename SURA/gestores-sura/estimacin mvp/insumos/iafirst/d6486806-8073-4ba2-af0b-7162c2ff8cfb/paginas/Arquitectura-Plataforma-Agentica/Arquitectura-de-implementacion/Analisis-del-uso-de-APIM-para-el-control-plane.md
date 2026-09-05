---
titulo: "Analisis del uso de APIM para el control plane"
id: 6244007968
espacio: AFGLYP
version: 2
actualizado: 2026-08-28T20:17:46.998Z
actualizado_por: "Diego Fernando Gomez Alvarez"
etiquetas: []
ruta: "AI First · Gobierno, Lineamientos y Prácticas > [ARQ] AI First: Arquitectura de referencia y lineamientos > Arquitectura Plataforma Agentica > Arquitectura de implementación"
origen: https://segurosti.atlassian.net/wiki/spaces/AFGLYP/pages/6244007968
---

# Analisis del uso de APIM para el control plane

Documento de posición técnica para sustentar el uso de **Azure API Management (APIM)** como capa de API / AI Gateway del **Control Plane** de la Plataforma Agéntica, en coexistencia con **Google Apigee** como estándar corporativo para la exposición de APIs de negocio.

> **[INFO]**
> **Conclusión recomendada.** Adoptar APIM como preferencia técnica para el Control Plane agéntico por su alineación con el runtime gobernado en Azure, su integración nativa con **Entra ID** y **Microsoft Sentinel**, y su mejor ajuste para capacidades como **A2A Gateway** y **MCP Gateway**. Esta decisión no reemplaza la estrategia corporativa de apificación basada en APIGEE.

Ir a: Resumen ejecutivo · Capacidades comparadas · Impacto en la arquitectura · ADR de la decisión · Próximos pasos

# Resumen ejecutivo

El análisis concluye que, desde el punto de vista estrictamente técnico, **APIM y APIGEE son alternativas viables** para cumplir el rol de gateway agéntico. La diferencia principal no está en la funcionalidad base de gestión de APIs, sino en la **integración con el ecosistema corporativo** y en la **alineación con la estrategia de IA**.

La preferencia técnica favorece a **APIM** para el Control Plane porque las cargas agénticas están gobernadas en Azure, lo que reduce fricción de integración, disminuye latencia y fortalece capacidades críticas de identidad, observabilidad y control centralizado. En paralelo, **APIGEE mantiene su rol** como capacidad corporativa para APIs de negocio, aliados y estrategia API-Led.

| Dimensión | APIM en Control Plane IA | APIGEE en APIs de negocio |
| --- | --- | --- |
| Rol principal | Capa de API / AI Gateway del ecosistema agéntico | Exposición y gobierno de APIs de negocio |
| Identidad | Integración nativa con Entra ID, service principals y managed identities | Integración posible, con mayor esfuerzo |
| SIEM | Conector nativo hacia Microsoft Sentinel | Requiere integración adicional desde GCP |
| Plano agéntico | Mejor alineación con A2A, MCP y runtime en Azure | Mayor fortaleza en exposición de negocio y aliados |
| Madurez operativa | Aceleradores IA por construir | Aceleradores APIOps ya maduros |

# Contexto y objetivo

La Plataforma Agéntica introduce un **Control Plane** como capa transversal de gobierno para agentes, modelos, herramientas, prompts, observabilidad, seguridad y FinOps. Dentro de esta capa, el gateway central controla el tráfico hacia modelos, tools, MCPs y otros agentes.

La pregunta de arquitectura es si este gateway debe implementarse sobre **APIGEE**, aprovechando los aceleradores corporativos existentes, o sobre **APIM**, priorizando la cercanía técnica con Azure, donde residen y se gobiernan las cargas agénticas.

Este análisis busca:

- Comparar APIM y APIGEE en capacidades funcionales y no funcionales para IA.
- Establecer el impacto de cada opción sobre la arquitectura del Control Plane.
- Identificar implicaciones de seguridad, operación, costos y gobierno.
- Registrar una posición técnica en formato ADR.

| En alcance | Fuera de alcance |
| --- | --- |
| Gateway del Control Plane agéntico: AI, A2A y MCP | Decisión final de adquisición y detalle económico de licenciamiento |
| Comparación APIM vs APIGEE para cargas de IA | Selección de una plataforma dedicada de AI Security |
| Implicaciones de gobierno, operación, seguridad y costos | Reemplazo de la estrategia corporativa API-Led |

# Capacidades comparadas

Ambas plataformas cubren correctamente las capacidades tradicionales de API Management. La comparación relevante se concentra en los requerimientos específicos del caso agéntico.

| Capacidad | APIM | APIGEE | Lectura arquitectónica |
| --- | --- | --- | --- |
| Exposición de APIs de negocio | Soportado | Fortaleza y estándar corporativo | APIGEE sigue siendo la referencia para negocio |
| A2A Gateway | Mejor integración en el plano Azure | Capacidad presente | Ventaja práctica para APIM |
| MCP Gateway | Control centralizado de acceso a tools y MCP | Capacidad presente | El Control Plane concentra el gobierno en APIM |
| Autenticación de agentes | Entra ID nativo | OAuth2, OIDC y JWT con mayor esfuerzo de integración | Ventaja clara para APIM |
| Control de consumo de modelos | Políticas nativas de cuota y límite de tokens | Soportado mediante políticas | Ambas viables, APIM más natural en Azure |
| Observabilidad / SIEM | Integración nativa con Sentinel | Integración indirecta vía conectores o desarrollo | APIM reduce complejidad operativa |
| Automatización operativa | Capacidades por madurar en el frente IA | Aceleradores maduros de APIOps | Ventaja actual para APIGEE |

note47866cd3cde9
**Lectura clave.** Para el frente de IA, APIM no gana porque APIGEE sea débil, sino porque se integra mejor con el plano donde viven las identidades, la observabilidad y el runtime agéntico.

**Lectura clave.** Para el frente de IA, APIM no gana porque APIGEE sea débil, sino porque se integra mejor con el plano donde viven las identidades, la observabilidad y el runtime agéntico.

# Capacidades no funcionales

| Atributo | APIM | APIGEE | Implicación |
| --- | --- | --- | --- |
| Integración de identidad | Nativa con Entra ID | Posible con mayor trabajo de integración | APIM simplifica gobierno de identidades no humanas |
| Latencia | Menor al estar en el mismo plano Azure | Puede añadir saltos hacia GCP | APIM favorece eficiencia transaccional |
| Resiliencia | Exige HA por ser punto central del Control Plane | Plataforma madura y ya operada | Ambas requieren diseño robusto |
| Escalabilidad | Adecuada, con diseño cuidadoso del punto único de exposición | Probada a escala para APIs | No es factor excluyente |
| Multicloud / híbrido | Azure + self-hosted gateway | Apigee X e Hybrid | APIGEE ofrece una postura fuerte en híbrido |
| Operación | Necesita construir aceleradores para IA | Ya cuenta con APIOps, portal y trazabilidad madura | APIGEE aventaja en madurez operativa actual |

# Impacto en la arquitectura

En el modelo objetivo, el gateway del Control Plane actúa como **puerta de entrada obligatoria** para el tráfico agéntico. Todo consumo de modelos, tools y comunicación entre agentes debe atravesarlo para asegurar trazabilidad, aplicación de políticas, control de acceso y observabilidad.

Esto implica un principio arquitectónico explícito: **no debe existir acceso directo entre componentes que evite el gateway**. Ese “contrabando” rompe la capacidad de gobierno centralizado y debilita la operación del ecosistema.

## MCP Gateway y ubicación de MCP servers

El análisis confirma que el **MCP Gateway es un componente permanente y necesario** del Control Plane. Su propósito no se limita a seguridad puntual; su valor principal es el **control centralizado de acceso** a múltiples MCP servers, incluyendo políticas por agente, cuotas, rate limiting y observabilidad unificada.

| Elemento | Ubicación y responsabilidad |
| --- | --- |
| MCP Gateway | Vive en APIM dentro del Control Plane y centraliza acceso, políticas, cuotas y trazabilidad sobre todos los MCP servers |
| MCP server de negocio | Se despliega por fuera del Control Plane, en el entorno del dominio de negocio que posee la capacidad |
| MCP server de tercero | Se conecta al ecosistema a través del MCP Gateway, que aporta gobierno y control que no existen sobre el tercero |
| Runtime agéntico | Permanece fuera del gateway, bajo gobierno de Azure |

> **[TIP]**
> **Resultado de diseño.** Este patrón evita solapamiento entre APIM y APIGEE: APIM gobierna el acceso agéntico centralizado en el Control Plane, mientras APIGEE mantiene el frente de exposición de negocio.

## Implicaciones técnicas directas

- El gateway se convierte en punto único de exposición y debe diseñarse con alta resiliencia.
- El onboarding de nuevos dominios requiere fuerte automatización de DNS, certificados, red y políticas.
- Cada dominio debe exponer sus rutas de forma controlada y registrarse en el gateway.
- La observabilidad debe cubrir tanto gateway como runtime agéntico para conservar trazabilidad end-to-end.

# Gobierno, seguridad y operación

## Gobierno

- **Separación de responsabilidades:** APIGEE sigue como estándar de negocio; APIM asume el frente IA.
- **Propiedad por dominio:** cada dominio dueño de una capacidad es responsable de su MCP server.
- **Gobierno de identidades no humanas:** Entra ID se consolida como base para agentes y service principals.
- **Gobierno del consumo:** todas las políticas de acceso, cuota y trazabilidad se concentran en el Control Plane.

## Seguridad

En seguridad base, ambas plataformas son suficientes. La ventaja de APIM se concentra en la integración nativa con identidad corporativa y monitoreo. Esta decisión cubre la **capa de gateway**, no reemplaza la necesidad futura de una **plataforma especializada de AI Security** para riesgos como prompt injection, jailbreak, envenenamiento de RAG o exfiltración.

| Aspecto | Lectura para APIM | Lectura para APIGEE |
| --- | --- | --- |
| AuthN / AuthZ | Muy bien alineado con Entra ID | Viable, pero menos nativo |
| Identidades no humanas | Mejor ajuste operativo | Mayor esfuerzo de integración |
| Integración SIEM | Directa con Sentinel | Requiere puente desde GCP |
| Control de acceso a MCP | Centralizado en el Control Plane | Depende del patrón de integración |

## Operación

- APIGEE aporta una base operativa madura, pero pensada para APIs de negocio.
- APIM para IA requiere construir aceleradores propios de onboarding, publicación y gobierno.
- La coexistencia de dos API Managers introduce complejidad operativa, asumida como deuda técnica gestionada.
- El modelo de operación del Control Plane sigue abierto y debe definirse con Plataforma Digital, Ciberseguridad y gobierno de IA.

# Costos y trade-offs

La evaluación de licenciamiento detallado está fuera del alcance del análisis, pero sí emergen implicaciones relevantes:

- **Costo de transacción y latencia:** enrutar tráfico agéntico fuera de Azure puede aumentar costo y complejidad.
- **Costo operativo:** coexistir con APIM y APIGEE exige más capacidades de administración.
- **Costo de construcción:** APIM necesita aceleradores e industrialización para el contexto IA.
- **Riesgo multicloud:** una futura expansión regional o hacia otras nubes puede tensionar la decisión.

> La decisión por APIM es técnicamente favorable hoy, pero no debe confundirse con una respuesta definitiva para todos los escenarios multicloud o de exposición futura a aliados.

# Ventajas, riesgos y dependencias

## Ventajas de APIM

- Coherencia con el gobierno de cargas agénticas en Azure
- Integración nativa con Entra ID y Sentinel
- Mejor ajuste para A2A y control centralizado de MCP
- Menor latencia al compartir plano con el runtime
- Capacidades nativas de control de consumo para LLM

## Riesgos y dependencias

- Punto único de falla del tráfico agéntico
- Necesidad de alta automatización de onboarding
- Modelo operativo aún no cerrado
- Dependencia de Entra ID, Sentinel y runtime en Azure
- Posible presión futura por escenarios multicloud o multi-región

# ADR de la decisión

| Campo | Contenido |
| --- | --- |
| Identificador | ADR-2026-001 |
| Estado | `[Propuesto]` Preferencia técnica por APIM, pendiente de ratificación estratégica |
| Fecha | 2026-08-19 |
| Decisión | Adoptar APIM como capa de API / AI Gateway del Control Plane agéntico y mantener APIGEE como estándar para APIs de negocio y exposición a aliados |
| Justificación principal | Las cargas agénticas residen en Azure; APIM se integra mejor con Entra ID, Sentinel, A2A y el gobierno centralizado de MCP |
| Consecuencias | Se administra un segundo API Manager, se exige alta resiliencia, automatización de onboarding y construcción de aceleradores operativos para IA |
| Decisiones abiertas | Ratificación estratégica, modelo operativo, postura multicloud, exposición a aliados y adopción de AI Security |

# Proximos pasos

- [ ] Escalar la decisión a un foro con mandato de estrategia de IA
- [ ] Ratificar la preferencia técnica mientras la implementación en IaC siga siendo reversible
- [ ] Definir el modelo de operación y sostenibilidad del Control Plane
- [ ] Automatizar onboarding de dominios: DNS, certificados, red y políticas
- [ ] Construir aceleradores operativos para publicación de agentes y registro de MCP
- [ ] Definir postura multi-nube y multi-región
- [ ] Planificar la evaluación de una capa especializada de AI Security
- [ ] Cerrar evaluación económica de licenciamiento

# Mensajes clave para comité

- **La decisión no es APIM versus APIGEE como reemplazo corporativo.** Es una decisión acotada al Control Plane de IA.
- **La coexistencia es el patrón recomendado.** APIM para gobierno agéntico; APIGEE para APIs de negocio.
- **El MCP Gateway debe permanecer en el Control Plane.** Su valor está en el gobierno centralizado del acceso, no solo en seguridad puntual.
- **La ratificación final debe ser estratégica.** Técnicamente APIM es preferible, pero la universalización de la decisión requiere visión multi-nube, regional y de exposición futura.

# Referencias

- [https://owasp.org/www-project-top-10-for-large-language-model-applications/](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [https://learn.microsoft.com/azure/api-management/api-management-policies](https://learn.microsoft.com/azure/api-management/api-management-policies)
