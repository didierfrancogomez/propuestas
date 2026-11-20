# Genera la propuesta de pago programado de la TUA (deck 16:9, mismo sistema visual que la propuesta PUI v5).
# Plan de 5 semanas de implementación, con un líder técnico al 100 % y un tester al 50 %.
# Uso: python3 -I generador/sp_gen.py <html_pui_v5> <carpeta_salida>
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sp_figs import svg2, legend2, arch, dash, NUM

src, outdir = sys.argv[1], sys.argv[2]
ref = open(src, encoding="utf-8").read()
STYLE = re.search(r"<style>(.*?)</style>", ref, re.S).group(1)
COVER = re.search(r'<img src="([^"]+)" alt="Tech and Solve" class="cover-logo">', ref).group(1)
BRAND = re.search(r'<img src="([^"]+)" alt="Tech and Solve" class="brand">', ref).group(1)
STYLE += """
/* pago programado */
.fcols { display: grid; grid-template-columns: 1fr 1fr; gap: 1.4cqw; flex: 1; min-height: 0; }
.fcols .card { padding: 1.1cqw 1.4cqw; }
.fcols .card h3 { font-size: 1.3cqw; margin: 0 0 .5cqw; }
.fcols .fsteps li { font-size: 1.06cqw; line-height: 1.34; margin-bottom: .5cqw; }
.fcols .fsteps .n { width: 1.8cqw; height: 1.8cqw; font-size: .9cqw; }
.fcols + .note { margin-top: 1cqw; }
.row4 + .note { margin-top: 1.2cqw; }
.risk td:first-child { width: 6%; }
.risk td:nth-child(2) { width: 30%; }
.content.big ul { font-size: 1.25cqw; line-height: 1.48; }
.content.big li { margin-bottom: .7cqw; }
.content.big .fsteps li { font-size: 1.22cqw; line-height: 1.4; margin-bottom: .75cqw; }
.content.big .card h3 { font-size: 1.45cqw; }
.pre.risk { font-size: 1.08cqw; line-height: 1.35; }
.pre.risk td { padding: .55cqw .6cqw; }
.wk .card { display: flex; flex-direction: column; }
.wk .role { font-size: 1.05cqw; }
.wk .dates { font-size: 1cqw; margin: -.2cqw 0 .5cqw; }
.content.big .kvl { font-size: 1.25cqw; line-height: 1.45; gap: 1cqw 1.2cqw; }
.content.big .val { font-size: 1.25cqw; }
.content.big .opts ul { font-size: 1.3cqw; line-height: 1.5; padding-left: 1.3cqw; margin: 0; }
.content.big .opts li { margin-bottom: .7cqw; }
.content.big .opts + .note { font-size: 1.12cqw; line-height: 1.4; }
.opt .role { font-size: 1.05cqw; margin-bottom: -.6cqw; }
.row5 { display: grid; grid-template-columns: repeat(5, 1fr); gap: .9cqw; }
.row5 .card { padding: 1cqw 1.1cqw; }
.row5 .card h3 { font-size: 1.2cqw; margin: .2cqw 0 .5cqw; }
.content.big .row5 ul { font-size: 1.05cqw; line-height: 1.4; padding-left: 1cqw; margin: 0; }
.content.big .row5 li { margin-bottom: .45cqw; }
.itd.itd3 { grid-template-columns: repeat(3, 1fr); gap: 1.1cqw; }
.content.big .itd3 .kvl { font-size: 1.02cqw; line-height: 1.38; grid-template-columns: 7.4cqw 1fr; gap: .6cqw .8cqw; }
.content.big .itd3 .val { font-size: 1.05cqw; }
.itd3 h3 { font-size: 1.3cqw; }
.cover-mid { margin: auto 0; }
.cover-title { font-size: 5.4cqw; line-height: 1.1; margin: 0 0 1.4cqw; max-width: 80cqw; }
.cover-bar { width: 9cqw; height: .45cqw; border-radius: .3cqw; margin: 0 0 1.4cqw; }
.cover-sub { font-size: 1.9cqw; font-weight: 300; margin: 0; }
.cover-mid .kicker { margin-top: 0; }
.content.big .pre.tight { font-size: 1.15cqw; line-height: 1.4; }
.content.big .pre.tight td { padding: .55cqw .6cqw; }
.content.mon .pre { font-size: 1.05cqw; line-height: 1.3; }
.content.mon .pre td { padding: .38cqw .6cqw; }
.content.mon .pre td:first-child { width: 26%; }
.content.mon .pre td:nth-child(2) { width: 74%; }
.wk .out { margin-top: auto; padding-top: .7cqw; font-size: 1.02cqw; font-weight: 600; }
"""

FOOT = "Pago programado de la TUA · Viva Aerobus · Requerimientos Batch y Generic API – Scheduled Payment (13/11/2026) y sesión del 18/11/2026"
FOOT_INT = "Uso interno · Pago programado de la TUA · Viva Aerobus"
CARD = 'class="card" style="background-color: var(--lighter-violet); color: var(--black)"'
DCARD = 'class="card" style="background-color: var(--dark-violet); color: var(--white)"'
H3 = 'style="color: var(--dark-violet)"'
ROLE = 'class="role" style="color: var(--violet-accent)"'
DROLE = 'class="role" style="color: var(--blue-accent)"'


def slide(title, body, internal=False, extra=""):
    banner = '<div class="banner" style="background-color: var(--black); color: var(--white)">Uso interno · Esta lámina no se debe mostrar al cliente</div>' if internal else ""
    pad = ' style="padding-top: 2.6cqw"' if internal else ""
    h2s = ' style="color: var(--dark-violet); min-height: 0; margin-bottom: .8cqw"' if internal else ' style="color: var(--dark-violet)"'
    f = FOOT_INT if internal else FOOT
    return f'''<section class="slide" style="background-color: var(--white); color: var(--black)">
  <div class="in"{pad}>
    <img src="{BRAND}" alt="Tech and Solve" class="brand">
    {banner}
    <h2{h2s}>{title}</h2>
    <div class="content {extra}">
{body}
    </div>
    <div class="foot" style="color: var(--black)">{f}</div>
  </div>
</section>
'''


