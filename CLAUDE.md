# Repositorio de propuestas de Tech and Solve

Propuestas de consultoría para clientes. Cada entregable es un HTML autocontenido, con
logos embebidos y sin dependencias externas más allá de Google Fonts, y su PDF exportado.

## Antes de tocar `gestores-sura/`

Leer primero `gestores-sura/v4/context.md`. Contiene el enfoque acordado, los entregables
vigentes, la terminología, las reglas de tono, las fuentes del sustento y los cambios
pendientes. Es documento interno: no se entrega al cliente.

**El enfoque, en una frase**: indicar, según estándar, cómo tener una torre de control de
sistemas agénticos orientada a las necesidades del cliente, sin perder las buenas
prácticas. No es una especificación de monitoreo operativo: el cliente ya tiene su catálogo
de 9 ejes y 88 variables, y no se reemplaza.

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
