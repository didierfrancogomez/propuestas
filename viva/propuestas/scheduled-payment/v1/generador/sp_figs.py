# Figuras reutilizadas por sp_gen.py
NUM = lambda i: f'<span class="n" style="background-color: var(--violet-accent); color: var(--white)">{i}</span>'
svg2 = """<svg viewBox="0 0 1200 330" width="100%" role="img" aria-label="Proceso del pago programado: Generic API, Navitaire, Identificador de cobros pendientes, SQS, Procesador de cobros, Adyen y SendGrid">
  <defs>
    <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#280265"/></marker>
    <marker id="aw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#EBEBFF"/></marker>
  </defs>
  <rect x="2" y="24" width="170" height="290" rx="16" fill="#FFFFFF" stroke="#280265" stroke-width="2.5" stroke-dasharray="9 6"/>
  <text x="87" y="16" text-anchor="middle" font-size="13" font-weight="700" fill="#280265" letter-spacing="1.5">PRECONDICIÓN</text>
  <text x="87" y="72" text-anchor="middle" font-size="21" font-weight="700" fill="#280265">Generic API</text>
  <text x="87" y="94" text-anchor="middle" font-size="13" fill="#000000">Flujo de pago</text>
  <text x="87" y="140" text-anchor="middle" font-size="12.5" fill="#000000">Crea la reserva</text>
  <text x="87" y="158" text-anchor="middle" font-size="12.5" fill="#000000">con pago programado</text>
  <text x="87" y="196" text-anchor="middle" font-size="12.5" fill="#000000">Tokeniza la tarjeta</text>
  <text x="87" y="214" text-anchor="middle" font-size="12.5" fill="#000000">en Adyen</text>
  <text x="87" y="282" text-anchor="middle" font-size="12" fill="#000000">En desarrollo, fuera</text>
  <text x="87" y="298" text-anchor="middle" font-size="12" fill="#000000">de esta propuesta</text>
  <rect x="222" y="24" width="190" height="290" rx="16" fill="#FFFFFF" stroke="#280265" stroke-width="2.5"/>
  <text x="317" y="16" text-anchor="middle" font-size="13" font-weight="700" fill="#280265" letter-spacing="1.5">EXISTENTE</text>
  <text x="317" y="72" text-anchor="middle" font-size="21" font-weight="700" fill="#280265">Navitaire</text>
  <text x="317" y="94" text-anchor="middle" font-size="13" fill="#000000">Reservas</text>
  <text x="317" y="132" text-anchor="middle" font-size="12.5" fill="#000000">Manifiestos y SSR:</text>
  <text x="317" y="150" text-anchor="middle" font-size="12.5" fill="#000000">quién tiene VTUP</text>
  <text x="317" y="188" text-anchor="middle" font-size="12.5" fill="#000000">Nota de VTUP: la tarjeta</text>
  <text x="317" y="206" text-anchor="middle" font-size="12.5" fill="#000000">Comentario: el monto</text>
  <text x="317" y="244" text-anchor="middle" font-size="12.5" fill="#000000">Registro del pago:</text>
  <text x="317" y="262" text-anchor="middle" font-size="12.5" fill="#000000">VTUA y paymentAdd</text>
  <rect x="462" y="24" width="476" height="290" rx="16" fill="#280265"/>
  <text x="700" y="52" text-anchor="middle" font-size="19" font-weight="700" fill="#FFFFFF">Solución Tech and Solve</text>
  <text x="700" y="72" text-anchor="middle" font-size="12.5" fill="#EBEBFF">AWS, por eventos · alcance de esta propuesta</text>
  <rect x="482" y="88" width="148" height="44" rx="8" fill="#FFFFFF"/>
  <text x="556" y="106" text-anchor="middle" font-size="12" font-weight="700" fill="#280265">EventBridge</text>
  <text x="556" y="122" text-anchor="middle" font-size="12" fill="#280265">evento programado</text>
  <rect x="660" y="88" width="258" height="44" rx="8" fill="#EBEBFF"/>
  <text x="789" y="106" text-anchor="middle" font-size="13" font-weight="700" fill="#280265">Identificador de</text>
  <text x="789" y="123" text-anchor="middle" font-size="13" font-weight="700" fill="#280265">cobros pendientes</text>
  <rect x="660" y="152" width="258" height="34" rx="8" fill="#EBEBFF"/>
  <text x="789" y="174" text-anchor="middle" font-size="13" font-weight="600" fill="#280265">SQS · un mensaje por reserva</text>
  <rect x="482" y="152" width="148" height="34" rx="8" fill="#FFFFFF" stroke="#EBEBFF" stroke-width="1.5" stroke-dasharray="5 3"/>
  <text x="556" y="174" text-anchor="middle" font-size="12.5" font-weight="600" fill="#280265">DLQ</text>
  <rect x="660" y="206" width="258" height="44" rx="8" fill="#EBEBFF"/>
  <text x="789" y="233" text-anchor="middle" font-size="13" font-weight="700" fill="#280265">Procesador de cobros</text>
  <rect x="482" y="268" width="210" height="30" rx="8" fill="#FFFFFF"/>
  <text x="587" y="288" text-anchor="middle" font-size="12" font-weight="600" fill="#280265">DynamoDB · estado del cobro</text>
  <rect x="702" y="268" width="216" height="30" rx="8" fill="#EBEBFF"/>
  <text x="810" y="288" text-anchor="middle" font-size="12" font-weight="700" fill="#280265">Notificaciones · SQS + Lambda</text>
  <line x1="789" y1="250" x2="789" y2="264" stroke="#EBEBFF" stroke-width="2" marker-end="url(#aw)"/>
  <line x1="630" y1="110" x2="656" y2="110" stroke="#EBEBFF" stroke-width="2" marker-end="url(#aw)"/>
  <line x1="789" y1="132" x2="789" y2="148" stroke="#EBEBFF" stroke-width="2" marker-end="url(#aw)"/>
  <line x1="789" y1="186" x2="789" y2="202" stroke="#EBEBFF" stroke-width="2" marker-end="url(#aw)"/>
  <path d="M660 236 L556 236 L556 190" fill="none" stroke="#EBEBFF" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#aw)"/>
  <text x="600" y="230" text-anchor="middle" font-size="11" fill="#EBEBFF">error técnico</text>
  <rect x="988" y="24" width="210" height="150" rx="16" fill="#FFFFFF" stroke="#280265" stroke-width="2.5"/>
  <text x="1093" y="16" text-anchor="middle" font-size="13" font-weight="700" fill="#280265" letter-spacing="1.5">EXISTENTE</text>
  <text x="1093" y="66" text-anchor="middle" font-size="21" font-weight="700" fill="#280265">Adyen</text>
  <text x="1093" y="88" text-anchor="middle" font-size="13" fill="#000000">Checkout API</text>
  <text x="1093" y="126" text-anchor="middle" font-size="12.5" fill="#000000">Ubica la tarjeta</text>
  <text x="1093" y="144" text-anchor="middle" font-size="12.5" fill="#000000">y cobra sin CVV</text>
  <rect x="988" y="194" width="210" height="120" rx="16" fill="#FFFFFF" stroke="#280265" stroke-width="2.5"/>
  <text x="1093" y="236" text-anchor="middle" font-size="21" font-weight="700" fill="#280265">SendGrid</text>
  <text x="1093" y="260" text-anchor="middle" font-size="12.5" fill="#000000">Correo con el</text>
  <text x="1093" y="278" text-anchor="middle" font-size="12.5" fill="#000000">resultado</text>
  <line x1="176" y1="100" x2="218" y2="100" stroke="#280265" stroke-width="2.5" marker-end="url(#ar)"/>
  <circle cx="197" cy="100" r="13" fill="#5300DF"/><text x="197" y="105" text-anchor="middle" font-size="13" font-weight="700" fill="#FFFFFF">1</text>
  <line x1="458" y1="110" x2="416" y2="110" stroke="#280265" stroke-width="2.5" marker-end="url(#ar)"/>
  <circle cx="437" cy="110" r="13" fill="#5300DF"/><text x="437" y="115" text-anchor="middle" font-size="13" font-weight="700" fill="#FFFFFF">2</text>
  <line x1="416" y1="228" x2="458" y2="228" stroke="#280265" stroke-width="2.5" marker-start="url(#ar)" marker-end="url(#ar)"/>
  <circle cx="437" cy="228" r="13" fill="#5300DF"/><text x="437" y="233" text-anchor="middle" font-size="13" font-weight="700" fill="#FFFFFF">3</text>
  <path d="M938 228 L963 228 L963 120 L984 120" fill="none" stroke="#280265" stroke-width="2.5" marker-end="url(#ar)"/>
  <circle cx="963" cy="168" r="13" fill="#5300DF"/><text x="963" y="173" text-anchor="middle" font-size="13" font-weight="700" fill="#FFFFFF">4</text>
  <line x1="938" y1="283" x2="984" y2="283" stroke="#280265" stroke-width="2.5" marker-end="url(#ar)"/>
  <circle cx="963" cy="258" r="13" fill="#5300DF"/><text x="963" y="263" text-anchor="middle" font-size="13" font-weight="700" fill="#FFFFFF">5</text>
</svg>"""
legend2 = f"""<div class="legend">
  <div>{NUM(1)}<span><b>Generic API reserva con pago programado:</b> deja <code>VTUB</code> y <code>VTUP</code> por pasajero, con la tarjeta en la nota de <code>VTUP</code>, y el monto de la TUA en un comentario.</span></div>
  <div>{NUM(4)}<span><b>Cobramos en Adyen:</b> el Procesador ubica la tarjeta tokenizada y cobra el total de la reserva sin CVV.</span></div>
  <div>{NUM(2)}<span><b>Identificamos:</b> un evento programado activa el Identificador, que lee en Navitaire los vuelos que tocan según el bundle (SMART 10, SWITCH 6, ZERO 1 día antes) y encola en SQS cada reserva con <code>VTUP</code>.</span></div>
  <div>{NUM(5)}<span><b>Avisamos por SendGrid:</b> el Procesador publica el aviso en una cola y una Lambda envía el correo con la plantilla de Viva, con reintentos.</span></div>
  <div>{NUM(3)}<span><b>Releemos y registramos:</b> el Procesador toma la reserva de la cola, la relee en Navitaire (tarjeta y monto) y, al cobrar, registra el pago con <code>VTUA</code>.</span></div>
</div>"""

