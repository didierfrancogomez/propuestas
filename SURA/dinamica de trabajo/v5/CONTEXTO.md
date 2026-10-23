# Contexto de la propuesta SURA · Planes por tallas

> Reglas vigentes en `REGLAS.md` (leerlo primero). Archivo vivo: se actualiza con cada cambio. Última actualización: 2026-10-23 (auditoría).

## 1. Qué es
- **Entregable:** `tech-and-solve-propuesta-paquetes-de-actividades.html` (11 láminas 16:9). El nombre del archivo viene de Viva y no se cambió para no romper referencias.
- **Origen:** copia de la propuesta de Viva Aerobus (v5), adaptada a SURA como modelo transversal, con tallas en vez de puntos y características en vez de actividades.
- **No hay PDF ni PPTX de SURA todavía.** Los de esta carpeta eran de Viva y se movieron a `_copia-viva/` (con `LEEME.md`), junto con los scripts `calculos/` de Viva.

## 2. Estructura (11 láminas)
**Para el cliente (1–8)**
1. Portada: «Propuesta de cambio de dinámica de trabajo: del modelo staff a llave en mano por características».
2. SURA deja de gestionar el equipo y solo pide características (tabla staff vs llave en mano).
3. Pago por características terminadas, no por FTE: entradilla «Ahora lo que se trabaja son características: es lo que Tech and Solve estima, desarrolla, prueba y entrega» y tres tarjetas (plan al mes, talla por característica XS–XL, pago de la característica finalizada). Sin los planes (pedido 5).
4. Cuántas características de cada talla soporta cada plan (máximos enteros) y el perfil real de septiembre (10 XL + 4 L + 1 M + 5 S + 4 XS) que llena el plan Inicial.
5. Mezclas posibles por plan (3 variantes, cada una llena el 100 % del plan y pide un esfuerzo parecido):
   | Mezcla | Inicial (117) | Profesional (156) | Alta velocidad (195) |
   |---|---|---|---|
   | Perfil de septiembre (escalado) | 10 XL + 4 L + 1 M + 5 S + 4 XS (24) | 13 XL + 6 L + 1 M + 7 S + 5 XS (32) | 16 XL + 7 L + 2 M + 9 S + 8 XS (42) |
   | Balanceada | 4 XL + 6 L + 10 M + 10 S + 5 XS (35) | 6 XL + 8 L + 12 M + 12 S + 8 XS (46) | 8 XL + 10 L + 15 M + 14 S + 8 XS (55) |
   | Muchas y pequeñas | 2 L + 15 M + 25 S + 12 XS (54) | 3 L + 20 M + 30 S + 21 XS (74) | 4 L + 25 M + 40 S + 20 XS (89) |
6. Modelo de trabajo (SURA entrega, prioriza y certifica; Tech and Solve valida, asigna la talla, implementa y ajusta).
7. Condiciones del servicio (tiempos de SURA en días hábiles, calidad, accesos, alcance; máximo talla XL).
8. Términos y condiciones (cambio de plan con 3 meses de aviso, facturación, escala de tallas, capacidad no usada, características en curso por definir).

**Internas (9–11), con «USO INTERNO» y el aviso de datos de referencia de Generic API de Viva**
9. Tallas de referencia: las 19 tareas de septiembre, con su talla y sus puntos (completa y del mes).
10. El plan Inicial es de 117 puntos: semanas, 153 → ≈ 115 → 117, y capacidad de cada plan (= 39 / 52 / 65 M exactos · ≈ 394 / 525 / 657 h de trabajo).
11. Cómo se reparte cada mezcla en el equipo: 39 puntos por persona, el reparto real de septiembre (46 · 44 · 27 en terminadas; 51 · 52 · 50 con todo el esfuerzo) y las horas típicas por persona (125–132 h al mes).

