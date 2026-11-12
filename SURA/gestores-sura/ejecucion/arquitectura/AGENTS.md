# AGENTS.md — cómo iterar sobre la arquitectura de Gestores SURA

Instrucciones para cualquier agente (Claude Code u otro) que trabaje en esta carpeta.
Objetivo: **no perder el contexto** entre iteraciones. Cada cambio al diagrama se refleja
primero como regla de negocio en `context.md` y luego en el dibujo.

## ⭐ Regla de oro: un cambio, todas las pestañas

Todo cambio se aplica en **todas las pestañas del `.drawio`** donde aparece lo que cambió: el
elemento, el flujo, el texto, el contrato o el nombre. El diagrama completo debe contar la misma
historia. Un cambio **no está terminado** mientras alguna pestaña diga otra cosa. Si una
pestaña no se puede alinear ahora, se deja como pendiente en `context.md` (§7 y bitácora),
nunca en silencio. Está en los lineamientos de diseño, `context.md` §9.

Pestañas que hoy repiten el Gestor Solicitud: *Detalle: Gestor Solicitud* (`d1`) y *canales con
core* (`vkSiqqhCaptGzxPIeG1_`). Pestañas que repiten el Gestor Evaluación: *Detalle: Gestor
Evaluación (Release 1)* (`d2`) y *Gestor Evaluación Release final* (`p70LqHCaPi_F7LSYZtux`).
Revisar también *Vista general*, *Juez*, *Dónde vive la IA*, *Duplicados* y *Glosario*.

*canales con core* es hoy una **copia exacta** de *Detalle: Gestor Solicitud* más dos notas propias
en el margen izquierdo (`lCf-iueePdCvOuLlOe5z-5` e `lCf-iueePdCvOuLlOe5z-2`). La forma más segura de
sincronizarla es editar el detalle y copiar su `<root>` completo a *canales con core*, y luego volver
a agregar esas dos notas.

Para encontrar todas las apariciones antes y después del cambio:

```bash
python3 -I - <<'PY'
import xml.etree.ElementTree as ET, re, html
PAT = re.compile(r'TEXTO_A_BUSCAR', re.I)   # p. ej. r'blob|no procesable'
t = ET.parse('Arquitectura_Gestores_SURA_v6_4.drawio').getroot()
for d in t.iter('diagram'):
    for c in d.iter('mxCell'):
        v = html.unescape(re.sub('<[^>]+>', ' ', c.get('value') or ''))
        if PAT.search(v): print(f"[{d.get('name')}] {c.get('id')}: {' '.join(v.split())[:120]}")
PY
```

## Archivos

| Archivo | Rol | ¿Se edita? |
|---|---|---|
| `context.md` | Fuente de verdad: reglas de negocio, contratos, decisiones, preguntas abiertas, inconsistencias, guía de estilo y bitácora | Sí, en **cada** cambio |
| `Arquitectura_Gestores_SURA_v6_4.drawio` | Diagrama vigente | Sí |
| `Arquitectura_Gestores_SURA_v6_3.drawio` | Versión anterior (subida a `main` en `dc117f0`) | **No** (histórico) |
| `Arquitectura_Gestores_SURA_v6_2.drawio` | Versión anterior | **No** (histórico) |
| `resources/Arquitectura-Gestores consolidado.drawio` | Insumo de referencia | **No** (solo lectura, regla de oro de `propuestas/CLAUDE.md`) |
| `resources/Cronograma implementación.xlsx` | Insumo de planeación: backlog de HU por épica (pestañas *Backlog General*, *HUs propuestas*, *Sprint 3Q4*). Resumen del Gestor Solicitud en `context.md` §3.3b | **No** (solo lectura; leer con un script en el scratchpad, sin guardar de vuelta) |

## Antes de cualquier cambio

1. Leer `context.md` completo, en especial §3–§7 (reglas, preguntas abiertas e inconsistencias) y §9 (estilo).
2. Respetar la **precedencia**: por ahora mandan las reglas de *Detalle: Gestor Solicitud* y *Detalle: Gestor Evaluación (Release 1)*. El diagrama es la **arquitectura completa**: el cronograma ordena la implementación, pero no recorta componentes.
3. Revisar los lineamientos aplicables en `SURA/lineamientos-sura/` (ver §8 de `context.md`). Si el cambio se aparta de uno, decirlo y anotar el motivo.
4. Usar la terminología de `propuestas/CLAUDE.md` (core, LLM Gateway, runtime agéntico, LLM-as-a-judge, HITL, siniestro padre, bandeja…).

## Ciclo por cada cambio que pida el usuario