arch = '''<svg viewBox="0 0 1200 300" width="100%" role="img" aria-label="Arquitectura AWS del servicio de pago programado">
  <defs><marker id="ar2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#280265"/></marker></defs>
  <rect x="150" y="6" width="760" height="288" rx="14" fill="#F7F6FF" stroke="#280265" stroke-width="1.5" stroke-dasharray="6 4"/>
  <text x="166" y="28" font-size="13" font-weight="700" fill="#280265">Cuenta AWS existente de Viva · VPC y subredes privadas</text>
  <rect x="4" y="60" width="128" height="56" rx="10" fill="#FFFFFF" stroke="#280265" stroke-width="2"/>
  <text x="68" y="84" text-anchor="middle" font-size="12.5" font-weight="700" fill="#280265">EventBridge</text>
  <text x="68" y="102" text-anchor="middle" font-size="12.5" font-weight="700" fill="#280265">Scheduler</text>
  <rect x="176" y="48" width="230" height="78" rx="10" fill="#280265"/>
  <text x="291" y="76" text-anchor="middle" font-size="14" font-weight="700" fill="#FFFFFF">ECS Fargate</text>
  <text x="291" y="96" text-anchor="middle" font-size="12" fill="#EBEBFF">Identificador de cobros pendientes</text>
  <text x="291" y="114" text-anchor="middle" font-size="12" fill="#EBEBFF">Procesador de cobros · conciliación</text>
  <rect x="176" y="160" width="230" height="44" rx="10" fill="#EBEBFF"/>
  <text x="291" y="187" text-anchor="middle" font-size="13" font-weight="600" fill="#280265">SQS de cobro + DLQ</text>
  <rect x="176" y="226" width="230" height="44" rx="10" fill="#EBEBFF"/>
  <text x="291" y="253" text-anchor="middle" font-size="12" font-weight="600" fill="#280265">Lambda que activa el Procesador</text>
  <rect x="440" y="48" width="200" height="44" rx="10" fill="#EBEBFF"/>
  <text x="540" y="75" text-anchor="middle" font-size="13" font-weight="600" fill="#280265">DynamoDB · estado</text>
  <rect x="440" y="104" width="200" height="44" rx="10" fill="#EBEBFF"/>
  <text x="540" y="131" text-anchor="middle" font-size="13" font-weight="600" fill="#280265">Secrets Manager · KMS</text>
  <rect x="440" y="160" width="200" height="44" rx="10" fill="#EBEBFF"/>
  <text x="540" y="187" text-anchor="middle" font-size="13" font-weight="600" fill="#280265">CloudWatch · logs y alertas</text>
  <rect x="440" y="226" width="200" height="44" rx="10" fill="#EBEBFF"/>
  <text x="540" y="253" text-anchor="middle" font-size="13" font-weight="600" fill="#280265">SQS + Lambda de notificación</text>
  <rect x="680" y="104" width="200" height="44" rx="10" fill="#EBEBFF"/>
  <text x="780" y="131" text-anchor="middle" font-size="13" font-weight="600" fill="#280265">Salida NAT</text>
  <rect x="960" y="20" width="236" height="56" rx="10" fill="#FFFFFF" stroke="#280265" stroke-width="2"/>
  <text x="1078" y="54" text-anchor="middle" font-size="14" font-weight="700" fill="#280265">Navitaire (dotREZ)</text>
  <rect x="960" y="96" width="236" height="56" rx="10" fill="#FFFFFF" stroke="#280265" stroke-width="2"/>
  <text x="1078" y="130" text-anchor="middle" font-size="14" font-weight="700" fill="#280265">Adyen Checkout API</text>
  <rect x="960" y="172" width="236" height="56" rx="10" fill="#FFFFFF" stroke="#280265" stroke-width="2"/>
  <text x="1078" y="206" text-anchor="middle" font-size="14" font-weight="700" fill="#280265">SendGrid</text>
    <line x1="132" y1="88" x2="172" y2="88" stroke="#280265" stroke-width="2" marker-end="url(#ar2)"/>
  <line x1="260" y1="130" x2="260" y2="156" stroke="#280265" stroke-width="2" marker-end="url(#ar2)"/>
  <line x1="291" y1="208" x2="291" y2="222" stroke="#280265" stroke-width="2" marker-end="url(#ar2)"/>
  <path d="M176 248 L160 248 L160 110 L172 110" fill="none" stroke="#280265" stroke-width="2" marker-end="url(#ar2)"/>
  <line x1="406" y1="70" x2="436" y2="70" stroke="#280265" stroke-width="2" marker-end="url(#ar2)"/>
  <path d="M406 98 L660 98 L660 126 L676 126" fill="none" stroke="#280265" stroke-width="2" marker-end="url(#ar2)"/>
  <line x1="880" y1="126" x2="956" y2="48" stroke="#280265" stroke-width="2" marker-end="url(#ar2)"/>
  <line x1="880" y1="126" x2="956" y2="124" stroke="#280265" stroke-width="2" marker-end="url(#ar2)"/>
  <line x1="880" y1="126" x2="956" y2="200" stroke="#280265" stroke-width="2" marker-end="url(#ar2)"/>
</svg>'''