def note(text, dark=False):
    st = "background-color: var(--dark-violet); color: var(--white)" if dark else "background-color: var(--lighter-violet); color: var(--black)"
    return f'<div class="note" style="{st}">{text}</div>'


def hl(t):
    return f'<span style="color: var(--violet-accent)">{t}</span>'


def ul(items):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def card(title, items, i=None, role=None, dark=False):
    c, h, r = (DCARD, 'style="color: var(--white)"', DROLE) if dark else (CARD, H3, ROLE)
    rr = f'<div {r}>{role}</div>' if role else ""
    nn = NUM(i) if i is not None else ""
    return f'<div {c}>{rr}<h3 {h}>{nn}{title}</h3>{ul(items)}</div>'


S, I = [], []

# 1 · Portada
S.append(f'''<section class="slide" style="background-color: var(--dark-violet); color: var(--white)">
  <div class="in" style="padding: 5cqw 6cqw">
    <img src="{COVER}" alt="Tech and Solve" class="cover-logo">
    <div class="cover-mid">
      <p class="kicker" style="color: var(--blue-accent)">Propuesta técnica y comercial · Viva Aerobus</p>
      <h1 class="cover-title">Pago programado <span class="hl" style="background-color: var(--violet-accent); color: var(--white)">de la TUA</span></h1>
      <div class="cover-bar" style="background-color: var(--blue-accent)"></div>
      <p class="cover-sub" style="color: var(--lighter-violet)">Cobro automático y monitoreado de la Tarifa de Uso de Aeropuerto</p>
    </div>
    <div class="cover-foot" style="color: var(--lighter-violet)">
      <span>Viva Aerobus · Pago programado de la TUA<br>Propuesta técnica y comercial</span>
      <span style="text-align: right; color: var(--lighter-violet)">Tech and Solve · Noviembre de 2026<br>Documento confidencial</span>
    </div>
  </div>
</section>
''')

# 1b · Propósito de negocio
S.append(slide(f'El propósito: que la TUA {hl("se cobre sola")}, sin doble cobro',
    '<p class="flead">Dos servicios en AWS: el Identificador encuentra cada día las reservas con pago programado a las que les toca cobro, y el Procesador las cobra en Adyen sin CVV, registra el pago en Navitaire y avisa al cliente.</p><div class="row4">' +
    card("Un cobro sin fricción", ["Elige al reservar que la TUA se cobre después, con la tarjeta que usó.", "No vuelve a capturar su tarjeta ni el CVV.", "Recibe un correo con el resultado; si el cobro no se puede procesar, paga manualmente como hoy."], role="Para el cliente") +
    card("TUA cobrada antes del vuelo", ["Cobro domiciliado y automático, un KPI estratégico de Viva.", "Menos reservas llegan al check-in con la TUA pendiente.", "Cada cobro queda registrado en Navitaire, sin cobrar dos veces."], role="Para Viva") +
    card("Las reglas del negocio", ["Monto fijo por pasajero, calculado al reservar.", "Un solo cobro por reserva: todos sus journeys y pasajeros.", "La fecha de cobro depende del bundle de la reserva.", "Si no se puede cobrar, se avisa al cliente por correo.", "Solo reservas con pago programado (<code>VTUP</code>)."], role="Lo que respetamos") +
    card("La TUA es el primer caso", ["La regla de fecha y el tipo de cargo son configurables.", "Si Viva programa otros ancillaries o deja que el cliente elija la fecha, el servicio se extiende sin rehacerse."], role="Lo que viene") +
    '</div>', extra="big"))

# 2 · Entendimiento
S.append(slide(f'Así entendemos la interacción: Generic API, Navitaire, {hl("nuestra solución")}, Adyen y SendGrid',
    svg2 + legend2 + note('<b>Generic API es precondición:</b> las pruebas end-to-end necesitan reservas con <code>VTUP</code> en TEST (lámina 10). Cubrimos solo reservas con pago programado (<code>VTUP</code>). Si el cobro no se puede procesar, solo se notifica al cliente; la DLQ guarda lo que falló por un error técnico, para reprocesarlo.')))

# 3 · Plan de 5 semanas
def wk(n, dates, title, items, out):
    d = '<p class="dates">' + dates + '</p>' if dates else ''
    return f'<div {CARD}><div {ROLE}>Semana {n}</div>{d}<h3 {H3}>{title}</h3>{ul(items)}<p class="out" style="color: var(--dark-violet)">{out}</p></div>'
PLAN_IDX = len(S)  # el plan por semanas no va en la versión del cliente
S.append(slide(f'Plan de {hl("5 semanas")} de implementación', '<div class="row5 wk">' +
    wk(1, "", "Arranque y base", ["Recepción de los contratos de integración congelados (lámina 10).", "Diseño detallado: estados del cobro, mensajes y datos.", "Terraform base en la cuenta de Viva: Fargate, SQS con DLQ, DynamoDB y secrets.", "Clientes de Navitaire y criterios de aceptación con negocio."], "Base desplegada en desarrollo.") +
    wk(2, "", "Identificador de cobros pendientes", ["Scheduled event, fechas por bundle y manifiestos de Navitaire.", "Filtro de reservas con <code>VTUP</code>, deduplicación y encolado en SQS.", "Cliente de Adyen Checkout y mocks.", "Pipeline con promoción a TEST."], "Identificador funcionando en TEST.") +
    wk(3, "", "Procesador de cobros", ["Revalidación de la reserva, tarjeta y monto por pasajero.", "Cobro con compensating transaction: autorizar, registrar en Navitaire y capturar o cancelar.", "Queue de notificaciones y Lambda que envía el correo por SendGrid, con retries y DLQ.", "Alerta de nota o tarjeta inválida."], "Cobro completo en TEST con mocks.") +
    wk(4, "", "Monitoreo en Datadog", ["Métricas de los servicios y logs con criterio de costo.", "Dashboard y 10 monitores, en Terraform.", "Conciliación interna diaria contra Navitaire."], "Operación visible en Datadog.") +
    wk(5, "", "End-to-end y entrega", ["Pruebas con reservas reales de Generic API en TEST.", "Corrección de defectos.", "Aceptación con negocio y entrega del código fuente y las evidencias de prueba."], "Entrega integrada en TEST.") +
    '</div>' + note('Las 5 semanas cuentan desde la fecha de arranque que defina Viva y son semanas hábiles: si caen festivos, el plazo se recorre esos días. La salida a Producción la hace Viva con la misma IaC; el acompañamiento posterior se cotiza aparte.'), extra="big"))