1. **Traducir el pedido a regla de negocio.** Identificar qué regla nueva, modificada o eliminada implica (IDs `RN-SOL-xx`, `RN-EVA-xx`, `RN-TRV-xx`; nuevos gestores usan su propio prefijo).
2. **Actualizar `context.md` en todas las partes afectadas**, no solo en la tabla de reglas:
   - flujo de punta a punta (§3.1 / §4.1),
   - tabla de reglas,
   - contrato de entrada/salida y respuesta,
   - decisiones de diseño,
   - preguntas abiertas (cerrar las que se resuelvan, con la respuesta),
   - inconsistencias (cerrar las que se corrijan),
   - lineamientos aplicados (si cambia la alineación),
   - **bitácora** (§10): fecha, cambio, reglas afectadas, páginas tocadas.
3. **Propagar al diagrama en todas las pestañas (regla de oro):** flujo, títulos y subtítulos, tabla de entrada/salida, notas de diseño, banda de eventos Kafka, auditoría y píldoras. Correr la búsqueda de arriba antes y después del cambio, y renderizar **cada** pestaña tocada.
4. **Mantener el estilo** de §9 de `context.md`: copiar el `style` de un elemento existente del mismo tipo; nunca inventar colores, fuentes ni formas.
5. **Verificar** (ver abajo) y reportar qué reglas y qué páginas cambiaron.

Si el pedido es ambiguo o contradice una regla vigente, preguntar antes de dibujar. Si es una duda de negocio sin respuesta, dibujarla como actividad punteada + *callout* y registrarla en "Preguntas abiertas".

## Cómo editar el `.drawio`

- Es XML sin comprimir (`<mxfile>` → `<diagram id=… name=…>` → `<mxGraphModel>` → `<mxCell>`). Editarlo con un script de Python que lea, modifique y escriba, o con reemplazos exactos; nunca reformatear el archivo entero.
- Páginas por id: `d0` Vista general · `d1` Detalle: Gestor Solicitud · `d2` Detalle: Gestor Evaluación (Release 1) · `p70LqHCaPi_F7LSYZtux` Gestor Evaluación Release final · `d3` Juez · `d4` Dónde vive la IA · `d5` Duplicados por servicio · `p6` Glosario.
- Ids nuevos únicos dentro de la página (por ejemplo `ctx-<tema>-<n>`); `parent` = id del contenedor en el que vive el elemento (las coordenadas son relativas a ese contenedor).
- Conectores con `source` y `target` reales, no flechas sueltas.
- **Los puntos de quiebre (`mxPoint`) de un conector están en las coordenadas de su `parent`.** Si el conector vive dentro de un contenedor, los puntos se dan relativos a ese contenedor, no a la página.
- Para que un conector no dé vueltas, fijar sus puertos (`exitX/exitY`, `entryX/entryY`) y llevarlo por los **pasillos entre franjas**. Al mover cajas, quitar los puertos y puntos viejos que ya no apliquen.
- **Ojo con las comillas del atributo `value`:** al reescribir un valor que contiene `"`, `xml.sax.saxutils.quoteattr` lo deja entre comillas simples (`value='…'`). Una regex `value="[^"]*"` no lo encuentra y **falla en silencio**. Usar `value=("[^"]*"|'[^']*')` y verificar siempre que el texto nuevo quedó escrito: comparar antes y después, o buscar el texto después de guardar.
- Antes de editar, renderizar la página para ubicar el espacio libre:
  ```bash
  /Applications/draw.io.app/Contents/MacOS/draw.io -x -f png -p <n_pagina_1_based> -s 0.5 -o <scratchpad>/pagina.png Arquitectura_Gestores_SURA_v6_4.drawio
  ```

## Verificación antes de entregar

1. El XML parsea (`python3 -c "import xml.etree.ElementTree as ET; ET.parse('Arquitectura_Gestores_SURA_v6_4.drawio')"`).
2. No hay ids duplicados en la página y todo conector tiene `source`/`target` existentes.
3. Se renderizó la página tocada con el comando de arriba y se revisó la imagen: sin textos desbordados, sin solapes, sin conectores cruzando cajas.
4. `context.md` y **todas** las pestañas dicen lo mismo (flujo, contratos, números ①②③, nombres); la búsqueda entre pestañas no devuelve textos viejos.
5. La bitácora tiene la entrada del cambio.

## Si el usuario abre una versión nueva

Cuando se cree `v6_5` (u otra), copiar la vigente, actualizar en este archivo y en `context.md` cuál es el diagrama vigente, y dejar la anterior como histórico. Las reglas no se reinician: se arrastran en `context.md`.

## Git

Commits directos a `main` en `didierfrancogomez/propuestas`, mensajes en español y en minúscula, perfil de gh **didierfrancogomez**. Solo hacer commit o push cuando el usuario lo pida.
