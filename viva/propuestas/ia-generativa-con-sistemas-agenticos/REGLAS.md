# Reglas de la propuesta · IA generativa con sistemas agénticos (Viva Aerobus · Generic API)

> Reglas dictadas por Didier y heredadas de los documentos que él indicó. Se cumplen siempre.
> **Se actualiza en la misma respuesta cada vez que Didier da una regla nueva o cambia una.**
> El detalle de cada pedido, las decisiones y los pendientes están en `CONTEXTO.md`.
> Última actualización: 2026-10-19 (seis agentes).

## 1. Forma de trabajo

1. **Carpeta de trabajo: esta misma** (`viva/propuestas/ia-generativa-con-sistemas-agenticos/`). No se crea `v1/` ni se toca ninguna otra carpeta, en especial `nuevo-modelo-de-trabajo/` (Didier, 19 oct 2026; deja sin efecto la ruta `ia-aplicada-desarrollo/v1/` de `instrucciones.md`).
2. **Se trabaja solo el HTML.** El PDF y la PPT se generan cuando Didier lo confirme.
3. **El HTML lo genera un script** en `calculos/`. `CONTEXTO.md` y este archivo se actualizan en cada cambio, sin que haya que pedirlo.
4. **Interpretar, no copiar.** Didier da el enfoque; la redacción es nuestra, en tono comercial.
5. **Ante una instrucción ambigua**, decir qué se entendió o preguntar. No reemplazar una lámina sin avisar.
6. **Nunca hacer supuestos.** Toda cifra o afirmación lleva evidencia trazable: ticket de Jira, PR, fila del informe de seguimiento, documento, o enlace oficial de Anthropic. Lo que no se puede verificar se dice («no consta»).
7. **Recursos en solo lectura:** Jira, GitHub, repos de `GitHubViva/` (incluido `VivaAerobus.Generic.ApiLLMCoder`), informes xlsx y propuestas previas. Nada se publica en servicios externos. El insumo del cliente no se modifica.
8. **Revisar cada lámina con capturas** antes de entregarla: ningún texto se desborda de su caja ni de la lámina.

## 2. Lo que ve el cliente

1. **Se puede hablar de IA y de sistemas agénticos** (Didier, 19 oct 2026): la propuesta consiste en qué agentes se ofrecen en cada fase del ciclo de desarrollo. La regla de Generic API de no mencionar la IA se acota a esta propuesta.
2. **Al cliente no se le habla del repo LLMCoder, pero sí de una propuesta de agentes y del beneficio de tenerlos implementados** (Didier, 19 oct 2026). **Audiencia: líderes de tecnología de Viva Aerobus. Sin límite de láminas.** **Sigue siendo interno** (el resto, por confirmar con Didier, ver `CONTEXTO.md` §4): el repositorio LLMCoder y su nombre, sus reglas y fases numeradas, cuántos agentes o reglas hay, y cualquier cifra interna de nuestra IA. No se dice «derechos de autor»: se dice «propia» y «exclusiva».
3. **Se nombra «Claude» y «Anthropic», sin versiones ni modelos concretos** (Didier, 19 oct 2026).
4. **Sin nombres de personas** del equipo ni cuántas personas trabajan internamente.
5. **Separar lo que ya opera de lo que se propone.** Lo que ya opera se respalda con LLMCoder (evidencia interna, no se cita ante el cliente); lo demás se dice como propuesta.
6. **Las láminas internas** (evidencia, trazabilidad) llevan la franja ámbar «USO INTERNO · Esta lámina no se debe mostrar al cliente».
7. **Esta propuesta no tiene relación con la de paquetes de puntos** (Didier, 19 oct 2026): es independiente. No se citan sus cifras, paquetes ni condiciones.

## 3. Problemas que ataca (Didier, 19 oct 2026)

1. Devoluciones en la revisión de PR.
2. Pruebas y evidencias.
3. Calidad y trazabilidad.

Tiempos desviados **no** se eligió como problema central; no se promete reducirlos.

## 4. Fuentes oficiales (regla de oro del `CLAUDE.md` del repositorio)

1. Toda afirmación sobre Claude o sobre agentes se cita desde el emisor (anthropic.com, docs.anthropic.com y sus ubicaciones canónicas vigentes, `code.claude.com`, `platform.claude.com`), **en la misma lámina donde se usa**, no solo al final.
2. **Solo versiones liberadas.** No se cita lo marcado beta, experimental, en desarrollo ni lo que una nota declare desactualizado. Managed Agents está en beta: no se presenta como estándar ni como algo que usamos.
3. Verificar antes de citar: que la URL responde y que el contenido es del emisor. Las URL de `docs.claude.com` redirigen (301) a `code.claude.com`; se cita la ubicación canónica.
4. «Building Effective AI Agents» (anthropic.com, dic. 2024) trae una nota de que el panorama cambió: **no se cita sin visto bueno de Didier.**
5. Lo que describimos de nuestro proceso es **práctica documentada de Tech and Solve**, nunca norma ni estándar.
6. **Sin plazos ajenos.** No se estiman tiempos de otros equipos.
7. Ninguna afirmación de efecto («reduce devoluciones», «ahorra horas») sin medición propia citada. Hoy no consta ninguna medición del efecto del pipeline en las devoluciones.