## 3. Modelo de cálculo (`modelo-tallas/`)
- **`modelo-calculo-tallas.xlsx`**: fórmulas vivas; hojas Parametros, Tareas, Septiembre, Planes, Mezclas, Equipo y Verificacion (todo OK). Insumo: informe de septiembre en `../resources/` (26 tareas; 564 h completas y 394 h del mes en las 19 terminadas + 130 h en 7 otras = 524 h).
- **Cadena:** horas reales + 30 % → talla → septiembre = 10 XL + 4 L + 1 M + 5 S + 4 XS = **117 pts** → / 3 personas = **39 pts por persona** → planes 117 / 156 / 195 → mezclas (suman exacto la capacidad) → reparto por persona (39 exactos; la suma del equipo = la mezcla).
- **Validación en horas (auditoría):** con el punto medio de cada talla, las 9 mezclas piden entre 1 % y 4 % menos horas que las equivalentes del plan (117 pts ≈ 394 h reales de septiembre) y cada persona queda entre 125 y 132 h al mes (unas 3 semanas de 42 h): las mezclas son equivalentes en esfuerzo y caben en el mes.
- **Scripts:** `generar_modelo.py` genera el Excel y `datos.json` y comprueba que el Excel evaluado (librería `formulas`) coincide con el modelo en Python; `actualizar_deck.py` reescribe las láminas 4, 5 y 11 y ajusta la 9 y la 10 (busca por título); `auditar_deck.py` comprueba cifras, orden y términos prohibidos ante el cliente. Correr: `venv/bin/python generar_modelo.py && python3 actualizar_deck.py && python3 auditar_deck.py` (el venv con xlsxwriter, formulas y openpyxl estaba en el scratchpad de la sesión; recrearlo si hace falta).

## 4. Decisiones confirmadas por Didier
- **Feedback de UAT: dentro de los 5 días hábiles desde que se abre el PR** (confirmado el 23 oct 2026; en Viva decía «5 días»).

## 5. Interpretaciones de Claude (por confirmar con Didier)
- Escala de **5 tallas (XS, S, M, L, XL)**, una por cada valor Fibonacci. Se puede reducir a S/M/L.
- Las descripciones de cada talla (lámina 4) y las mezclas «Balanceada» y «Muchas y pequeñas» son propuestas; la mezcla «Perfil de septiembre» sí sale de datos.
- Se quitó «Ready for prod» de lo que ve el cliente (es un estado del Jira de Viva); queda «certificada en UAT».
- Tiempos del cliente, Sonar, VPN y accesos se mantuvieron como en Viva; hay que validarlos con la realidad de SURA.

## 6. Riesgos y diferencias conocidas
- **153 pts × 3/4 = 114,75 vs 117** de base (2,25 pts, 1,9 %), heredado de Viva; está en la hoja Septiembre.
- **Caso extremo de horas:** si todas las características quedaran en el tope de su talla, la mezcla «Muchas y pequeñas» pediría 0,4–0,5 % más horas que las del mes (506 / 677 / 844 h frente a 504 / 672 / 840). No es un control (es el peor caso), pero muestra que las tallas pequeñas dan menos puntos por hora: el riesgo es de Tech and Solve.
- Los 39 pts por persona son un objetivo parejo; en septiembre el reparto real en tareas terminadas fue 46 / 44 / 27.

## 7. Historial de pedidos (23 oct 2026)
1. Tallas en vez de puntos; planes Inicial, Profesional y Alta velocidad; misma medición y capacidad de Viva; transversal.
2. Lámina de mezclas posibles por plan (mínimo 3 variantes).
3. Lámina de reparto por persona por mezcla y plan (interna).
4. «Verifica los cálculos; todos deben dar» → Excel con fórmulas y scripts; la mezcla 1 pasó a ser el perfil real de septiembre.
5. Quitar los paquetes de la lámina 3.
6. Láminas internas de septiembre: aviso de datos de referencia de Generic API de Viva (pueden variar en SURA).
7. Discurso comercial: se trabajan **características** (se estiman, desarrollan, prueban y entregan).
8. **Auditoría:**
   - el reparto por persona se movió al final, con las internas (antes estaba entre láminas del cliente);
   - se quitó el nombre del Excel de las láminas del cliente;
   - «5 días» pasó a «5 días hábiles desde que se abre el PR»;
   - «con su propia estimación» pasó a «con su propia talla»;
   - se corrigió «no se descuentan» a «no se descuenta» (la capacidad) y «1 pts» a «1 pt»;
   - se agregaron controles de horas al Excel (punto medio por talla) y la frase de horas por persona en la lámina 11;
   - se apartaron los archivos de Viva en `_copia-viva/`;
   - se agregó `auditar_deck.py`.
9. «Sí, deja "5 días hábiles desde que se abre el PR"» → confirmado (sección 4).