# 10b · Monitoreo en Datadog (parte del alcance)
S.append(slide(f'Dashboard propuesto en {hl("Datadog")}', dash + note('Parte del alcance. Esquema con valores ilustrativos de un día; el detalle de cada monitor está en la lámina siguiente.')))

MON = [
    ("Identificador no corrió", "No llegó la corrida en el horario programado: ese día nadie se cobra", "Sin datos de la métrica de corrida", "Requerimiento"),
    ("Nota, tarjeta o monto inválidos", "Nota de <code>VTUP</code> sin formato válido, tarjeta no encontrada o comentario de TUA ausente: no se cobra", "Métrica de descartes por motivo", "Requerimiento"),
    ("Queue atascada", "El mensaje más antiguo de SQS lleva más del umbral sin procesarse", "Métrica de SQS (integración de AWS)", "Operación"),
    ("Mensajes en la DLQ", "Cobros que fallaron por un error técnico y esperan reproceso", "Métrica de SQS mayor que 0", "Operación"),
    ("Cobros sin cerrar", "Cobros detenidos a medio camino: en proceso, autorizados o registrados sin captura, o encolados sin procesar", "Gauge del estado de los cobros, cada 5 minutos", "Integridad del cobro"),
    ("Diferencias internas", "Un cobro con captura solicitada sin <code>VTUA</code> o sin pago en Navitaire, o una cancelación con <code>VTUA</code>", "Métrica de la conciliación mayor que 0", "Integridad del cobro"),
    ("Errores de Navitaire o Adyen", "Errores o rechazos por límite de llamadas por encima del umbral", "Métrica de llamadas por integración y resultado", "Integraciones"),
    ("Rechazos fuera de lo normal", "La tasa de cobros rechazados se sale de su comportamiento habitual", "Monitor de anomalías", "Operación"),
    ("Correos sin enviar", "Avisos que la Lambda no pudo enviar por SendGrid tras los retries: quedan en la DLQ de notificaciones", "Métrica de SQS de la DLQ de notificaciones", "Cliente"),
    ("Falla al borrar tarjeta", "Quedó vivo en Adyen el token de una tarjeta de un solo uso", "Métrica de borrado por resultado", "Escenario 1"),
]
mt = '<table class="pre tight"><thead><tr style="color: var(--black)"><th>Monitor</th><th>Qué detecta</th></tr></thead><tbody>' + \
    "".join(f'<tr style="color: var(--black)"><td>{a}</td><td>{b}</td></tr>' for a, b, c, d in MON) + '</tbody></table>'
S.append(slide(f'Detalle del dashboard: {hl("monitores")}', mt, extra="mon"))

# 4 · Qué construimos
def comp(role, title, val, items):
    dl = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in items)
    r = f'<div {ROLE}>{role}</div>' if role else ''
    return f'<div {CARD}>{r}<h3 {H3}>{title}</h3><p class="val">{val}</p><dl class="kvl">{dl}</dl></div>'
S.append(slide(f'Qué construimos y entregamos {hl("en TEST")}', '<div class="itd itd3">' +
    comp("", "Identificador de cobros pendientes", "Encuentra cada día las reservas con pago programado a las que les toca cobro.", [
        ("Se construye", "Scheduled event en EventBridge, fechas de cobro por bundle, búsqueda de vuelos y manifiesto de SSR por leg, filtro de reservas con <code>VTUP</code>, deduplicación por reserva y encolado en SQS; re-ejecución por fecha."),
        ("Se prueba", "Con mock de Navitaire y en TEST: bundles, fechas, reservas con solo <code>VTUB</code> que no deben entrar, duplicados y corrida perdida."),
        ("Operación", "Alerta si no corrió, re-ejecución por fecha y traceability por <code>recordLocator</code>."),
    ]) +
    comp("", "Procesador de cobros", "Cobra una sola vez y solo cuando Navitaire puede registrar el pago.", [
        ("Se construye", "Revalidación de la reserva, ubicación de la tarjeta en Adyen, cobro con compensating transaction, registro del pago en Navitaire por pasajero y journey, aviso al cliente publicado en una queue de notificaciones, que una Lambda envía por SendGrid con retries, DLQ y conciliación interna diaria."),
        ("Se prueba", "Los tres escenarios de tarjeta, caída de Navitaire después de autorizar, commit sin respuesta, pago manual previo y cobro rechazado; al final, end-to-end con Generic API."),
        ("Operación", "Alerta si la nota, la tarjeta o el monto no son válidos: no se cobra."),
    ]) +
    comp("", "Dashboard y monitores en Datadog", "Muestra en un solo lugar si los cobros salieron y avisa cuando algo se detiene.", [
        ("Se construye", "Métricas del Identificador, del Procesador y de la Lambda de notificación; logs con criterio de costo; dashboard con el funnel del día y 10 monitores, todo en Terraform (láminas 5 y 6)."),
        ("Se prueba", "Cada monitor se dispara en TEST forzando su caso: corrida que no ocurre, mensajes en la DLQ, cobro sin cerrar, diferencia interna y correo sin enviar."),
        ("Operación", "Avisos al canal que defina Viva, con los umbrales acordados."),
    ]) + '</div>' + note('<b>Todo se entrega desplegado e integrado en el ambiente de TEST de Viva</b>, no en Producción: Viva despliega en Producción con la misma IaC. Sin reservas de Generic API en TEST, las pruebas end-to-end solo se validan con mocks; y como aún no hay estimado de volumen, se prueba con un volumen supuesto acordado.', dark=True), extra="big"))