## 5. Diseño de la presentación

1. **Línea gráfica de `SURA/gestores-sura/metodologia-trabajo/Tech and Solve - Dinámica de trabajo del equipo.html`:** láminas 16:9 apiladas, medidas en `cqw`, fondo blanco, títulos violeta, tarjetas violeta claro, pie con logo y número, portada violeta con el logo en caja blanca.
2. Reutilizar la hoja de estilos; los títulos nunca más pequeños que el párrafo que titulan; tamaños de impresión fijos en `@media print`.
3. Las figuras hacen trabajo, no decoran. Verificar anclas, balance de etiquetas, ids únicos y que ningún texto se desborde.

## 6. Terminología y tono

1. La del `CLAUDE.md` del repositorio: **golden set**, **LLM-as-a-judge**, **modo shadow**, **canary**, **runtime agéntico**; sin anglicismos inventados.
2. Son sugerencias debatibles y construidas sobre el modelo de trabajo del cliente (Jira, PR en GitHub, revisión del equipo Ezy). Sin vocabulario de auditoría; nunca se menciona nada interno de iteraciones.
3. El cliente es protagonista: se describe por lo que aporta, con verbo. No «otros equipos».

## 7. Redacción de agentes y beneficios (criterio aplicado en el primer HTML)

1. **Cada agente se describe con el mismo molde:** qué hace, qué recibe Viva Aerobus, quién decide. Todo se presenta como propuesta; el estado real (opera, parcial, propuesta) va solo en la lámina interna.
2. **Beneficios como propiedades del proceso** («llega con evidencia por cada caso», «cada cambio es trazable»), nunca como cifras ni como reducción («menos devoluciones», «más rápido») sin medición propia citada. La medición se propone (lámina 12), no se da por hecha.
3. **Siempre decide el desarrollador:** ningún agente publica un PR ni mueve un ticket sin su aprobación. Solo se dice lo que la evidencia interna respalda.
4. **Las fases se nombran con los estados de Jira de Viva** (To Do análisis, To Do, In Progress, In review, UAT, Ready for prod, Done).
5. **Sin «auditor», «dossier de defensa» ni anglicismos inventados** (los nombres Publicador y Orquestador los dictó Didier y se conservan). Sin plazos: el orden de activación es una sugerencia, no un calendario.
6. **Hay seis agentes:** Orquestador (orquesta todo el flujo; definición nuestra por confirmar), Analista (antes «Análisis»), Implementador de código (con las pruebas **unitarias** automatizadas embebidas), Pruebas funcionales (evidencia manual de consumo de servicios reales en Jira; pedido por Didier el 19 oct 2026), Validador de calidad (cobertura, Sonar, estilos y convenciones; nombre nuestro) y Publicador (antes «PR Creator»). Didier retiró el Check de puesta a punto y el Unit Tester como agentes aparte; no vuelven sin que él lo pida. Reemplazan a los 12 agentes anteriores (respaldo en `calculos/respaldo/`). No son nombres de personas.
7. **El diagrama de flujo muestra los seis agentes, las compuertas donde decide el desarrollador (pastillas ámbar) y lo que hace Viva Aerobus (verde).** Cada lámina de agente repite el mismo molde: qué hace, qué recibe Viva Aerobus, quién decide y lo que gana.
8. **El agente trabaja a petición del desarrollador, y es el desarrollador quien certifica que lo hecho es lo que espera recibir** (Didier, 19 oct 2026). En todo el documento quien valida, aprueba o decide sobre lo que entrega un agente es **«el desarrollador»**, no «una persona» ni «el equipo». El agente no certifica su propio trabajo y la responsabilidad por el cambio, ante el equipo de revisión y ante Viva Aerobus, sigue siendo del desarrollador. Lo que decide Viva Aerobus (revisión del PR, UAT) no cambia.
9. **El Orquestador también es un agente** (Didier, 19 oct 2026): se dibuja con el color de los agentes y se cuenta entre ellos. En el diagrama es una barra bajo los agentes porque los coordina; el retorno de hallazgos entre agentes lo hace él, no una flecha directa entre agentes.
10. **Qué cubre cada agente se dice con precisión** (Didier, 19 oct 2026): el Implementador automatiza solo pruebas unitarias; la evidencia manual de consumo de servicios reales en Jira es del agente de Pruebas funcionales, y el error funcional lo atacan juntos Analista, Implementador y Validador (el analista sabe lo que la task pide, el implementador la implementa y el validador garantiza que todo se cubre).
11. **La lámina de motivos de devolución** es la tabla consolidada de los 9 motivos del análisis de septiembre, con el motivo en texto normal y solo los agentes como chips; sin cifras (van en la lámina de cada agente).
12. **Sin láminas internas ni de medición (Didier, 19 oct 2026):** la presentación son 10 láminas para el cliente. Lo interno (evidencia en LLMCoder, límites de lo que se dice, estado de cada agente) vive solo en `CONTEXTO.md`; si se vuelve a agregar alguna lámina interna, lleva la franja «USO INTERNO». Se mantiene que no se promete cifra de mejora.
