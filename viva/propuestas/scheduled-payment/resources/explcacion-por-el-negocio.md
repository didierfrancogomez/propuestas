Didier Fabian Franco Gomez  0:03
a lo particular, empezando por lo que estás buscando como tal en el alcance del proyecto.

Hector Eduardo Rodriguez Cervantes  0:09
Sí, digo, ahí digo, este es un proyecto estratégico KPI. Aquí le llamamos. Actualmente, el objetivo principal es que el usuario desde el frontend.
Cuando genera una reserva.
Le vamos a mostrar una nueva opción que dice que pueda programar el pago de su TUA. ¿Saben acá el TUA es un impuesto que se cobra del uso del aeropuerto, no? Pues en todos los aeropuertos de la República. Hoy en día ya existe que tú puedas pagar la TUA después, o sea, tú puedes generar tu reserva.
Y le puedes decir pagar después y x días antes. No recuerdo los días exactos, pero son configurables, pues tú puedes pagar la tuba manualmente antes de la salida del vuelo. Es decir, si yo compro un vuelo hoy para salir el 24 de diciembre, quizá el 15 de diciembre yo puedo entrar a mi reserva y pagar.
Pues el TUA que en ese momento corresponda. Algo importante aquí es que el TUA al ser un impuesto puede cambiar, es raro, pero cambia, ¿no? Entonces normalmente en el flujo productivo ese valor se calcula desde el backend que usa el canal web y la app, ¿no?
Para el flujo del pago programado, que es el que les compartí, el TUA no va a cambiar, es decir, cuando tú selecciones quiero pagar mi TUA programada. ¿Qué significa programada para nosotros? Es que se va a hacer un cobro domiciliado, le llamamos también acá o automático, no.
Ese cobro es sin el uso del CBV, no, porque hoy en día en el flujo que le que tenemos, pues el usuario sí ingresa al sitio a la aplicación, selecciona que va a pagar la tua y captura sus datos de pago, no incluyendo el CBV, no. Esta vez, pues en este nuevo flujo el proceso de pago es.
Pues automático y por ende tiene que estar tokenizada la tarjeta para poder y autorizada por el cliente para poder ser procesado, no básicamente esa es la intención. Digo hablando un poquito desde la experiencia de usuario, de qué va a depender el.
El pago programado, la fecha, ahí los de producto pues se pusieron, nos nos la pusieron un poquito más compleja de lo esperado, la verdad, porque en un principio yo proponía que el usuario seleccione su fecha. En lo personal creo que es más amigable que el usuario decida.
Pues sabiendo qué tarjeta es la que va a domiciliar y en qué fecha, pues se espera que le haga el cobro, ¿no? ¿Cómo se va a manejar esto? La regla es que va a depender del bundle. En este caso, como saben, tenemos 3 bundles, el cero, el switch y el smart. Si es cero, el cobro se hace 6 días antes.
Perdón, si es cero se cobra un día antes, si es switch 6 días antes, si es smart son 10 días antes, no el por qué se definió así, les mentiría. O sea, no sé la lógica de negocio de por qué 1101C es 111 o el beneficio de pues lo desconozco, pero bueno, fue la regla que nos marcaron.
Y es por eso que ustedes verán en el documento que se habla de ir al manifiesto de Naviter, entrando un poquito ya a la capa intermedia, donde pues vamos, estamos pensando en ir a recuperar fechas hacia adelante. justamente el.
No tanto por el fondo, o sea, sí es una validación que hay que hacer, por supuesto, pero sí ir por el target de las fechas donde vamos a estar procesando los pagos, ¿no? Ahora, como nosotros ya estamos trabajando con los ingenieros del backend, la primera parte, ¿cuál es la primera parte?
El flujo del pago, es decir, cuando el usuario selecciona pago programado de la TUA, nosotros vamos a guardar en Nabiter una bandera, por decirlo así, en un nuevo SSAR dentro de Nabiter. Ese nuevo SSAR va a ser un SSAR que justo nos va a servir para nosotros poder filtrar las reservas. que.
Pues tienen el pago programado, ¿no? Hoy en día tenemos 2 SCS ya para la TUA, uno es el VTUV, el VTUV de bueno.
Ese justo es el que se inserta en la reserva cuando el cliente selecciona pagar después. ¿Cómo se elimina cuando el usuario paga en el sitio el servicio del generic o el backend de la web? Lo que hace es borrar el SS SAR. y.
Agrega un free para balancear la reserva en la sección de Naviter. No sé si a ver si les puedo mostrar. ¿Han visto el de Skyspeed en Naviter?
O cómo se mira.
No, okay, déjenme, déjenme les muestro para compartir mi pantalla.

Didier Fabian Franco Gomez  5:23
Oh.

Hector Eduardo Rodriguez Cervantes  5:33
Ahí se se mira.

Didier Fabian Franco Gomez  5:38
Yeah, that.

Jonh Freddy Osses Castro  5:40
Ok.

Hector Eduardo Rodriguez Cervantes  5:41
O K, a ver, déjenme a ver si puedo abrir una de las reservas que generé ayer.
Este es Naviter, sale entonces para yo, por ejemplo, ayer generé varias reservas de prueba, no recuerdo si pagué el TUA, pero ahorita checamos.
Por ejemplo, bueno, pues producciones acá más bien.
Tengo varias, vamos a ver esta última.
Esta reserva, por ejemplo, tiene PTUA. Este son los CCSARS. PTUA significa que si yo voy K.
Significa que ya pagué el TUA. De hecho, aquí aparece el monto que yo pagué de esa TUA. Cuando no está pagada, esto no aparece. Esto aquí no hay registro o una entrada de dinero a nivel del sistema y lo que va a aparecer es acá en los SSARS.
Por pasajero, uno que va a decir BTUYB de bueno de tu sale. ¿Por qué? Porque finalmente el TUA es por pasajero, eso es algo importante, ¿no? El TUA no es por reserva, es a nivel de pasajero, pues porque es un impuesto por pasajero, ¿no? Entonces, ¿qué pasa cuando tú pagas la reserva?
Se elimina el ve tu y se agrega el ve tu a esta, como les digo, ya está apagada, ¿no? Este qué vamos a hacer nosotros nosotros en el SSAR, a ver si por aquí puedo mostrarlo.
Tiene una notita, esto a nivel de servicios de Navita en el Swagger van a poder ver que hay un campo que se llama SSAR Note, se llama Note dentro de Navita. Si yo voy, déjame ver si puedo consultar una SSAR.
Fíjense, aquí dice ese SAR note, digo, este no tiene ahorita una nota, pero yo aquí podría poner una nota que va a tener la nota. Me voy a adelantar un poquito cuando nosotros generemos la reserva en el backend, aquí vamos a agregar una nota con el basket ID.
O el customer number.
¿Y vamos a concatenar también es una o es otra, sale? Ahorita les voy a explicar por qué y vamos a concatenar un dato que se llama First.
First, reverse.
Este Esto va a ser lo que nosotros vamos a guardar en el nuevo SSAR del pago programado. ¿O K por qué? Y ahí déjame ver si tengo aquí el diagrama. De hecho, debe venir en los que les pasé.
En el de Generic, que esa parte estamos controlando.