# 11 · Lo que entregamos
S.append(slide(f'Entregables {hl("del servicio")}', '<div class="tc">' +
    card("Código e infraestructura", ["Identificador y Procesador en NestJS, contenerizados en ECS Fargate, con las reglas de fecha y cargo configurables, y la Lambda de notificación.", "IaC en Terraform por módulos, parametrizada por ambiente, sobre la cuenta y la red de Viva.", "Pipelines de build, IaC y promoción, con rollback."], 1) +
    card("Pruebas y evidencias", ["Unit tests de cada historia y análisis de calidad del código en el Sonar de Viva.", "Mocks de Navitaire y Adyen.", "Evidencias funcionales, de integración y end-to-end del proceso de cobro.", "Aceptación con el negocio de Viva."], 2) +
    card("Seguridad", ["Sin datos de tarjeta en el servicio: solo referencias y tokens de Adyen.", "Secrets en Secrets Manager y cifrado con KMS; sin endpoints expuestos a Internet.", "Corrección de los hallazgos de la revisión de seguridad de Viva, un ciclo."], 3) +
    card("Operación", ["Dashboard y 10 monitores en Datadog, incluidas las alertas del requerimiento (láminas 5 y 6).", "Traceability por reserva y por cobro.", "Conciliación interna diaria."], 4) +
    card("Entregables", ["<b>Código fuente</b> de los dos servicios, la IaC y los pipelines, en el repositorio de Viva.", "<b>Evidencias de prueba confirmadas:</b> funcionales, de integración y end-to-end, aceptadas por el negocio de Viva."], 5) +
    '</div>' + note('<b>Fuera de alcance:</b> confirmar en Adyen las capturas y cancelaciones (lo hace Viva en su conciliación financiera), seguir la entrega final de los correos de SendGrid, reservas sin <code>VTUP</code> (pago posterior manual con solo <code>VTUB</code>, o TUA ya pagada), Generic API y su flujo de pago, el frontend, crear el SSR <code>VTUP</code> en Navitaire, diseñar las plantillas de correo (las define Marketing), desplegar o probar en Producción, ejecutar pruebas de seguridad o de penetración (las hace Viva) y cualquier acción sobre la reserva, además del correo al cliente, cuando el cobro no se puede procesar.')))

# 4 · Tiempo y costo
TC_TITLE = f'Tiempo y costo: {hl("fijos")} sobre este alcance'
TC_BODY = '''<div class="opts">
  <div class="opt sel" style="background-color: var(--lighter-violet); color: var(--black)">
    <div class="role" style="color: var(--violet-accent)">Tiempo</div>
    <div class="opt-h" style="color: var(--dark-violet)"><b>5 semanas</b><span>de implementación</span></div>
    <p>Desde la <b>fecha de arranque que defina Viva</b>, con los dos servicios entregados e integrados en TEST.</p>
    <ul>
      <li>Semanas hábiles: si caen festivos, el plazo se recorre esos días.</li>
      <li>Cuenta desde que están definidos los contratos de integración y listos los prerrequisitos de arranque (lámina 10).</li>
      <li>Deja a Viva lista para integrar el frontend y salir a Producción con la IaC entregada.</li>
    </ul>
  </div>
  <div class="opt sel" style="background-color: var(--lighter-violet); color: var(--black)">
    <div class="role" style="color: var(--violet-accent)">Costo</div>
    <div class="opt-h" style="color: var(--dark-violet)"><b>USD 20.489,94</b><span>precio fijo</span></div>
    <p>Un solo valor por todo el alcance de esta propuesta. Forma de pago: <b>mes vencido</b>.</p>
    <ul>
      <li><b>Incluye:</b> los dos servicios, IaC y pipeline, pruebas y evidencias, conciliación interna, el dashboard y los monitores en Datadog, el código fuente y las evidencias de prueba confirmadas (lámina 8).</li>
      <li><b>Se cobra aparte:</b> cambios en los contratos de integración, cambios o fallas de componentes externos (lámina 10), y el acompañamiento posterior o a Producción.</li>
      <li><b>Soporte recomendado:</b> 2 semanas después de la entrega, USD 6.850,00, aparte de este precio.</li>
    </ul>
  </div>
</div>''' + note('<b>Tiempo y precio son fijos porque los contratos se definen y congelan al arrancar</b> y las integraciones están implementadas para cuando se prueba. Lo que cambie después se estima y se aprueba como control de cambios antes de ejecutarlo.')
S.append(slide(TC_TITLE, TC_BODY, extra="big"))

# 6 · Prerrequisitos
def pre(role, title, items, dark=False):
    c, h, r = (DCARD, 'style="color: var(--white)"', DROLE) if dark else (CARD, H3, ROLE)
    return f'<div {c}><div {r}>{role}</div><h3 {h}>{title}</h3>{ul(items)}</div>'
S.append(slide(f'Prerrequisitos y {hl("control de cambios")}',
    '<p class="prelead" style="color: var(--black)">El proyecto arranca con <b>los contratos de integración definidos</b> y los prerrequisitos listos, y <b>las integraciones deben estar implementadas en TEST cuando se va a probar</b>. Si algo falta, la fecha se corre lo mismo. Si después del inicio cambia un contrato de integración, o un componente externo (Navitaire, Adyen, SendGrid, Generic API o la infraestructura AWS de Viva) cambia, falla o no está disponible, <b>es control de cambios</b>. En ambos casos el tiempo adicional se cobra aparte.</p><div class="pregrid">' +
    pre("Antes de arrancar", "Contratos definidos y congelados", ["<b>Navitaire:</b> búsqueda de vuelos, manifiesto de SSR, reserva, alta y baja de SSR, <code>paymentAdd</code> y commit.", "<b>Adyen Checkout:</b> tarjetas guardadas, pago, captura, cancelación y borrado de token.", "<b>SendGrid:</b> envío con plantilla. <b>Generic API:</b> nota de <code>VTUP</code>, comentario de TUA y SSR.", "<b>Un cambio posterior es control de cambios y se cobra aparte.</b>"], dark=True) +
    pre("Antes de arrancar", "Permisos, accesos y ambiente estable", ["<b>Permisos y accesos suficientes</b> para desarrollar, configurar, integrar, probar y cargar datos de prueba en desarrollo y TEST, para nuestro equipo y nuestro tester: AWS (incluidos IAM y el despliegue del pipeline), Navitaire, Adyen, SendGrid, Datadog, Terraform y Sonar.", "<b>Ambientes de desarrollo y TEST homologados y estables:</b> misma configuración, versiones e integraciones, salvo parámetros y secrets, con Navitaire, Adyen y SendGrid de prueba disponibles.", "<b>Lineamientos de Viva claros</b> para AWS, SQS, DynamoDB, Terraform y CI/CD, si existen.", "Cuenta de servicio de Navitaire con rol de agente y credencial de Adyen Checkout para <code>VB_WEB</code>, con manual capture."]) +
    pre("Antes de arrancar", "Navitaire", ["Búsqueda de vuelos, paginación y límites confirmados.", "Registro del pago: campos de <code>paymentAdd</code> y cargo de <code>VTUA</code> por pasajero."]) +
    pre("Antes de arrancar", "SendGrid y Datadog", ["ID de plantillas de SendGrid, o una de prueba.", "Integración de AWS en Datadog, API keys, canal de avisos y umbrales."]) +
    pre("Antes de probar", "Integraciones implementadas en TEST", ["<b>Generic API</b> generando reservas con <code>VTUP</code> en los tres escenarios, y colección Postman.", "<b>Navitaire, Adyen y SendGrid</b> de prueba operando según los contratos acordados.", "Volumen supuesto acordado y responsable de negocio para la aceptación."]) +
    pre("Durante el proyecto", "Para no perder ritmo", ["<b>Liberar y probar en TEST sin interrupciones:</b> sin ventanas de aprobación ni ambientes bloqueados.", "Patrocinador y un responsable por prerrequisito.", "Respuesta a dudas en 2 días hábiles.", "Revisión de seguridad de Viva, si aplica, con hallazgos en 3 días hábiles."]) +
    '</div>'))