ARCH_SLIDE_SRC = 'I.append(slide(f\'Arquitectura AWS de la {hl("solución")}\', arch + \'\'\'<div class="archnotes">\n  <div><b>1 · Descubrir.</b> EventBridge Scheduler llama al endpoint del Identificador en Fargate; este lee Navitaire, deduplica contra DynamoDB y encola en SQS.</div>\n  <div><b>2 · Cobrar.</b> Una Lambda toma cada mensaje y llama al endpoint del Procesador, como se conversó con Héctor. Alternativa más simple: que el servicio consuma SQS directamente.</div>\n  <div><b>3 · Estado y compensación.</b> DynamoDB guarda cada cobro (iniciado, autorizado, confirmado, cobrado, cancelado), los intentos y la próxima hora de reintento.</div>\n  <div><b>4 · Sin webhooks.</b> Captura y cancelación responden «received»; la conciliación diaria con el reporte de Adyen confirma el resultado. No hay ingreso público.</div>\n  <div><b>5 · Salida.</b> NAT hacia Navitaire, Adyen y el correo; si alguno exige IP fija, Viva la registra.</div>\n  <div><b>6 · Reintentos.</b> El retraso de SQS llega a 15 minutos, así que los intentos de horas se agendan en DynamoDB y los toma la siguiente corrida.</div>\n</div>\'\'\', internal=True))\n\n'