Didier Fabian Franco Gomez  8:39
Yo lo Yo lo vi y tengo una duda puntualmente con eso, porque ahí no estamos identificando como otra banderita el como el escenario por el que se va. Si es una tarjeta que ya está registrada, si es una tarjeta que no se quiere registrar, porque hay un hay un escenario.

Hector Eduardo Rodriguez Cervantes  8:43
It's.

Didier Fabian Franco Gomez  8:58
En el que con la forma en que quieren identificarlo con el slash, podríamos borrarle la tarjeta al usuario si la tenía guardada.
Entonces, si mandáramos la banderita de una vez, no nos llegaría a pasar eso, cierto, solo sería que le pusieras ese uno al inicio slash y ya el resto, cierto.

Hector Eduardo Rodriguez Cervantes  9:19
Sí, ahí algo importante es que la tarjeta como tal, a ver si aquí lo tenemos, sí.
Se le.
Aquí hay 3 escenarios, como puedes y ahorita te te respondo en el medio, Didier.
En el frontend, cuando hace el pago, nosotros vamos a mandar una nueva bandera que es esta.
Esto ya lo estamos construyendo, que es le estamos diciendo al BAC que el pago es programado, ¿no?
¿Qué vamos a hacer? El Los pagos hoy en día se procesan entre Naviter y Adyen Adyen es un procesador de pagos que realmente se conecta pues a la red de Mastercard, de Visa, a los adquirientes, no, este realmente es el que procesa el pago. Vale, lo que llaman en otros lados es la pasarela de pagos.
¿Entonces, qué ocurre cuando nosotros bandereamos un pago? En este caso, el primer escenario es una nueva tarjeta y el usuario en el frontend decide no guardar ese esa tarjeta para más adelante. ¿Qué ocurre aquí cuando tú?
Hoy en día en producción nosotros podemos guardar tarjetas, o sea, es un flujo que ya existe. Yo hoy en día, por ejemplo, con mi cuenta, déjenme ver si puedo lanzar aquí.
No probita.
Un poquito lento.
Aquí fíjense, yo hice un login, no aquí yo me logueé.
Con.
Mi cuenta de Viva, esto es test, por supuesto que hice un login y yo a esta en mi cuenta de Viva de test tengo ya tarjetas guardadas, por ejemplo, déjenme ver aquí.
Hoy creo que no la no la agregué, pero si no.
¿Te la la mandamos a llamar, cómo ver si me.
I'll take care.
Sí, aquí está. Estas son las tarjetas guardadas que yo tengo en mi cuenta de Viva, es decir, si yo en la aplicación web me logueo.
Yo cuando llega el momento de pagar una reserva, el front me va a dar un drop down list donde voy a ver todas estas tarjetas. Vale, entonces son las tarjetas guardadas de mi cuenta. ¿Vale, entonces qué ocurre?
En el flujo, el escenario uno.
El usuario decide no guardar su tarjeta. Eso significa que en el servicio que les acabo de mostrar no va a existir un registro de esa tarjeta, va a ser de un solo uso. ¿Qué significa eso? Que yo voy a domiciliar ese pago de esa tua por única vez, es decir.
¿Cómo voy a ligar yo esa tarjeta de un solo uso mediante el basket ID? El basket ID es un identificador que se genera durante el booking flow le llamamos durante la creación de la reserva. Es por eso que acá fíjense cuando se manda el pago desde el backend and habiter.
Naviter va a Adyen y Adyen es quien tiene la bóveda o el vault de tener las tarjetas guardadas. Sale, pero aquí en este flujo, este es el más complejo porque el cliente solo va a usar esa tarjeta por única vez para domiciliar una sola vez. Si accede una segunda vez al flujo, pues esa tarjeta no la va a ver en su cuenta guardada.
Nunca, porque es de un solo uso, vale, pero qué pasa nosotros aquí desde el backend vamos a invocar Edgent y justo lo que vamos a hacer este servicio lo que hace es ir a la bóveda y decir, bueno, pues yo en tu bóveda te mandé una tarjeta que necesito que toque nice, ya está tokenizada.
Dámela, dame, dame la información de esa tarjeta, ¿no? ¿Qué va a ocurrir aquí? Nosotros como tal, en un principio habíamos pensado en guardar el token en Naviter, pero eso es inseguro entre un tema de PCI. Entonces decidimos solamente guardar para este escenario en el SSR Note.
Que es el que les mostraba acá acá.
Les digo, esto es un campo en el swagger de Naviter, viene como es Sernout. Aquí van a ver esto. Entonces, vía servicio, ustedes van a poder recuperar estos valores. ¿Estos valores para qué sirven? Esos valores sirven porque.
Ya déjame ver si tengo estos son los request de Alien. Esto es directamente la documentación o bueno, la documentación es algo que yo extraje de la documentación de Alien, pero es importante que la conozcan porque el batch, que es la parte que ustedes van a desarrollar, va a usar una conexión directa con Alien. Sale entonces.
Por ejemplo, aquí esta este paso uno no les toca a ustedes porque en realidad el pago ocurre en línea en el sitio. Entonces este request, pues digamos que lo hacemos nosotros, no desde nuestro backend. Pero fíjense, la salida me da, pues aquí ciertos datos, no ahora.
Cuando yo quiero en este llamado que se miraba.
Aquí este es un get. Bueno, aquí viene como un post, pero en realidad es un get de tras bambalinas. ¿Qué voy a qué ocurre acá? Cuando yo hago un llamado a ese servicio, list recuring details, obtengo toda esta data.
Esta data corresponde.
Oh.
La tarjeta tokenizada, si se dan cuenta aquí en el request, fíjense el request que alguien espera.
Aparte que pues estos datos que son fijos, el contract y el merchant account, el más importante es este que dice shopper reference. Este shopper reference es el dato maestro, por decirlo así, porque este es un ID único nosotros para obtener las tarjetas guardadas que le mostraba que les mostraba aquí en mi ejemplo.
Lo que hace el backend es mandarle el customer number de Héctor. Héctor tiene un customer number o mi cuenta tiene un customer number asignado y es un valor único ese dato. Entonces yo a alguien le mando el customer number que de hecho es parte de cuando mando guardar la tarjeta.
Y me va a decir, bueno, este cliente con este ID tiene todas estas tarjetas guardadas. Sale, ¿qué va a pasar cuando no tengamos customer number? Le vamos a mandar el basket. ¿Sale? ¿Por qué? Porque el usuario decidió no guardar su tarjeta. Entonces no la no se la puedo ligar a su customer number porque él no aceptó eso.
Él aceptó solamente usarlo una vez. Entonces, como es de un solo uso, el de identificador va a ser el basket ID. Sale cómo el batch va a obtener el token para procesar el pago. Es el siguiente pasito que les voy a mostrar acá, que ya la ejecución del pago sin el CBB.
Ustedes necesitan en el batch este dato, el PSP reference con este dato, cuando ustedes manden el basket ID en el escenario uno, el escenario 2 y el 3 ahorita se los cuento, pero en el escenario uno mandan el basket ID en este parámetro.
Y ustedes van a poder recuperar el token, el token de esta respuesta es este que dice este campo es el token.
Y ese es el que ustedes van a usar después para procesar el pago y ya que se apruebe, entonces van y escriben en Abiter el resultado. Sale, entonces este es el token. Tú para obtener el en el primer escenario, la ventaja que se tiene es que solo van a solo van a recibir una, solo van a obtener en la res.
Apuesta de este servicio una sola tarjeta, porque para este básquet siempre va a haber solamente una tarjeta, no va, no va a haber en ningún escenario donde este básquet ahí te devuelva 2 tarjetas guardadas. Eso no se puede dar, sale entonces aquí no hay falle porque.
Pues básicamente el dato que obtengan aquí es el que van a usar para después mandar el pago. Se dan cuenta aquí en el pago viene este campo que dice select recuring detail reference, que es el token, este es el token y aquí en el para hacer el pago es el que le van a mandar.
¿Sale de dónde van a obtener el monto a pagar? Aquí este mail lo van a obtener de un comentario que existe también en Habitar.
Sale, entonces, en resumen, del S StarNote van a obtener la los datos para poder hacer esta consulta, es decir, obtener la tarjeta tokenizada y de Eraviter hay un campo que en los comentarios que se llama ahorita en esa reserva no viene porque chances sí.
Déjame ver si puedo mostrarles alguna de estas.
Es viejita, pero chance puedo consultar.
Igual quien están bastantes familiarizados con estos servicios de Navitar, también este pues los chicos que trabajan con nosotros de con ISI.
Ellos conocen muy bien estos servicios, prácticamente nos ayudan con todos y te canso Luis, Daniel. este.

