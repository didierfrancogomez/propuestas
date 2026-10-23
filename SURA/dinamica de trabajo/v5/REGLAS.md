# Reglas de la propuesta · Planes por tallas (SURA, modelo transversal)

> Reglas dictadas por Didier. Se cumplen siempre y se actualizan en la misma respuesta cada vez que cambian.
> Base copiada de la propuesta de Viva Aerobus (`propuestas/viva/propuestas/nuevo-modelo-de-trabajo/v5/REGLAS.md`).
> El detalle de cada pedido y las cifras vigentes están en `CONTEXTO.md`.
> Última actualización: 2026-10-23 (auditoría).

## 0. Forma de trabajo
1. **No se modifica nada de Viva.** La carpeta `propuestas/viva/...` es solo lectura: sirve de referencia para la escala, la medición y la capacidad. Lo que se copió de allí está en `_copia-viva/` (no es de SURA, no se envía) o en `../resources/` (insumo).
2. **Se trabaja solo el HTML** `tech-and-solve-propuesta-paquetes-de-actividades.html`. El PDF se regenera solo cuando Didier lo confirme (hoy no hay PDF de SURA).
3. **`CONTEXTO.md` y este archivo se actualizan en cada cambio**, sin que haya que pedirlo.
4. **Todo número sale de `modelo-tallas/modelo-calculo-tallas.xlsx`** y la hoja Verificacion debe dar OK. Las láminas de capacidad por talla, mezclas y reparto por persona se regeneran con `actualizar_deck.py`, no a mano; `auditar_deck.py` debe pasar después de cualquier cambio.

## 1. El modelo
1. **Tallas en vez de puntos ante el cliente.** Misma medición que en Viva (tiempo real invertido + 30 %, escala Fibonacci):
   | Talla | Puntos internos | Tope (h con el 30 %) | Horas de trabajo |
   |---|---|---|---|
   | XS | 1 | 6 h | hasta 4,6 h |
   | S  | 2 | 11 h | 4,6–8,5 h |
   | M  | 3 | 17 h | 8,5–13,1 h |
   | L  | 5 | 28 h | 13,1–21,5 h |
   | XL | 8 | 39 h | 21,5–30 h |
   Lo que pasa de XL se divide: bloques XL de 39 h más el resto con su talla.
2. **Planes: Inicial, Profesional y Alta velocidad** = personas × 39 puntos: 117 / 156 / 195 (3 / 4 / 5 personas). 39 = 117 puntos de septiembre (equipo de referencia) / 3 personas. Subir o bajar de plan es sumar o quitar una persona.
3. **Cada plan dice cuántas características de cada talla soporta** (máximo entero si todo el mes fuera de una sola talla; las tallas se combinan). M divide exacto en los tres planes (39 / 52 / 65).
4. **Mezclas:** cada una llena exactamente la capacidad de su plan y debe pedir un esfuerzo parecido al del plan (punto medio de cada talla, ±5 %) y caber en el mes.
5. **Reparto por persona:** cada persona toma exactamente 39 puntos y la suma del equipo es la mezcla.
6. **Vocabulario comercial:** lo que se estima, se desarrolla, se prueba y se entrega son **características** (no «actividades»). «Tarea» solo se usa para los tickets del informe de Viva en las láminas internas y en el Excel.
7. **Propuesta transversal:** no va atada a un proyecto de SURA.

## 2. Lo que ve el cliente
1. Sin nombres de personas, sin IA, sin Viva, sin número de personas, sin horas ni puntos por plan, sin archivos internos.
2. **Las láminas internas van al final** (hoy 9, 10 y 11) y llevan la alerta «USO INTERNO · Esta lámina no se debe mostrar al cliente».
3. Las internas con datos de Viva dicen además: «Datos de referencia del equipo de Generic API de Viva Aerobus. En SURA pueden variar según el tipo de proyecto.»
4. Toda cifra mostrada como dato previo es citable (F1: informe de septiembre de 2026 del proyecto de referencia, copiado en `../resources/`).

## 3. Se mantienen de Viva
- Modelo de trabajo (SURA entrega, prioriza y certifica; Tech and Solve valida, asigna la talla, implementa, entrega en UAT y ajusta), cobro de la característica certificada en UAT.
- Condiciones del servicio (tiempos de SURA en días hábiles: revisión del PR y paso a UAT en máximo 3 días hábiles y **feedback de UAT dentro de los 5 días hábiles desde que se abre el PR**, confirmado; pruebas, Sonar, accesos, alcance) y términos (3 meses de aviso para cambiar de plan, facturación del 100 % del plan, la capacidad no usada no se descuenta).
- Línea gráfica de la presentación de referencia; ningún texto se desborda.