# Tablero propuesto en Datadog (esquema, valores ilustrativos)
_W = 'fill="#FFFFFF" stroke="#C7B5F7" stroke-width="1.5"'
def _box(x, y, w, h, title):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" {_W}/><text x="{x+12}" y="{y+19}" font-size="12" font-weight="600" fill="#280265">{title}</text>'
def _txt(x, y, s, size=11, fill="#282E3F", weight=400, anchor="start"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{s}</text>'
def _kpi(x, w, title, value, sub):
    return (f'<rect x="{x}" y="50" width="{w}" height="62" rx="8" {_W}/>' + _txt(x+10, 67, title, 11, "#280265", 600)
            + _txt(x+10, 93, value, 20, "#5300DF", 700) + _txt(x+10, 106, sub, 9.5))
def _bars(x0, y0, h, vals, w=13, gap=6):
    out = []
    for k, (a, b, c) in enumerate(vals):
        x = x0 + k * (w + gap); y = y0 + h
        for v, col in ((a, "#5300DF"), (b, "#22D0FF"), (c, "#C7B5F7")):
            y -= v; out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{v}" fill="{col}"/>')
    return "".join(out)
def _dot(x, y, s):
    return f'<circle cx="{x}" cy="{y-4}" r="4.5" fill="#5300DF"/>' + _txt(x+10, y, s, 10)

_kpis = [("Cobros del día", "1.248", "capturados"), ("Tasa de éxito", "96,3 %", "cobradas / procesadas"),
         ("Monto cobrado", "2,1 M MXN", "captura solicitada en Adyen"), ("Cobros sin cerrar", "3", "autorizados sin captura"),
         ("Descartadas", "11", "por motivo, sin cobro"), ("Mensajes en la DLQ", "0", "errores técnicos")]
_k = "".join(_kpi(20 + n * 194, 182, *v) for n, v in enumerate(_kpis))

_funnel = ""
_steps = [("Encoladas", "1.300", 1.0), ("Procesadas", "1.296", .997), ("Registradas", "1.251", .962), ("Cobradas", "1.248", .96)]
for n, (lab, val, r) in enumerate(_steps):
    x = 32 + n * 140; w = 122
    _funnel += f'<rect x="{x}" y="{150 + (1-r)*60:.0f}" width="{w}" height="{36}" rx="6" fill="#5300DF" opacity="{1 - n*0.15:.2f}"/>'
    _funnel += _txt(x + w/2, 172 + (1-r)*60, f"{lab} · {val}", 11, "#FFFFFF", 600, "middle")
    if n < 3:
        _funnel += f'<text x="{x + w + 9}" y="{173}" font-size="13" fill="#280265">›</text>'

dash = ('<svg viewBox="0 0 1200 468" width="100%" role="img" aria-label="Esquema del tablero propuesto en Datadog">'
  '<rect x="2" y="2" width="1196" height="464" rx="14" fill="#F7F6FF" stroke="#280265" stroke-width="2"/>'
  + _txt(20, 32, "Datadog · Pago programado de la TUA", 15, "#280265", 700)
  + '<rect x="760" y="16" width="120" height="24" rx="12" fill="#FFFFFF" stroke="#C7B5F7"/>' + _txt(820, 32, "ambiente: TEST", 11, "#280265", 400, "middle")
  + '<rect x="890" y="16" width="140" height="24" rx="12" fill="#FFFFFF" stroke="#C7B5F7"/>' + _txt(960, 32, "bundle: todos", 11, "#280265", 400, "middle")
  + '<rect x="1040" y="16" width="140" height="24" rx="12" fill="#FFFFFF" stroke="#C7B5F7"/>' + _txt(1110, 32, "escenario: todos", 11, "#280265", 400, "middle")
  + _k
  # embudo
  + _box(20, 122, 580, 108, "Embudo del día: lo encolado contra lo cobrado")
  + _funnel
  + _txt(32, 222, "Descartadas 11: pago manual previo 8 · sin monto 2 · nota inválida 1  |  No procesadas 34: rechazos 30 · canceladas 4", 9.3)
  # barras
  + _box(612, 122, 568, 108, "Cobros por hora y resultado")
  + _bars(630, 146, 64, [(30,3,2),(44,4,1),(52,3,3),(58,5,1),(46,2,2),(38,3,1),(55,4,2),(41,2,1),(33,3,1),(48,4,2),(45,3,1),(36,2,1),(28,2,0),(24,1,1),(40,3,1),(50,4,2),(54,5,2),(47,3,1),(39,2,1),(35,2,1)])
  + '<rect x="1020" y="146" width="10" height="10" fill="#5300DF"/>' + _txt(1036, 155, "capturados", 10)
  + '<rect x="1020" y="164" width="10" height="10" fill="#22D0FF"/>' + _txt(1036, 173, "rechazados", 10)
  + '<rect x="1020" y="182" width="10" height="10" fill="#C7B5F7"/>' + _txt(1036, 191, "cancelados", 10)
  # fila 3
  + _box(20, 240, 284, 96, "Identificador · última corrida")
  + _txt(32, 280, "06:00 · 4 min 12 s · 418 legs revisados") + _txt(32, 298, "Encoladas: SMART 512 · SWITCH 401 · ZERO 387") + _txt(32, 316, "Errores con Navitaire: 0")
  + _box(316, 240, 284, 96, "Cola de cobros (SQS)")
  + _txt(328, 280, "Mensajes en la cola: 4") + _txt(328, 298, "Edad del más antiguo: 2 min") + _txt(328, 316, "En la DLQ: 0")
  + _box(612, 240, 284, 96, "Integraciones · latencia p95 y errores")
  + '<polyline points="626,322 650,314 674,318 698,306 722,312 746,302 770,309 794,298 818,305 842,296 866,302 884,294" fill="none" stroke="#5300DF" stroke-width="2"/>'
  + '<polyline points="626,328 650,325 674,327 698,321 722,325 746,319 770,323 794,317 818,322 842,315 866,320 884,313" fill="none" stroke="#22D0FF" stroke-width="2"/>'
  + '<polyline points="626,316 650,318 674,312 698,315 722,309 746,313 770,306 794,311 818,304 842,309 866,302 884,306" fill="none" stroke="#280265" stroke-width="2" stroke-dasharray="4 3"/>'
  + _txt(624, 276, "Navitaire (violeta) · Adyen (azul) · SendGrid (punteada)", 10)
  + _box(908, 240, 272, 96, "Conciliación interna · cobros vs Navitaire")
  + _txt(920, 280, "Cuadran: 1.248 (con VTUA y pago)") + _txt(920, 298, "Diferencias: 0") + _txt(920, 316, "Última conciliación: 05:00")
  # fila 4
  + _box(20, 346, 284, 108, "Notificaciones · SQS, Lambda y SendGrid")
  + _txt(32, 386, "Publicados: 1.282 · enviados: 1.282") + _txt(32, 404, "Reintentos: 6") + _txt(32, 422, "Sin enviar, en su DLQ: 0")
  + _box(316, 346, 284, 108, "Tarjetas de un solo uso (escenario 1)")
  + _txt(328, 386, "Borradas en Adyen: 311") + _txt(328, 404, "Fallas al borrar: 0") + _txt(328, 422, "Sin datos de tarjeta: solo tokens")
  + _box(612, 346, 568, 108, "Monitores")
  + _dot(626, 386, "Identificador no corrió") + _dot(810, 386, "Nota, tarjeta o monto inválidos") + _dot(1000, 386, "Cola atascada")
  + _dot(626, 406, "Mensajes en la DLQ") + _dot(810, 406, "Cobros sin cerrar") + _dot(1000, 406, "Diferencias internas")
  + _dot(626, 426, "Errores de Navitaire o Adyen") + _dot(810, 426, "Rechazos fuera de lo normal") + _dot(1000, 426, "Correos sin enviar")
  + _dot(626, 446, "Falla al borrar tarjeta")
  + '</svg>')