Didier Fabian Franco Gomez  19:17
Sí.

Jonh Freddy Osses Castro  19:19
Different factor.

Hector Eduardo Rodriguez Cervantes  19:19
¿Este ahorita dame chance, no?
Vamos a sacar con otro resto.

Jonh Freddy Osses Castro  19:33
Yo tengo una pregunta con esa transacción y es siempre entonces se conoce cuánto tiempo irían guarda en su bóveda estas tarjetas, pues nuevas. Pero digo es porque se puede dar el primer pago y si es, por ejemplo, un una reserva de mucho tiempo y tal vez el plan es cero.
Que es de un día antes de pues como el vuelo, que es lo que lo que no entiendo, pues puede pasar un buen lapso ahí en ese espacio, pues de tiempo. Entonces no sé si se tiene de pronto documentación sobre y en cuánto tiempo lo guarda en su bóveda al ser una tarjeta, pues que no tiene un costumbre ID, sino que es básicamente nueva.

Hector Eduardo Rodriguez Cervantes  20:18
Mhm.

Jonh Freddy Osses Castro  20:19
Borres en.

Hector Eduardo Rodriguez Cervantes  20:19
Mhm.
Sí, creo que te digo, tengo que confirmar el dato, pero sí es largo el tiempo. O sea, sí da el margen para procesar, porque incluso los vuelos creo que lo que vendemos son a máximo 6 7 meses hasta 8 si no me equivoco, y es mayor a eso. O sea, no habría ahí un tema.

Jonh Freddy Osses Castro  20:35
Okay.
Ok, listo, súper.

Hector Eduardo Rodriguez Cervantes  20:41
Salvo que manualmente, que también existe la forma, nosotros mandemos borrarla.

Jonh Freddy Osses Castro  20:48
Sí, claro, sí, seguramente una política de retención de datos. Supongo yo que también se puede solicitar una eliminación de eso. Entonces eso también de pronto.

Hector Eduardo Rodriguez Cervantes  20:49
Dale este.
Sí, correcto.

Jonh Freddy Osses Castro  20:59
Y.

Hector Eduardo Rodriguez Cervantes  21:18
Bueno, es que aquí ya está pagada. Entonces no necesito una que no esté pagada. Lástima, hay un este es un servicio de Naviter.
Retrieve para el bricolocator, donde nosotros le pasamos el pnry ahí hay un objeto que se llama comments. Este digo, este no es ahorita, desafortunadamente esta reserva tiene la tuba apagada, pero aquí en este arreglito viene un arreglo donde viene el comentario.
De la tua que se persistió en ese momento. Entonces esa no va a cambiar, es un dato fijo. Entonces de ahí es donde hay que leer el monto que hay que mandar en el Ricoes que les mostraba acá, que este es el Ricoes del pago, no el que ya transacciona y el que ya pues le debita al cliente el saldo no correspondiente.
Este Estos parámetros son importantes, como los pongo aquí, igual creo que le serviría este flujito que tengo aquí del request y el response es el Happy Path, porque pues es prácticamente como hay que ustedes prácticamente harán uso de este servicio para obtener la tarjeta tokenizada. Ay, perdón por ser repetitivo y el paso 3, pues pagarlo, ¿no?
Y sería un armado como este, sale incluso aquí les pongo también la tablita de donde sale cada dato, ¿no?

Jonh Freddy Osses Castro  22:32
That.

