# Rutas de referencia resueltas (v2)

Las instrucciones de v1 se escribieron cuando los artefactos vivían en la raíz de
`estimacin mvp/`. Al versionarlos en `v1/`, tres rutas quedaron rotas. Este archivo las
resuelve sin tocar v1, que es de solo lectura por la regla de oro de `instrucciones.md`.

Raíz del frente (todas las rutas relativas de aquí abajo cuelgan de ella):

```
/Users/didierfranco/Documents/GitHub/techandsolve/propuestas/SURA/gestores-sura/estimacin mvp
```

## Lo que se rompió y dónde está ahora

| Ruta citada en v1 | Ubicación vigente |
| --- | --- |
| `arquitectura-tecnologia.drawio` | `v1/arquitectura-tecnologia.drawio` |
| `2 Gestores_Seguimiento_Requerimientos_2026.xlsx` | `v1/2 Gestores_Seguimiento_Requerimientos_2026.xlsx` |
| `instruccione-estimacion.md` | `v1/instruccione-estimacion.md` |

Las tres se citan en `v1/instrucciones.md` y `v1/instruccione-estimacion.md` como archivos
editables. En v2 son **solo lectura**: son la línea base de la que se parte.

## Lo que sigue resolviendo sin cambios

Insumo del cliente, no se modifica:

- `insumos/iafirst/` — lineamientos AI First de SURA
- `insumos/2 Gestores_Seguimiento_Requerimientos_2026 (2).xlsx` — hoja original del cliente
- `insumos/resumen-arquitectura-gestores.drawio` — acote de arquitectura acordado
- `insumos/resumen-arquitectura-gestores-Arquitectura MVP.drawio.svg` — alcance del MVP dibujado

Nuestras recomendaciones previas, los archivos «Tech and Solve» del insumo:

- `insumos/Tech and Solve - Torre de control.html`
- `insumos/Tech and Solve - Torre de control_estimacion.html`
- `insumos/Tech and Solve - Notas de arquitectura.html`

## Línea base de v1, para leer y no para editar

- `v1/arquitectura-tecnologia.drawio` — tres páginas: despliegue tecnológico, runtime del
  gestor, trazabilidad del stack
- `v1/2 Gestores_Seguimiento_Requerimientos_2026.xlsx` — hoja «Estimación por Requisitos»,
  183 requisitos, 76 del MVP tallados
- `v1/Tech and Solve - Gestores MVP_estimacion.html` — dimensionamiento, entregable al cliente
- `v1/Tech and Solve - Gestores MVP_equipo_tech.html` — perfiles, documento interno
- `v1/estados de row.md` y `v1/image.png` — convención de colores de fila (la referencia
  relativa a la imagen sigue funcionando porque ambos se movieron juntos)

## Destino de los artefactos de v2

Todo lo que se genere va en `v2/`, con el mismo nombre que en v1 para que el par sea
evidente. Nada se escribe en la raíz del frente ni en `v1/`.