# 12 · Calidad
S.append(slide(f'Calidad desde el inicio, {hl("de la mano del negocio")}',
    '<p class="flead">Al inicio se acuerdan con el negocio los criterios y los datos de prueba, y cada componente se prueba en cuanto se despliega. Al cierre se confirma lo ya probado, end-to-end con Generic API.</p><div class="row4">' +
    card("Criterios que Viva aprueba", ["Criterios de aceptación en formato Given / When / Then.", "Reglas verificables: bundles, fechas, escenarios e idempotency."], role="Al inicio") +
    card("Terminado quiere decir probado", ["Los unit tests se escriben al construir cada historia.", "Cada componente se prueba en cuanto se despliega."], role="Durante la construcción") +
    card("Sin esperar a los sistemas reales", ["Mocks de Navitaire y de Adyen.", "API tests automatizados en el pipeline.", "Casos de compensación forzados: caída después de autorizar y commit sin respuesta.", "Cada monitor de Datadog se dispara en TEST forzando su caso."], role="Integración") +
    card("Con el negocio de Viva", ["Pruebas end-to-end con reservas de Generic API en TEST.", "Aceptación final de Viva."], role="Al cierre") +
    '</div><div class="who4">' +
    '<div style="background-color: var(--lighter-violet); color: var(--black)"><b>Desarrollo</b>Diseño, construcción, unit tests, IaC y pipeline.</div>' +
    '<div style="background-color: var(--lighter-violet); color: var(--black)"><b>Calidad</b>Criterios, pruebas funcionales, de integración y end-to-end.</div>' +
    '<div style="background-color: var(--lighter-violet); color: var(--black)"><b>Generic API</b>Reservas con <code>VTUP</code> en TEST para las pruebas end-to-end.</div>' +
    '<div style="background-color: var(--lighter-violet); color: var(--black)"><b>Viva</b>Aceptación y revisión de seguridad, si aplica.</div>' +
    '</div>', extra="big"))

# 13 · Dudas
S.append(slide(f'Dudas {hl("a resolver")}', '<div class="dq">' +
    f'<div {CARD}><h3 {H3}>{NUM(1)}¿Dónde y con qué se construye?</h3>' + ul(["¿Qué cuenta AWS, qué red y qué equipo la administra?", "¿Qué CI/CD usa Viva, y hay módulos o plantillas de Terraform obligatorios?", "¿Hay lineamientos de Viva para SQS y DynamoDB?"]) + '</div>' +
    f'<div {CARD}><h3 {H3}>{NUM(2)}¿Cómo se registra el cobro en Navitaire?</h3>' + ul(["¿Con qué campos se hace <code>paymentAdd</code> de un pago autorizado fuera de su gateway?", "¿Cómo queda el cargo de <code>VTUA</code> por pasajero y journey?"]) + '</div>' +
    f'<div {CARD}><h3 {H3}>{NUM(3)}¿Qué decide producto?</h3>' + ul(["Texto del correo cuando el cobro no se puede procesar.", "Tras un cobro no procesado, ¿se borra la tarjeta de un solo uso (escenario 1)?", "Si la reserva no tiene el comentario de TUA, ¿se avisa al cliente? El requerimiento no lo define; mientras tanto se trata como la nota inválida: no se cobra y se alerta."]) + '</div>' +
    '</div>' + note('<b>Otras dudas abiertas.</b> Con Adyen: vigencia del token de un solo uso en la bóveda. Con Generic API: cuándo habrá reservas con <code>VTUP</code> en TEST, si quita <code>VTUP</code> al cambiar journeys o pasajeros, y si el escenario 1 lleva el <code>basketId</code> solo o como <code>TUA-{basketId}</code>. Con Navitaire: si existe una búsqueda directa de reservas por SSR (<code>VTUP</code>), y paginación y límites del manifiesto.')))