Hector Eduardo Rodriguez Cervantes  22:41
Entonces, en resumen, son 2 momentos. Déjame en el escenario 2 y el 3 son más sencillos, porque en el 2, pues básicamente el usuario sí chequea en el front, digo, está muy lenta mi compu, pero en el front literal hay un checkbox que le dice guardar tarjeta y eso le estás diciendo al sistema.
¿Que quieres que esa tarjeta te la guarde ligada a tu cuenta y tu customer ID y entonces en futuros pagos la puedas usar para que se tokenencia tiene que ser un pago exitoso, no? O sea, quizá yo hoy capturo una nueva tarjeta, un American Express, le digo que sí quiero guardar mi tarjeta, se crea la reserva y si yo chequee esa opción.
Ya en mi segunda compra ya voy a ver esa tarjeta disponible como guardada, ¿no? Y ya nada más me va a pedir el CBV porque eso es, digamos, si es parte de lo que hoy en día existe, ¿no? Y el siguiente escenario pues es el store aquí. Bueno, básicamente se repite. La diferencia es que en lugar de guardar el basket ID, digo este creo.
Que no lo tengo actualizado, pero en el que les pase sí es customer ID Pipe First PSP Referent, porque aquí sí este valor hace mucho, muchísimo más sentido en el escenario 2 y 3, porque si vamos a la respuesta que les mostraba de la tarjeta guardada.
Van a virar que yo tengo muchas tarjetas.
Entonces.
Aquí.
Fíjense, yo tengo una aquí por el key, es única, 1234 tarjetas. ¿Cómo van a saber ustedes qué tarjeta es la que es la que yo decidí usar para programar el pago? Lo van a hacer mediante este dato.
Aquí cuando invoquen.
El este servicio.
Aquí ustedes ya van a traer de Nabiter.
Este valor que es el que yo les voy a alojar en Nabiter. Entonces van a decir, bueno, ese que viene en el SSarenote búscalo en la respuesta aquí y esa es la tarjeta que tengo que utilizar. Entonces de ahí sacas el token. Este es el uso real de este campo, o sea, por eso en el SSarenote van a tener el customer.
Porque es el que ocupan para mandar en el request, en el shopper reference y van a ocupar el PSP reference para poder identificar qué tarjeta utilizar. Como les decía, en el escenario uno no hay tanto rollo porque siempre va a haber una tarjeta, pero en el escenario 2 y 3 que ya es una tarjeta guardada y posiblemente ese customer ID tiene muchas tarjetas tokenizadas.
Ustedes tienen que saber cuál van a mandar al pago, sale. Es por eso que el valor a utilizar.
Aquí pues lo van a sacar de aquí, entonces básicamente ustedes les va a servir el del lado izquierdo para la petición en el shopper reference y el segundo para identificarle la respuesta a la tarjeta a utilizar.
Vale, entonces este es como, digamos, el flujo que ya estamos desarrollando. este De hecho, lo está trabajando un chico de Tecansol, Luis Llano, él está trabajando el ya este ticket de del flujo que viene aquí, el que le estoy presentando el de acá.
Este este ya lo está trabajando en un ticket este Daniel este y la segunda parte, pues justo es la complementaria, que es el batch, no que el batch es este.
Obtener en pocas palabras las reservas. ¿Cómo van a obtener ese listado por el SSAR? El SSAR, les digo, va a ser un SSAR propio de este proceso que le pusimos para seguir el estándar así de tu.
Porque la el que existe es B tu a no, perdón, BTUBY el otro es BTUI porque es para internacionales. El impuesto cambia cuando es internacional, pero para el programado va a ser este.
Y.
Déjame checar si lo tenemos por acá.
Because I see.
La actualizado, pero.
Creo que sí lo tenemos por aquí. Exacto, aquí hay un en este endpoint de este.
De Naviter viene, ustedes pueden obtener por SSAR el las bookings que cumplen los criterios. Entonces aquí cuando el SSAR sea igual a ponerle ahorita nada más por aquí a la B de programado, por eso es la P de.
Programado significa que esa reserva pues tiene pendiente este el pago y que pues cumple los criterios para ser procesada. Sale cuando algo importante postpago es que este se tiene que quitar de la reserva.
Y se tiene que agregar el que les mostraba hace un momento, que es el del Betua.
Acá.
Todo hago ahí, digo, es más como teórico, un necesar teóricamente no tiene costo. Cuando tiene costo se le se le liga en Naviter, es más como de Naviter esta este este que les platico, se le liga un ficode por eso.
No sé, o sea, yo digo vetua, el SSAR es el vetua, pero ese SAR tiene ligado un FICODE, porque ese ficode se vuelve como el registro físico contable del lado de Naviter y del para toda la parte este financiera. Este representa ya el pago, ¿no? entonces?
Como tal, el SSAR no tiene un precio, pero tiene ligado un fee code, que es el interés o el código de interés, por decirlo así, una traducción más literal, pero ese es el que ya te te representa un pago, ¿no? Y es por eso que cuando tú proceses el pago con alguien, como les explicaba, pues hay que retirarle el SSAR.
Vino de un pago post booking manual. O que si lo pagó directamente, cuando creo la reserva.
A grandes rasgos el el proyecto.

Didier Fabian Franco Gomez  29:27
Rofer.

Jonh Freddy Osses Castro  29:28
Y.

Hector Eduardo Rodriguez Cervantes  29:29
Algo importante y Alex me me lo recalco bastante.
Es que digo, esta es la idea principal, como siempre sujeta a a propuestas, mejoras, si por ahí ustedes identifican algo que se puede mejorar para eficientar el proceso, en la lógica inclusive de de obtención. Le dimos varias vueltas, es la realidad, pero algo muy importante es que nosotros vemos en nuestra cabeza 2 batch por eso aquí, dice Batch uno y batch 2.
Porque en realidad, cuando tú obtienes el universo de reservas que cumplen los criterios, lo vas a mandar a una Q.
Y el el segundo batch en realidad es el que va a ser la operación del del pago. Es lo que les explicaba de ir a bueno, ya está en la cola.
Entonces ese sí ya cumplió.
Estoy seguro que ya cumplió todas las condiciones porque ya lo encolé.
¿Entonces, ese segundo proceso va y toma, le saco la el la reserva le le sacan el s saur note y ocupan esa data para para pagar, no?
Y luego, pues, regresan a a persistir.
¿El resultado del pago?
No, que también puede ser por ahí negativo.
Verán, hay un escenario de reintentos son 3.
En el tercero, pues hay que sacarlo de la cola este ese.
Esa reserva y el usuario tendría que pagar manualmente.
Hay una integración también por ahí que que ya hemos usado en Generic es el proveedor de email para que, por cada intento de pago, pues se le notifique, pues el resultado no, y mantener al cliente de Oye, ya se intentó hacer el primer cargo. Sí pasó quédate tranquilo o no pasó, pues va a haber 1 segundo intento, no.
Ahí va a haber términos y condiciones, etcétera, no para para todo esto, para toda esta parte.

Jonh Freddy Osses Castro  31:12
Pero.
Una pregunta, ahí sí.
Finalmente, después de esos 3 reintentos que se hacen, no se logra realizar el pago y el cliente no lo hace manual.
¿Se cancelaría, por ejemplo el vuelo o o qué implicaciones tendría que cancelar o KY ya el tema de retorno?

Hector Eduardo Rodriguez Cervantes  31:31
Sí.

Jonh Freddy Osses Castro  31:36
El retorno del dinero pongo que hay una multa, pero no sé si hay un proceso de retorno de dinero o se pierde completamente, por ejemplo, el el dinero de la reserva. Pues que se hizo en su momento. O no sé si tenga un escenario para eso.

