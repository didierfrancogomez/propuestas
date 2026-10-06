vamos a hacer una nueva propuesta de trabajo a Viva, 
en este folder /Users/didierfranco/Documents/GitHub/techandsolve/propuestas/viva/propuestas/nuevo-modelo-de-trabajo

Actualmente el cliente tiene un modelo staff con tres desarrolladores, donde constantemente tiene micromanagement sobre el equipo de trabajo 

El modelo de trabajo actual es 
Un equipo genera task en jira, luego el equipo de tech tomas esas task y las desarrolla, luego el equipo tech hace un pr que revisa otro equipo 
luego el otro equipo hace cometarios y el equipo tech resuelve los comentarios hasta garantizar que todo queda acorde a lo que pide la task y lo que revisa quien mira el pr. 

El equipo no automatiza pruebas. 
El equipo debe subir evidencias de pruebas manuales a jira task 
El po del proyecto hace micromanagement a las personas, siempre mirando los tiempos de las jira task, las fechas y la cantidad de intentos de pasar el pr (numero de veces que se resuelven los comentarios y luego aparecen mas)

Nuestra propuesta
Cambiar el modelo de trabajo 
Permitir al equipo de tech ser parte del equipo de diseña las task, esto permite tener mayor contexto de negocio que permite luego tener una sinergia diferente con el equipo de implementación 

Trabajar en un modelo diferente donde se estimen las actividades no por horas sino por tallas, 
No tener personas fijas, sino que el cliente contrata una cantidad de task represantan un peso o tallaje general al mes. 
El modelo de cumplimiento no se mide por devoluciones de pr u horas, se mide por task con pr aprobado. 

En el proceso el equipo requiere: 
1. Automatizar pruebas unitarias 
2. Utilizar sonar como herramienta centralizada de buenas prácticas


En la evidencia se garantiza 
1. Un pr por jira task con pruebas unitarias que garantizan cobertura de cada criterio de aceptacion solicitado en la jirta task 
2. Evidencia de resultado de pruebas realizadas 
3. Sesión de entrega a Viva de la actividad con sus evidencias
4. Task con pr aprobado. 

Condiciones
1. Un cambio de alcance de una jira task deberá ser un nuevo jira task 
2. Una actividad podrá ser rechazada para su implementación si
2.1 El tallaje de la jira task no es acorde a lo que considera el equipo Tech And Solve como oportuno 
2.2 No hay criterios de aceptación claros en la jira task 
2.3 Hay ambiguedad en la definición de jira task 
2.4 Hay dependencias externas no resueltas 
3. El equipo entrega la jira task con el pr resuelto, pero si el equipo de Viva decide no hacerle merge y luego pide revisiones posteriores porque el base brach ya ha cambiado y el merge no se puede hacer limpio, entonces tendrá que ser otra jira task con estimacion independiente para ello. 
4. Todo control de cambios es una jira task nueva con estimacion independiente 
5. El equipo tiene libertidad de implementar las pruebas unitarias que considere oportunas
6. El revisor del pr no podrá estar mas de dos días sin dar respuesta el pr, ya que eso acarrea reprocesos para todo el equipo de desarrollo. 
7. El cliente no contrata personas específicas, contrata numero de actividades a desarrollar segun tallaje 

Busca un estándar de talla en agile para estimar historias y haz una propuesta con diferentes cantidades de historias, tallas por mes. 

crea la propuesta en este mismo folder en html. 