# 14 · Términos y condiciones
S.append(slide("Términos y condiciones", '<div class="tc">' +
    card("Alcance", ["Solo reservas con pago programado (<code>VTUP</code>).", "Los dos servicios y lo de la lámina 8, entregados en TEST.", "No incluye Generic API, el frontend, Producción ni pruebas de seguridad o de penetración: las hace Viva y corregimos sus hallazgos, un ciclo."], 1) +
    card("Ambientes", ["Trabajamos en desarrollo y TEST, en la cuenta AWS que defina Viva, con el pipeline entregado.", "Viva da permisos y accesos suficientes para desarrollar, configurar, integrar, probar y cargar datos de prueba, y mantiene desarrollo y TEST homologados (misma configuración salvo parámetros y secrets) y estables. Los ajustes por diferencias entre ambientes se cobran aparte.", "Liberamos y probamos en TEST sin interrupciones, y nuestro tester tiene permisos para operar allí; las interrupciones se cobran aparte.", "TEST cuenta con Navitaire, Adyen y SendGrid de prueba.", "Producción la despliega Viva con la misma IaC."], 2) +
    card("Contratos y cambios", ["Los contratos de integración se entregan al inicio y quedan congelados (lámina 10).", "Los cambios posteriores en esos contratos son <b>control de cambios</b> y se cobran aparte.", "Los cambios o fallas de componentes externos que afecten la implementación se cobran aparte."], 3) +
    card("Tiempos", ["Tiempo y precio fijos sobre este alcance.", "5 semanas hábiles desde el arranque que defina Viva, con los contratos definidos y los prerrequisitos listos.", "Si un prerrequisito o una integración en TEST no está cuando se necesita, la fecha se corre lo mismo y ese tiempo se cobra aparte.", "Cambios de reglas, como que el cliente elija la fecha, se estiman aparte."], 4) +
    card("Aceptación", ["Viva acepta la entrega en TEST en 2 días hábiles, con el responsable de negocio que designe.", "Las dudas de la lámina 12 se resuelven con Viva; si una respuesta cambia el alcance, es control de cambios."], 5) +
    f'<div {CARD}><h3 {H3}>{NUM(6)}Inversión</h3><ul><li>Valor del proyecto: <b>USD 20.489,94</b>, precio fijo.</li><li>Forma de pago: <b>mes vencido</b>.</li><li>Soporte recomendado después de la entrega: 2 semanas, <b>USD 6.850,00</b>, aparte del valor del proyecto.</li></ul></div>' +
    '</div>'))

# ---------------- Internas ----------------
I.append(slide(f'Arquitectura AWS de la {hl("solución")}', arch + '''<div class="archnotes">
  <div><b>1 · Identificar.</b> EventBridge Scheduler llama al endpoint del Identificador en Fargate; este lee Navitaire, deduplica contra DynamoDB y encola en SQS.</div>
  <div><b>2 · Cobrar.</b> Una Lambda toma cada mensaje y llama al endpoint del Procesador, como se conversó con Héctor. Alternativa más simple: que el servicio consuma SQS directamente.</div>
  <div><b>3 · Estado y compensación.</b> DynamoDB guarda cada cobro (iniciado, autorizado, confirmado, cobrado, cancelado), y evita que una reserva con cobro fallido se vuelva a encolar.</div>
  <div><b>4 · Sin webhooks.</b> Captura y cancelación responden «received» y se toman como solicitadas; la confirmación del lado de Adyen la hace Viva en su conciliación financiera. No hay public ingress.</div>
  <div><b>5 · Notificaciones.</b> El Procesador publica cada aviso en una queue SQS; una Lambda lo envía por SendGrid, con retries y DLQ propia. Salida por NAT; si un tercero exige IP fija, Viva la registra.</div>
  <div><b>6 · Un solo intento.</b> Si el cobro no se puede procesar, se notifica al cliente y la reserva no vuelve a la queue.</div>
</div>''', internal=True))