Hector Eduardo Rodriguez Cervantes  31:49
Sí, sí hay, te, mentiría.
Honestamente, sé que se cancela.
No sé exactamente si en ese escenario de que no pagó la, pues, manualmente o programada, o post booking, como como decida si hay un un reembolso parcial o algún algo en viva cash por ahí, porque pues pago una parte. Es verdad. ¿Es posible que sí, EH?
Pero el escenario, la verdad, desconozco hoy en día, pero sí sé que existen procesos de cancelación.
Opciones no este en este escenario.
No, no sé si se le reembolse cuando no paga la tua.

Jonh Freddy Osses Castro  32:26
Perfecto, listo. Voy a tenerlo ahí presente.

Hector Eduardo Rodriguez Cervantes  32:29
Sí.

Jonh Freddy Osses Castro  32:29
Para evaluar.
¿Listo?

Didier Fabian Franco Gomez  32:34
¿Ahí se habla de un boom del cero, cierto?
¿Entonces, me imagino que en la forma que vamos a programar estos badges tiene que tener una una recurrencia lo suficientemente alta como para que en un día, si se puedan validar los 3 intentos, cierto?

Hector Eduardo Rodriguez Cervantes  32:54
Sí, correcto, sí, sí, sí.

Didier Fabian Franco Gomez  32:55
Y ahí me imagino que, como quieren en el portal administrativo, poder customizar esas esas acciones.

Hector Eduardo Rodriguez Cervantes  32:56
Sí.

Didier Fabian Franco Gomez  33:02
Tocaría tener alguna restricción de cara a los horarios programados, de que en que se ejecuta el batch, como lo mismo que vas a tener.
¿O van a ser hasta 3, pero no menos de eso, porque el batching igual ya no daría por los horarios en que se programó cierto?
¿O algo así?

Hector Eduardo Rodriguez Cervantes  33:18
Claro, sí, sí, sí, así tal cual para el cero. Digamos que sí existe, habrá que considerar esa esa variable.
Creo que no. No tiene documentada, pero sí justo.
O sea, hay que considerar ahí que en en ese cero posiblemente solamente déjenme confirmar ese dato nada más. A ver si le hacemos los 3 intentos el mismo día o si sólo sería un intento de pago. No solo lo confirmo yo con producto.

Didier Fabian Franco Gomez  33:46
¿YY tengo una pregunta esa, ese cobro solo se hace una vez por piquete? Comprado así sea, ida y vuelta, o eso se tiene que procesar para el de IDA y se tiene que procesar para el de vuelta.

Hector Eduardo Rodriguez Cervantes  34:03
Ahí es completo, o sea, para ida y vuelta, no, o sea porque la reserva como tal tiene ligada, depende, no, o sea, si el usuario compró un vuelo sencillo.
Este, pues, es solo ida en ese caso, pues se le cobra el como le decía la la tú en realidad es por pasajero, más que por por el vuelo, no como tal.

Didier Fabian Franco Gomez  34:22
Sí.

Hector Eduardo Rodriguez Cervantes  34:24
Entonces, el pasajero tiene que pagar el impuesto de los aeropuertos que implica ese viaje ligado a esa reserva, y la reserva puede tener multidestino, que es por ejemplo.
Este a lo mejor vuelo, no sé hablando aquí de Estado de la República mexicana, Vuelo de México a Monterrey.
Y a lo mejor mi vuelta es de Guadalajara a México no, ya no salí del mismo aeropuerto, es redondo, pues son los mismos aeropuertos, pero lo que quiero decirles con eso es que.
La el pago siempre va a ser por los vuelos que tiene ese esa reserva por la que se pagó y los pasajeros que incluyen no, entonces no vamos a separar de ya te cobro la tua del deida y en otro momento el de vuelta, no.
¿Siempre va a ser full, sobre sobre todo lo que tenga comprado, no?

Didier Fabian Franco Gomez  35:12
Súper sup.
Listo y cómo y cómo se trabajaría aquí de pronto una cancelación.
De de o sea, vamos a vamos a soportar que se cancele el el cobro automático o netamente. Si se programó ya se va así, eso no se va a modificar después.

Hector Eduardo Rodriguez Cervantes  35:35
¿Ahí lo que puede ocurrir y ver si entendí la pregunta es por ejemplo, si yo compro una reserva el 25 de diciembre, selecciono pago programado?

Didier Fabian Franco Gomez  35:44
Es.

Hector Eduardo Rodriguez Cervantes  35:45
Con smart. No. Entonces mi mi, en teoría a mí me va a cobrar el automático el 10, el 15 de diciembre, mi fecha de salida de vuelo es el 25 de diciembre y mi fecha de cobro va a ser el 15 porque escogí smart, no que es como el escenario más sencillo, creo yo este.
Si yo decido pagar la reserva el 30 de noviembre manualmente.
¿Eh?
El proceso actual de gennellic, lo que va a hacer es retirarle el cesar o va a retirar el SCR de programado y el cesar de de Tube.
Y va a ponerle la el pago, le va a imputar el pago del B two a que les explicaba hace un momento. Entonces, cuando para ese momento, cuando tú intentes leerlo o recuperarlo mediante el Sad ya no lo vas a encontrar porque ya.
Previamente es el minuto. Entonces posiblemente ni te enteres ya de que ese.
Esa reserva, pues la tienes que procesar porque ya no ya no la vas a encontrar por porque el cesar ya no va a existir.

Didier Fabian Franco Gomez  36:51
Claro. Entiendo y digamos que cuando se intentan los pagos.
Y por algún motivo, digamos, no se logra definitivamente hacer el cobro.
Cierto puede ser que Ponte que es muy usual, o al menos yo lo uso con ese New Bank que yo creo. Tarjetas virtuales temporales.
Yo les pongo una expiración de 24 horas.
Entonces yo podría utilizar eso, hacer la reserva acá y eso está por allá para dentro de 3 meses y de aquí a esa tarjeta no existe, eso no es no, no es posible.
¿Iglesia, ese escenario ahí cómo se comportaría?

Hector Eduardo Rodriguez Cervantes  37:25
Ahí lo que va a pasar es que sí se va a mandar a Tokenizar tu tarjeta.
O sea, tu tarjeta que tú creaste. Temporal de 24 horas, pues el sistema no va a saber que que está, que es una temporal.
¿Entonces él lo va a tomar como una tarjeta definitiva, te la va a guardar? Sí, si el resultado es positivo y transacciona y es aprobado tu pago, sí lo va a guardar en la bóveda.
Como una tarjeta tokenizada.
¿El tema qué va a pasar? Que cuando tú vayas a la bóveda a recuperar esa tarjeta tokenizada.
¿Pues le vas a intentar hacer el pago, no?
Pero ahí lo que ya va a pasar es que el procesador pues te la va a rechazar, no digamos que adgen dentro de su implementación y pues todo la.
Toda la las funcionalidades que tiene cuando vaya a procesar, que en este caso con ubank, que no sé si sea Mastercard o Visa, este va al adquiriente bueno a la red de pagos y pues es nubanco, Mastercard, Visa. ¿Le va a decir, sabes que esta tarjeta?
¿Pues ya, pues ya ya no es válida, no te la va a rechazar el pago?
¿Ahí el escenario, lo que va a ocurrir, pues es que en los 3 intentos va a ser vacilarse y en el tercero, pues ya lo vas a tener que mandar correo de que haga el pago manual el usuario, no?
Porque pues los 3 intentos van a fallar.

