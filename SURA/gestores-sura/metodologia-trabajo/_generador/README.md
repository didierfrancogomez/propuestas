# Generador del .pptx

Genera `../Tech and Solve - Dinámica de trabajo del equipo.pptx` con las mismas láminas,
textos y notas del HTML de la carpeta de arriba.

**El HTML es la fuente de verdad.** Todo cambio se hace primero en el HTML y después se lleva
a `generar.js`. Los dos deben decir lo mismo.

## Regenerar el .pptx

Requiere Node.js 18 o superior.

```bash
cd "SURA/gestores-sura/metodologia-trabajo/_generador"
```

```bash
npm install
```

```bash
npm run generar
```

El archivo se escribe junto al HTML y reemplaza al anterior.

## Revisar desbordes

`revisar_desbordes.py` dibuja cada lámina de forma aproximada y avisa si un texto se sale de
su caja. Mide con Arial, más ancha que Calibri, así que la revisión es conservadora. No aplica
transparencias ni el recorte circular de las fotos: las fotos se ven cuadradas aunque en
PowerPoint salen circulares.

```bash
python3 -m pip install lxml pillow
```

```bash
python3 revisar_desbordes.py "../Tech and Solve - Dinámica de trabajo del equipo.pptx" /tmp/revision
```

Si no imprime ninguna línea `WARN`, no hay desbordes. Las imágenes quedan en la carpeta de
salida, una por lámina. Usa las fuentes de macOS.

Aun así, abre el `.pptx` en PowerPoint antes de entregar.

## Contenido

| Archivo | Qué es |
|---|---|
| `generar.js` | El generador: tema de marca, plantillas, helpers y una sección por lámina |
| `assets/logo.jpeg` | Logo de Tech and Solve |
| `assets/p_*.jpg` | Fotos del equipo, recortadas a 400 × 400 px y centradas en la cara |
| `revisar_desbordes.py` | Revisión aproximada de desbordes |
| `package.json` | Dependencia fija: `pptxgenjs` 4.0.1 |

`node_modules/` y `package-lock.json` no se versionan.

## Cómo está organizado `generar.js`

- **Tema**: Poppins para títulos, Calibri para el cuerpo y la paleta de la marca. Al final,
  `aplicarTema` escribe los colores en el tema del `.pptx`, porque pptxgenjs deja la paleta de
  Office.
- **Plantillas**: `TITULO`, sin pie, para portadas y aperturas de sección. `CONTENIDO`, con
  título, logo, pie de página y número de lámina.
- **Helpers**: `T` para texto, `card`, `dot`, `source` y `link` para citas con enlace,
  `newSlide` y `personCard` para la tarjeta de persona estándar.
- **Láminas**: un bloque por lámina, marcado con `// ================= N · nombre`, en el
  orden en que aparecen. Las notas del presentador van en `newSlide(..., notas)`.

## Fotos nuevas

1. Guarda el original en `~/Documents/GitHub/techandsolve/personas/<persona>/`, en JPG o PNG
   de al menos 800 × 800 px.
2. Recórtalo cuadrado, centrado en la cara y con aire sobre la cabeza.
3. Guárdalo en `assets/p_<nombre>.jpg` a 400 × 400 px y úsalo con `IMG("<nombre>")`.
4. En el HTML, súmalo como variable CSS en `:root` (`--p-<nombre>`), en base64.