risks = [
    ("R1", "El intervalo configurado es más corto que el horario del Identificador", "Ya no aplica: un solo intento, sin retries", "—"),
    ("R2", "Se borra la tarjeta guardada: la nota de <code>VTUP</code> lleva <code>|</code> en los tres escenarios", "El escenario se lee del tipo de la parte izquierda: <code>basketId</code> (GUID) o <code>customerNumber</code>; sin cambiar Generic API", "Procesador · lectura de la reserva"),
    ("R3", "El requerimiento cobra por journey; negocio, por reserva", "Cobro completo y llave reserva + intento", "Identificador y Procesador"),
    ("R4", "ZERO: no caben tres intentos en un día", "Ya no aplica: un solo intento, sin retries", "—"),
    ("R5", "No se puede leer la queue de Navitaire", "Resuelto: SQS con DLQ como transporte y DynamoDB como estado", "Infraestructura"),
    ("R6", "Cliente cobrado con la reserva pendiente", "Compensating transaction con manual capture y conciliación interna", "Procesador · cobro"),
    ("R7", "Límites de llamadas de Navitaire sin dato de volumen", "Concurrencia configurable, espera ante rechazos y volumen supuesto", "Cliente de Navitaire"),
    ("R8", "Falta el comentario con el monto de la TUA", "Sin monto no se procesa: se marca como fallido y se alerta; si se avisa al cliente queda en dudas", "Procesador · lectura de la reserva"),
    ("R9", "Doble cobro si el cliente paga manualmente después de encolado", "Releer la reserva justo antes de cobrar", "Procesador · revalidación"),
    ("R10", "Un cambio en un contrato o componente externo durante las 5 semanas", "Contratos congelados el día 1; cambios por control de cambios, cobrados aparte (lámina 10)", "Gestión del proyecto"),
]
rt = '<table class="pre risk"><thead><tr style="color: var(--black)"><th>ID</th><th>Riesgo</th><th>Cómo lo cubre el plan</th><th>Dónde</th></tr></thead><tbody>' + \
    "".join(f'<tr style="color: var(--black)"><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in risks) + '</tbody></table>'
I.append(slide(f'Riesgos del análisis y {hl("dónde quedaron en el plan")}', rt +
    note('Detalle de R1 a R9, con su ejemplo paso a paso, en <code>scheduled-payment/analisis.md</code>, sección 7. R2 solo pide confirmar el formato del escenario 1 en la semana 1; R1 y R4 ya no aplican: ante un fallo solo se notifica al cliente.'), internal=True))


TEAM_IDX = len(I)
I.append(slide(f'Equipo y {hl("licencias de Claude")}', '<div class="dq">' +
    card("Equipo", ["<b>Líder técnico al 100&nbsp;%</b> las 5 semanas: diseño, construcción, unit tests, IaC, pipeline, monitoreo en Datadog y entrega del código. Unas 176 h, descontando los festivos del 8 y el 25 de diciembre y el 1 de enero si se arranca el 30 de noviembre.", "<b>Tester al 50&nbsp;%</b>, con licencia de Claude (plan Max): criterios de aceptación, pruebas funcionales, de integración y end-to-end, y la prueba de monitoreo. Unas 88 h.", "No se muestra al cliente: la propuesta solo compromete alcance, plazo y precio."], 1) +
    card("Licencias de Claude", ["<b>Líder técnico · plan Ultra:</b> USD 200 al mes. Las 5 semanas pasan de un mes: 2 meses, USD 400. Se elige porque no tiene el límite de 5 horas y da 10 veces el uso de Pro cada semana.", "<b>Tester · plan Max:</b> USD 100 al mes, con 5 veces el uso de Pro: 2 meses, USD 200. Para diseñar casos, automatizar pruebas y preparar evidencias.", "Total de licencias: USD 600. Se incorporan al valor del proyecto, sin línea aparte para el cliente: no se subsidian. Precios de la página oficial de Claude, a validar antes de cerrar la cotización.", "Si Viva contrata acompañamiento posterior, se suma un mes por licencia por cada mes adicional."], 2) +
    card("Capacidad: a cuidar", ["La estimación por actividades que hicimos antes sumaba unas 610 h, sin el dashboard de Datadog; este equipo suma unas 264 h en 5 semanas.", "El plan depende de la productividad con Claude y de que contratos y prerrequisitos estén listos a tiempo, sin cambios.", "Por eso la propuesta protege el plazo con contratos congelados y control de cambios cobrado aparte (lámina 10)."], 3) +
    '</div>', internal=True, extra="big"))

HEAD = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tech and Solve - Pago programado de la TUA · Viva Aerobus</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>{STYLE}</style>
</head>
<body>
'''
TAIL = '''<div class="hint" style="background-color: var(--white); color: var(--black)">Flechas para navegar · Ctrl/Cmd+P para PDF</div>
<script>
  const slides = [...document.querySelectorAll('.slide')];
  const current = () => slides.findIndex(s => s.getBoundingClientRect().bottom > innerHeight / 2);
  addEventListener('keydown', e => {
    const i = current();
    if (['ArrowRight', 'ArrowDown', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); slides[Math.min(i + 1, slides.length - 1)].scrollIntoView({ behavior: 'smooth', block: 'center' }); }
    if (['ArrowLeft', 'ArrowUp', 'PageUp'].includes(e.key)) { e.preventDefault(); slides[Math.max(i - 1, 0)].scrollIntoView({ behavior: 'smooth', block: 'center' }); }
  });
</script>
</body>
</html>
'''
def renum(html, f):
    html = re.sub(r"láminas (\d+) y (\d+)", lambda m: f"láminas {f(int(m.group(1)))} y {f(int(m.group(2)))}", html)
    return re.sub(r"lámina (\d+)", lambda m: f"lámina {f(int(m.group(1)))}", html)
os.makedirs(outdir, exist_ok=True)
base = os.path.join(outdir, "propuesta-viva-scheduled-payment-v1")
open(base + "-fuente-con-internas.html", "w", encoding="utf-8").write(HEAD + "\n".join(S + I) + TAIL)
CLIENT = [s for k, s in enumerate(S) if k != PLAN_IDX]
plan_no = PLAN_IDX + 1
_shift = lambda n: n - 1 if n > plan_no else n
client_html = renum("\n".join(CLIENT), _shift)
open(base + "-cliente.html", "w", encoding="utf-8").write(HEAD + client_html + TAIL)
# Equipo de trabajo: una lámina por rol (uso interno de Tech and Solve)
TEAM_CSS = """
.rolegrid { display: grid; grid-template-columns: .8fr 1.75fr; gap: 1.4cqw; flex: 1; min-height: 0; }
.rolecard { border-radius: 1cqw; padding: 1.8cqw 2cqw; display: flex; flex-direction: column; gap: 1.2cqw; }
.rolecard .rname { font-size: 2.6cqw; font-weight: 700; line-height: 1.15; margin: 0; }
.rolecard .rk { font-size: .9cqw; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; margin: 0 0 .25cqw; }
.rolecard .rv { font-size: 1.6cqw; font-weight: 600; line-height: 1.25; margin: 0; }
.rolecard .rs { font-size: 1.05cqw; line-height: 1.4; margin: .3cqw 0 0; }
.know { border-radius: 1cqw; padding: 1.4cqw 1.7cqw; }
.know h3 { font-size: 1.35cqw; margin: 0 0 .8cqw; }
.know .kgrid { display: grid; grid-template-columns: 1fr 1fr; gap: .9cqw 1.8cqw; }
.know .kgrid b { display: block; font-size: 1.02cqw; margin-bottom: .2cqw; }
.know .kgrid ul { font-size: .92cqw; line-height: 1.33; padding-left: 1cqw; margin: 0; }
.know .kgrid li { margin-bottom: .15cqw; }
"""
def role_slide(nombre, dedicacion, ded_sub, ia, ia_costo, ia_sub, titulo_k, grupos, titulo=None):
    kg = "".join(f'<div><b style="color: var(--dark-violet)">{g}</b>{ul(items)}</div>' for g, items in grupos)
    body = f'''<div class="rolegrid">
  <div class="rolecard" style="background-color: var(--dark-violet); color: var(--white)">
    <p class="rk" style="color: var(--blue-accent)">Rol</p><p class="rname">{nombre}</p>
    <div><p class="rk" style="color: var(--blue-accent)">Dedicación</p><p class="rv">{dedicacion}</p><p class="rs" style="color: var(--lighter-violet)">{ded_sub}</p></div>
    <div><p class="rk" style="color: var(--blue-accent)">Herramienta de IA</p><p class="rv">{ia}</p><p class="rv" style="color: var(--blue-accent)">{ia_costo}</p><p class="rs" style="color: var(--lighter-violet)">{ia_sub}</p></div>
  </div>
  <div class="know" style="background-color: var(--lighter-violet); color: var(--black)"><h3 style="color: var(--dark-violet)">{titulo_k}</h3><div class="kgrid">{kg}</div></div>
</div>'''
    return slide(titulo or f'Equipo de trabajo: {hl(nombre.lower())}', body, internal=True)

LT = role_slide("Líder técnico", "100&nbsp;% las 5 semanas", "Unas 176 h, descontando festivos. Diseña, construye, prueba, despliega y entrega el código end-to-end.",
    "Claude · plan Ultra", "USD 200 al mes", "Sin el límite de 5 horas y con 10 veces el uso de Pro cada semana. 2 meses: USD 400.",
    "Conocimientos para desarrollar la solución end to end", [
    ("Backend", ["NestJS y TypeScript: modules, dependency injection, HTTP clients, error handling", "Unit testing con Jest, mocks y test doubles", "AWS Lambda en TypeScript con SQS event source y partial batch responses"]),
    ("AWS", ["Amazon ECS on Fargate y Amazon ECR", "Amazon SQS: dead-letter queue, visibility timeout, redrive policy", "Amazon DynamoDB: conditional writes, GSI, idempotency", "EventBridge Scheduler, Secrets Manager, KMS, IAM least privilege, VPC y NAT Gateway"]),
    ("Infrastructure as Code y CI/CD", ["Terraform: modules, remote state, per-environment variables", "CI/CD pipelines: build, test, container image, promotion a TEST y rollback", "Static code analysis con SonarQube"]),
    ("Navitaire (dotREZ / NSK API)", ["Agent authentication y session management", "Flight manifest y SSR manifest", "SSR add/delete, <code>paymentAdd</code>, booking commit y booking comments"]),
    ("Adyen Checkout API", ["Tokenization y stored payment methods (<code>storedPaymentMethods</code>)", "Merchant-initiated transactions sin CVV (<code>ContAuth</code>, <code>UnscheduledCardOnFile</code>)", "Manual capture, cancel e <code>idempotency-key</code>"]),
    ("Event-driven architecture", ["Producers y consumers desacoplados por queues, scheduled events con EventBridge", "At-least-once delivery, idempotent consumers, retries con backoff, DLQ y redrive", "Saga / compensating transaction y eventual consistency", "SendGrid con dynamic templates como consumer de notificaciones"]),
    ("Observability (Datadog)", ["Datadog Agent como sidecar en Fargate: DogStatsD, APM y FireLens; Datadog Lambda extension", "Custom metrics, distribution metrics y tag cardinality", "Dashboards y monitors as code con Terraform"]),
    ("Security y AI-assisted development", ["PCI-aware handling: sin card data, log masking y secrets management", "Claude Code para design, coding, testing, IaC y documentación"]),
    ])
QA = role_slide("Tester", "50&nbsp;% las 5 semanas", "Unas 88 h. Define criterios con negocio, prueba cada componente, ejecuta la prueba de monitoreo y prepara las evidencias.",
    "Claude · plan Max", "USD 100 al mes", "5 veces el uso de Pro. 2 meses: USD 200.",
    "Conocimientos para asegurar la calidad de la solución", [
    ("Test design", ["Acceptance criteria en Gherkin (Given / When / Then)", "Traceability matrix de requisito a evidencia", "Edge cases: bundles, fechas, escenarios de tarjeta, pago manual previo"]),
    ("API testing", ["Postman o equivalente, con collections y environments", "API test automation en el CI/CD pipeline", "Lectura de API contracts y JSON responses"]),
    ("Dominio de la aerolínea", ["Navitaire y SkySpeed: SSR <code>VTUB</code>, <code>VTUP</code> y <code>VTUA</code>, booking comments y payments", "Payment flow de Generic API para generar test bookings"]),
    ("Payments testing", ["Adyen test environment y test cards", "Casos de authorisation refused, cancel y capture"]),
    ("Integration y resilience testing", ["Mocks y stubs de Navitaire y Adyen", "Fault injection: errores técnicos, mensajes a la DLQ, commit timeout", "Event-driven testing: mensajes duplicados, retries, redrive desde la DLQ y eventual consistency", "End-to-end testing con Generic API en TEST"]),
    ("AWS y Datadog (read-only)", ["Revisar SQS, DLQ, DynamoDB y CloudWatch Logs en la AWS Console", "Leer dashboards y logs, y verificar que cada monitor dispara en Datadog"]),
    ("Test evidence", ["Evidencias funcionales, de integration y end-to-end", "Bug reporting y regression testing"]),
    ("AI-assisted testing", ["Claude para test case design, test data generation y test automation"]),
    ])
SOP = role_slide("Líder técnico", "50&nbsp;% inicial, bajo demanda", "Unas 40 h en las 2 primeras semanas. El soporte se calcula por el tiempo dedicado, sin tester al inicio.",
    "Claude · plan Max", "USD 100 al mes", "5 veces el uso de Pro. Por las 2 semanas de soporte inicial: 1 mes, USD 100.",
    "Soporte después de la entrega en TEST", [
    ("Cómo se calcula", ["Bajo demanda: se calcula por el tiempo efectivamente dedicado", "Aparte del precio fijo de la implementación"]),
    ("Propuesta inicial", ["Líder técnico al 50&nbsp;% durante 2 semanas", "Sin tester: el LT cubre las pruebas de los ajustes", "Claude Max por esas 2 semanas"]),
    ("Qué cubre", ["Dudas y ajustes de los dos servicios, la IaC y el dashboard en Datadog", "Análisis de mensajes en la DLQ y de cobros con <code>DIFERENCIA</code> en la conciliación", "Acompañamiento a Viva en la integración del frontend y la salida a Producción"]),
    ("Si la demanda crece", ["Se amplía la dedicación del LT o se suma el tester, con aprobación de Viva"]),
    ], titulo=f'Equipo de trabajo: {hl("soporte")}')
# Tiempo y costo al inicio del equipo de trabajo, con las láminas numeradas como en la propuesta del cliente
TC_TEAM = slide(TC_TITLE, re.sub(r"lámina (\d+)\)", r"lámina \1 de la propuesta)", renum(TC_BODY, _shift)), internal=True, extra="big")
open(os.path.join(outdir, "equipo-de-trabajo.html"), "w", encoding="utf-8").write(
    HEAD.replace("Pago programado de la TUA · Viva Aerobus</title>", "Equipo de trabajo · Pago programado de la TUA</title>").replace("</style>", TEAM_CSS + "</style>", 1) + TC_TEAM + LT + QA + SOP + TAIL)
print("cliente", len(CLIENT), "fuente", len(S) + len(I))