Didier Fabian Franco Gomez  38:44
YY en el sistema no marcamos nada más, o sea, como de la tarjeta, ya no es válida, o sea, no hacemos nada de eso, simplemente notificamos y ya.

Hector Eduardo Rodriguez Cervantes  38:49
Sí, no, hombre.
Exacto accidente. Solo te va a decir si es aprobado o declinado y ya.
No, no te dice. Más información del motivo.
A lo mejor creo que sí hay un campo que te dice no sé, saldo insuficiente, pero para nosotros, pues digamos que ese es indistinto.
Es aprobado, rechazado, no, normalmente no le decimos al cliente el motivo de rechazo.
Igual por temas como de seguridad y experiencia al cliente. Como no, no se le suele decir el motivo de fallo.

Didier Fabian Franco Gomez  39:16
Sí.
Claro, y los templates de esas notificaciones los diseñaría alguien de viva nosotros solo lo reutilizaríamos.

Hector Eduardo Rodriguez Cervantes  39:26
Sí, exacto sí. Ahí, qué bueno que me lo dices. De hecho, sí es un punto muy bueno. Ahí me van a pasar a mí un ID de template que ustedes van a mandar en el request, y ahí, pues con ese se arma todo el HTML.

Didier Fabian Franco Gomez  39:34
Ah, bueno.
Y.
Nosotros tenemos acceso a ese a ese template para ver qué parámetros hay que enviarle para hacer pruebas y eso.

Hector Eduardo Rodriguez Cervantes  39:46
Sí, deberían, sí, sí.
De hecho, me parece que ya tenemos integraciones ahí en otros servicios.
Igual de Tecansol Transactions, creo con Félix o sea sí en respuesta, sí nada más. Lo que sí me falta no me lo han dado, es el template.
O sea, yo creo que ahorita ocuparíamos uno dummi si se arranca el desarrollo que agarraremos un cascaroncito y este porque ese me lo tiene que definir a mi marketing.
Ya saben, todo el el, pues el tema de copy la comunicación al usuario, etcétera.

Didier Fabian Franco Gomez  40:19
¿Listo está bien y yo había visto, pues yo yo estaba analizando como la documentación y vi que ahí estamos colocándonos servicios de aiden, cierto?

Hector Eduardo Rodriguez Cervantes  40:28
Sí.

Didier Fabian Franco Gomez  40:29
Pero estaba analizando cómo la, pues por analizando.
Yo me refiero a que sea una I a para que fuera y leyera todo el contrato que ofrece eiden, pero me marcó que un par de esos servicios ya decía que.

Hector Eduardo Rodriguez Cervantes  40:36
Ajá.
Sí.

Didier Fabian Franco Gomez  40:41
Que ya están inactivos y que no están soportados y que se recomienda pasarse a otros.

Hector Eduardo Rodriguez Cervantes  40:47
No, miren, hay muy buen punto, digo, lo que pasa es que generic yo, yo ahorita como lo generé generic ya usa una endpoint y usa la versión de autorize, que es donde es el pago, pero sí en efecto el a B 72 si no me equivoco, que ya es un endpoint que se llama payments.

Didier Fabian Franco Gomez  40:48
¿Eh?
Sí.
¿Eso?
¿La EH su uso ahí te lo acaba de mandar, es el es el payment de B 64 y el payment sí es del Autorize el capture cierto?

Hector Eduardo Rodriguez Cervantes  41:13
Exacto, sí.

Didier Fabian Franco Gomez  41:14
Y entonces ahí dice que ya están deprecaos y que recomienda utilizar otras rutas, pero.
Ahí sí me quedé con esa duda, si.
Y entonces yo simplemente invoco el el genery a PI para que siga haciendo el proceso como lo venía haciendo o yo voy a invocar directo Aden, y me paso a los nuevos servicios que dicen que deben de usar.

Hector Eduardo Rodriguez Cervantes  41:24
Miren.
No, yo creo.
Sí.
Sí, la invocación como la en este caso va a ser directa, digamos en Generic. No no movimos la versión y documento. Se se trabajó sobre el estándar de que pues sí, generic usa esa versión.

Didier Fabian Franco Gomez  41:42
Sí.

Hector Eduardo Rodriguez Cervantes  41:46
El batch USA esa versión, pero pensándolo bien, en realidad sí podríamos desde el Batch conectar la nueva versión de alguien porque de hecho sería lo ideal porque sí, justo como dices, si es una versión sin soporte como este, el batch sí, la intención.

Didier Fabian Franco Gomez  41:57
Ajá.

Hector Eduardo Rodriguez Cervantes  42:01
O sea, lo que ustedes desarrollen. Sí, la intención es que vayas en directo.
No a gen Erick.
En realidad, la comunicaciones son entre el batch y adyen y naviter, solo para recuperar información y guardan información. Entonces sí podríamos ir, y de hecho creo que está más sencillo. Sí, llega a ver el la integración y creo que los llamados son más simples en el de payments.

Didier Fabian Franco Gomez  42:05
Es.
Y esto no quería, solo aclarar eso. Luego 3 esta solución va a tener infraestructura independiente, o sea, se considera como un servicio independiente y lo único que va a hacer es integrarse cierto.

Hector Eduardo Rodriguez Cervantes  42:27
Sí.
Yo creo que esta en particular, porque justo trae otro proyectito y pedí una cuenta y me rechazó. Ahí la dirección este por ser un tema de integración de pagos que ya ya existe, digamos flujos.
Lo más seguro es que usemos una que ya tengamos, no sé si va a ser una nueva que acabamos de crear para transactions, que es un servicio que igual lleva. Llevamos con ustedes este u otra de las que yo administro con otros equipos, pero calculo que este batch sí lo desplegaríamos en una cuenta de a WS ya existente. ¿No? Y obviamente, pues con infraestructura como servicio, pues nuevamente lo que es.
Pidiendo que con el iaac se hagan los despliegues no de de la infraestructura.

Didier Fabian Franco Gomez  43:18
Sí, sí.

Hector Eduardo Rodriguez Cervantes  43:19
Pero sí será sobre algo existente cada 95% seguro.

Didier Fabian Franco Gomez  43:19
Súper.
Claro, entonces, ahí. Ya de pronto, los temas de configurar las BPSSY, todo eso ya estaría avanzados.

Hector Eduardo Rodriguez Cervantes  43:30
Exacto, correcto.

