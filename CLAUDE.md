# Repositorio de propuestas de Tech and Solve

Propuestas de consultoría para clientes. Cada entregable es un HTML autocontenido, con
logos embebidos y sin dependencias externas más allá de Google Fonts, y su PDF exportado.

## Regla de oro: fuentes oficiales y versiones liberadas

Aplica a toda propuesta de este repositorio, sin excepción.

1. **Solo fuentes oficiales.** Toda afirmación que se sustente en un estándar, una norma o
   una regulación se cita desde el emisor: el organismo normativo, el diario oficial, el
   supervisor o el proyecto que publica la especificación. **Nunca desde un sitio de
   terceros**, por conveniente que sea de leer: agregadores, trackers, explicadores,
   resúmenes de consultoras o wikis no son fuente.
2. **Solo versiones liberadas.** Se cita lo publicado y vigente. **Nunca borradores**,
   preprints, versiones en desarrollo, consultas públicas abiertas ni páginas marcadas como
   experimentales o no mantenidas. Si un estándar aún no tiene versión liberada, se dice
   así en el documento y no se presenta como estándar.
3. **Verificar antes de citar.** Confirmar que la URL responde, que el contenido es el
   emisor y no un espejo, y que la versión está liberada. Si una página advierte que se
   movió o que no se mantiene, no se cita: se busca la ubicación canónica.
4. **La práctica de industria se etiqueta como tal.** La documentación de un fabricante
   (por ejemplo IBM) es fuente válida sobre su propia práctica, y se cita desde su sitio
   oficial, pero se presenta como práctica documentada y nunca como norma.
5. **Todo estándar tiene que ser enlazable.** Ninguna afirmación que invoque un estándar,
   una norma o una regulación entra al documento sin su enlace a la documentación oficial,
   en el mismo bloque donde se afirma y no solo en una lista de referencias al final. Si no
   existe un enlace oficial que la respalde, la afirmación se reformula como opinión propia
   o se elimina. La regla práctica: **si no se puede citar, no se afirma como estándar.**
6. **Sin plazos ajenos.** No estimamos ni citamos como propios los tiempos de trabajo de
   otros equipos. Se nombra la dependencia, y el plazo lo declara su dueño.

Ejemplos resueltos en este repositorio: el Reglamento europeo de IA se cita desde EUR-Lex,
no desde sitios de seguimiento cuyas traducciones son generadas por máquina; las
convenciones semánticas de OpenTelemetry se citan en su versión liberada, y las específicas
de IA generativa se declaran en desarrollo en lugar de presentarse como estándar.

## Regla de oro: el insumo del cliente no se modifica

Aplica a toda propuesta de este repositorio, sin excepción.

1. **Ningún insumo entregado por el cliente es modificable directamente.** Diagramas,
   hojas de cálculo, presentaciones, actas, documentos y capturas se tratan como evidencia
   de solo lectura. No se editan, ni siquiera para corregir un error evidente, un nombre
   mal escrito o un formato incómodo.
2. **Se versiona tal como llegó.** Se conserva el nombre original, incluidos los sufijos
   raros que traiga. Una versión nueva del mismo insumo se agrega al lado, no reemplaza a
   la anterior, para que el historial muestre qué recibimos y cuándo.
3. **Lo que haya que corregir o derivar vive en un artefacto propio.** Si un dato del
   insumo está mal, o hace falta transformarlo, el resultado va en nuestro documento o en
   el contexto interno, con la observación de dónde salió. El archivo del cliente queda
   intacto.
4. **Los scripts que lo leen, solo leen.** Nada de reescribir la hoja, normalizar columnas
   en el sitio ni guardar de vuelta. Si hace falta un extracto, se escribe en el
   scratchpad o en un archivo nuevo.
5. **La propuesta no se compara contra el insumo.** Se construye sobre el diseño del
   cliente y lo cita como base, pero no pone nuestras cifras al lado de las suyas ni
   señala inconsistencias de su planeación. Eso es conversación de sesión, no contenido
   del entregable.

Ejemplo resuelto en este repositorio: el insumo de SURA del 1 de septiembre se versionó
completo y sin tocar en `torre-de-control/v1/documentacion 1 septiembre/`, y todos los
ajustes que produjo quedaron en nuestros documentos.

## Antes de tocar la cuenta de SURA

El trabajo de SURA está repartido en dos carpetas, y cada una versiona por su cuenta:

- `torre-de-control/` — la torre de control, con la propuesta, el dimensionamiento y el
  documento interno de equipo. Cada versión es una subcarpeta, `v1`, `v2` y siguientes.
- `gestores-sura/` — las notas de arquitectura sobre la acertividad de los agentes, con el
  mismo esquema de subcarpetas por versión.

Leer primero el `context.md` de la versión vigente de `torre-de-control/`. Contiene el
enfoque acordado, los entregables vigentes, la terminología, las reglas de tono, las
fuentes del sustento y los cambios pendientes. Es documento interno: no se entrega al
cliente. El insumo que entrega el cliente vive junto a ese contexto y se rige por la regla
de oro de más arriba.

**El enfoque, en una frase**: indicar, según estándar, cómo tener una torre de control de
sistemas agénticos orientada a las necesidades del cliente, sin perder las buenas
prácticas. No es una especificación de monitoreo operativo: el cliente ya tiene su catálogo
de 9 ejes y más de 80 variables, y no se reemplaza.

## Terminología obligatoria

Usar el término correcto, aunque esté en inglés, y preferir la etiqueta que el cliente usa
en sus propios diagramas.

- **core** o **SuraHis**, nunca "núcleo de registro"
- **AI Control Plane**, **LLM Gateway**, **Prompt Management**, **runtime agéntico**
- **golden set**, nunca "conjunto de oro"
- **modo shadow** y **canary**, nunca "sombra" ni "canario"
- **LLM-as-a-judge**, nunca "modelo como juez"
- Se conservan por ser vocabulario del cliente o del negocio: acertividad, bandeja,
  preradicado, glosa, meta-estados, siniestro padre, ANS, tutela, integralidad, toque cero
- Sin anglicismos inventados y sin traducciones literales que obliguen a traducir de vuelta

## Tono

- Son sugerencias debatibles y descartables, construidas sobre el diseño del cliente.
- No usar vocabulario de auditoría en el cuerpo del documento.
- Nunca mencionar iteraciones internas ni versiones previas: para el cliente es una sola
  propuesta.
- Ninguna norma citada obliga al cliente: se presentan como referencia de mercado.

## Al editar un HTML de propuesta

- Reutilizar la hoja de estilos existente; los títulos nunca más pequeños que el párrafo
  que titulan, y los tamaños de impresión van fijos en `@media print`.
- Verificar antes de entregar: anclas del índice, balance de etiquetas, ids únicos, y que
  ningún texto de las figuras se desborde de su lienzo ni de su caja.
- Las figuras hacen trabajo, no decoran. El marco conceptual va en anexos, no en el cuerpo.

## Git

- Remoto `didierfrancogomez/propuestas`, rama `main`, commits directos.
- El perfil de gh debe ser **didierfrancogomez**; con `franco52428` el push falla con 403.
- Mensajes de commit en español y en minúscula.
- Los `.DS_Store` están en `.gitignore` y no se versionan.