Didier Fabian Franco Gomez  43:32
¿Solo sería más el la implementación puntual del componente de pronto, y si llegas a tener esa definición, me puedes compartir que eso ya existe o qué equipo lo está administrando? Porque si el detec.

Hector Eduardo Rodriguez Cervantes  43:35
¿Eso?

Didier Fabian Franco Gomez  43:44
¿To tenemos avanzado a ios y cuáles son los templates que ya se usan para meter esta solución dentro del a BPC, o dentro de de las?

Hector Eduardo Rodriguez Cervantes  43:48
No.

Didier Fabian Franco Gomez  43:52
De las segregaciones de redes que que ya tenga cierto para uno identificando. ¿Bueno, esto ya está avanzado y solo de incluirlo dentro de la configuración que yo pongo en ese terraform o esto es algo que definitivamente igual toca subsecretarlo adentro, cierto?

Hector Eduardo Rodriguez Cervantes  43:57
Sí.
Claro.
Sí.
Sí, sí, sí, sí, totalmente, sí. O sea, entiendo y necesitan como el el input para justo construir, no la.
El código que que estaremos desplegando.

Didier Fabian Franco Gomez  44:16
Ajá.
¿Claro, y te estás imaginando esto como una solución netamente serverless? Con funciones.
¿O te imaginas que esto también puede ser con tenerizado y simplemente invocado por el job?
El scheduler.

Hector Eduardo Rodriguez Cervantes  44:31
Pues mira, en un principio lo que nos nos nos solicitaba Pablo era y Alex pues que si lo hiciéramos orientado a eventos no. O sea, ver por ahí ocupar un SQS este.
El o sea que ese sea como el patrón, pues hacia eventos no com.

Didier Fabian Franco Gomez  44:47
Pausa.
Sí lo podemos hacer. Edwin Driven Architecture y eso va a partir del evento, entonces pasará por colas de mensajería que disparan el evento y mueven los Estados.

Hector Eduardo Rodriguez Cervantes  44:50
Exacto.
Sí.
Sí.

Didier Fabian Franco Gomez  44:56
Eso se puede lograr, pero eso no limita que lo podamos hacer como una API con tenerizada o como una función.

Hector Eduardo Rodriguez Cervantes  45:02
Ajá.
Claro.

Didier Fabian Franco Gomez  45:04
Landa, cierto, lo es, es uno lo limitaría, entonces eso se puede, se puede cumplir. Mi recomendación sería que lo hagamos como una API contenerizada.

Hector Eduardo Rodriguez Cervantes  45:05
Sí, cierto, sí, sí, sí.

Didier Fabian Franco Gomez  45:14
¿Por qué? Porque se puede utilizar un framework debajo.
¿Se puede utilizar un nes day s, por ejemplo, para hacer esto se puede utilizar un Python?
Cierto, YYY ahí ya podríamos utilizar un framework que lo soporte y que sea más fácil evolucionar o gestionar toda la trazabilidad y todos los componentes. Entonces, con tener esa, lo hace que sea mucho más eficiente el desarrollo e inclusive el mantenimiento a futuro, porque cuando lo tiras a Landas esto pues tiende a generar muchísimas más porciones de código en diferentes lugares y la infraestructura cambia la forma en que se.

Hector Eduardo Rodriguez Cervantes  45:22
¿Cierto?

Didier Fabian Franco Gomez  45:47
¿Despliegue lo hace más complejo, cierto?
Pero como es una única integración y la corte de su responsabilidad es muy limitado, creo que no tendría mucho sentido hacer un serverless.

Hector Eduardo Rodriguez Cervantes  45:50
Sí.

Didier Fabian Franco Gomez  45:55
Creo que tendría más sentido hacer un contenerizado que se levante, cierto, puede ser en un farguete, por ejemplo.
Hacer una imagen que se levanta en un fargue y eso simplemente expone la API de Procéseme este esta petición puntual cierto YY seguimos trabajando por eventos, porque básicamente una cola invocaría.

Hector Eduardo Rodriguez Cervantes  46:11
Ajá.

Didier Fabian Franco Gomez  46:14
Después haríamos la cola para que llegue el mensaje.
Y una landa que invoque el endpoint con el que ese servicio procesa ciertos. Pero toda la lógica de procesamiento y demás estaría con tener esa esa. Yo creo que por ahí sería una buena arquitectura para esto.

Hector Eduardo Rodriguez Cervantes  46:24
Sí.
Sí, sí, coincido, sí, en lo personal sí me, o sea, la parte de la escalabilidad de la alta disponibilidad YY de. O sea, sí considero que estaría mejor como dices, contenerizarla.
Sé que sean servicios en un cluster.
¿Sí, crear la imagen igual de pronto también lo que buscamos y me olvidé y es importante y ahorita que mencionabas lo de la arquitectura es la escalabilidad, no?
O sea, ahorita y la escalabilidad y aparte de técnica.
O sea, en cuanto a la arquitectura de tecnológica, de que que se defina, pero también la solución a nivel funcional, porque ahorita si vienes la tua, lo que estamos buscando a futuro es que después sean otro tipo de ansilaries los que se puedan programar o automatizar estos pagos. No es como el conejillo de Indias.
Exacto. Entonces cuando se extienda, sigo pensando que pues.

Didier Fabian Franco Gomez  47:21
Va a ir extendiéndose después.

Hector Eduardo Rodriguez Cervantes  47:26
Como tú, que que sería más adecuado implementarlo de manera contenerizada.
¿O servicios?

Jonh Freddy Osses Castro  47:35
Y con par Gates es súper, tienes que poderle escalar, entonces sí es una ventaja también ahí, como nos dice Diego, entonces yo creo que sería la mejor opción.

Didier Fabian Franco Gomez  47:35
Super super.

Hector Eduardo Rodriguez Cervantes  47:42
Sí.

Didier Fabian Franco Gomez  47:43
Sí, súper.
¿Listo, tenemos idea de cuántos millones de registros hay que demoler con cada ejecución?

Hector Eduardo Rodriguez Cervantes  47:49
¿No, YY es, y ahorita digo, puedo preguntar cuánto estiman? Sería muy muy aventura ahorita, porque de hecho están haciendo experimentos a B con ciertas herramientas acá y están moviendo por ejemplo, jugando mucho con la tuba. En qué momento se paga, no.
Por ahí ha habido unos más, más positivos que otros, entonces siguen como moviendo mucho esa parte para ver que pues las decisiones del usuario no.
Finalmente, como parte de un experimento, inclusive, me atrevo a decir que esto si bien buscamos siempre que el desarrollo justo, pues sea escalable y sea reutilizable el componente para otras cosas, porque finalmente domiciliar un pago, pues puede ocurrir en otros flujos.

Didier Fabian Franco Gomez  48:20
Claro.

Hector Eduardo Rodriguez Cervantes  48:37
Como dices, ver cómo lo extendemos, pero sí ahorita digamos que no, no hay como justo, yo creo que va a ser el primer, la primera pruebita para ver, pues si los usuarios realmente lo ocupan o no.

Didier Fabian Franco Gomez  48:46
Claro.

Hector Eduardo Rodriguez Cervantes  48:48
No, no dudo que cambien en algún momento las reglas del juego, como decía lo de quitar lo del bundol y a lo mejor el mismo usuario seleccione la fecha. Ese tipo de cosas no, que igual podemos como explorar en la solución la manera más fácil de si en un punto nos cambian la jugada.
¿Cuál sería, como el worker round, no para soportarlo?

Didier Fabian Franco Gomez  49:08
Claro, y en esa en esa propuesta están esperando lo mismo que en la última que hicimos tiempo y coste fijo.

Hector Eduardo Rodriguez Cervantes  49:16
Sí, correcto, sí, sí, sí, sí, hay de de esa. Pues digo yo, entiendo que igual se acercaron ahí con Alex que que está bien porque pues él quien tiene como quien toma las decisiones y tiene el detalle fino.
De de todo lo que pues de las propuestas que que llegan.
¿Pero sí, o sea, el entregable creo que sería exactamente el mismo, no?
¿Que que vimos la vez pasada realmente, pues como saben lo que lo que normalmente se revise son los costos y el tiempo, no entonces?

Didier Fabian Franco Gomez  49:45
¿Listo y tenemos alguna fecha límite para hacer esto o un tiempo esperado?

Hector Eduardo Rodriguez Cervantes  49:50
Miren el el compromiso del trimestre.
Como les digo ya tec con izzi, está trabajando el la primera parte, que es el el banderar, el pago y lo que les explicaba al inicio entonces.
Pues sí, ya estamos un poquito, la desafortunadamente.
Pues yo creo que en tiempos a cierto punto el compromiso es que el el Q cuatro, nosotros, como saben estamos divididos por QY hay compromisos, este por ejemplo, es un KPI que yo traigo de mi link que que yo.
Lo llevo y nos extiende. Normalmente el compromiso a finales de cuando es el último, nos dan como principios de enero, finales de enero, mediados de enero. Perdón, tenemos que tener el desarrollo listo, no le.
¿Cómo va a estar en 2 partes en 3 partes, es decir, la el pago?
El es el batch o scheduler y aparte el frontend. O sea el compromiso que traemos Ahorita es que en este trimestre saquemos todo el backend.
¿El pago que ya estamos haciendo más el batch, no sé en principios mediados de enero tener la integración completa no?
En test en test.

Didier Fabian Franco Gomez  50:59
¿Y no nos afecta y como?

Hector Eduardo Rodriguez Cervantes  51:01
Todo esto va a ser en test, o sea, no en producción.

Didier Fabian Franco Gomez  51:02
Ah, bueno, eso sí, porque.

Hector Eduardo Rodriguez Cervantes  51:04
No, no, no es test, nada más.

Didier Fabian Franco Gomez  51:06
Ah, bueno, bueno, sí, sí.

Hector Eduardo Rodriguez Cervantes  51:07
Eso eso ayuda un montón, o sea, es salir a a test YY decir, Ah, yo terminé. El desarrollo probado que funciona en test, la producción, yo creo que va a salir hasta finales de marzo del Q uno al siguiente año.

Didier Fabian Franco Gomez  51:09
Claro.
Ese seat han seria startest.

Hector Eduardo Rodriguez Cervantes  51:24
Exacto, sí. Si el alcance desarrollo test. Exacto.

Didier Fabian Franco Gomez  51:25
¿Listo?
Listo, esto no. Entonces yo me habéis contado esta información y revalidar todos los supuestos que tenía con estos detalles que me diste y sobre eso ya miro si me quedan más dudas y te las comunico. Pero esta claridad súper súper bueno. O sea, creo que me me espero muchas dudas ya dentro.

Hector Eduardo Rodriguez Cervantes  51:41
Sí, claro.
Listo, perfecto. Si no cualquier cosa es a n que esté ahí disponible en el chat igual.

Didier Fabian Franco Gomez  51:51
A.

Jonh Freddy Osses Castro  51:52
Yo tengo una última.
Una preguntica cortika pequeñita.
Es que en el documento del Batch veo que todavía el estatus está en Draft. No sé si ya cambió, si de pronto hay una nueva versión o puede ser que se genere algún cambio. Veo que fue del 13 de noviembre.
Es, al menos el que yo tengo, la versión, no sé si sigue así o tal vez haya alguna modificación como para tenerlo presente.

Hector Eduardo Rodriguez Cervantes  52:07
Ya no ahorita.
¿Sí, normalmente es como es un template que trabajamos con izzi y con Tecan solf nos lo piden, tiene creo que un trimestre que lo venimos usando ese template, el draft normalmente se deja hasta que tengamos la versión definitiva no? ¿O sea, si por ejemplo el día de mañana por ejemplo Ahorita subo algunos puntitos, por ahí que salieron, me dice Oye Héctor, Este sabes qué? ¿En lugar de ocupar este servicio de na?
¿Por qué no vamos a este?
Y lo lo debatimos entonces. Yo eso implica que yo actualicemos la versión para irla como cerrando, no normalmente se pone draft hasta que digamos que se va a arrancar el desarrollo, ya no va a haber cambios sobre sobre el documento yo yo ya no le voy a mover, o sea yo ahorita digamos que la adversión que les pasé es la definitiva, no puede que le mueva durante.

Jonh Freddy Osses Castro  53:02
O K.

Hector Eduardo Rodriguez Cervantes  53:05
Este tiempo post estimación a lo mejor porque también sabemos que cuando.
¿Pues ya se empieza a meter mano, surgen cosas, no y por ahí lo que siempre buscamos es, pues este ir teniendo actualizado el documento, no?

Jonh Freddy Osses Castro  53:20
¿De acuerdo de acuerdo? Listo, no perfecto. Esa era la dudita que tenía porque lo vi que estaba en rato.

Hector Eduardo Rodriguez Cervantes  53:23
¿Vale?

Jonh Freddy Osses Castro  53:25
Tenía esa duda, pero no vale super claro, muchas gracias.

Hector Eduardo Rodriguez Cervantes  53:27
¿Sí, no, no?

Didier Fabian Franco Gomez  53:29
Muchas gracias Héctor. Ahí estamos hablando entonces.

Hector Eduardo Rodriguez Cervantes  53:32
Listo, sí, de acuerdo.

Didier Fabian Franco Gomez  53:34
Van a que estén bien, feliz día.

Hector Eduardo Rodriguez Cervantes  53:36
Igual, feliz día cuénse. Estamos hablando hasta luego.

Didier Fabian Franco Gomez  53:38
Bueno, chao.