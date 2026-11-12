# EDA Framework: Glosario y definiciones generales

> Fuente: [https://segurosti.atlassian.net/wiki/spaces/AR/pages/5251366915](https://segurosti.atlassian.net/wiki/spaces/AR/pages/5251366915) · versión 8 · actualizado 2026-08-05 por Víctor Daniel Martínez Olier

> **⚠️ Advertencia**
>
> En esta documentación EDA es una abreviatura para *Event-Driven Architecture*. **NO TIENE NINGUNA RELACIÓN CON LA MISMA ABREVIATURA USADA POR OTRA GERENCIA PARA REFERIRSE A ESTRATEGIA DE DATOS Y ANALÍTICA.**

# Evento (Events)

Un evento es un registro inmutable de un hecho (*fact*), normalmente un cambio de estado en un sistema. Los eventos deben tener estas características:

- Notifican un cambio de estado o hecho.
- Son inmutables (no cambian su valor).

## Flujo de eventos (Event streams)

Un flujo de eventos es una serie continua de eventos. Sus características son:

- El flujo puede haber comenzado antes de procesarlo.
- El final es desconocido y se considera infinito.

## Backbone (troncal) de eventos

Es la capa de infraestructura y plataforma que soporta el flujo de eventos necesario para las arquitecturas EDA. Esta capa, crítica para el funcionamiento, debe contar con capacidades técnicas robustas, como:

- Resiliencia.
- Escalabilidad.
- Seguridad.

# CQRS

Abreviatura del patrón de segregación de responsabilidades de consulta y comandos, inglés *Command and Query Responsibility Segregation*.

## Comando (*Command*)

Acción enviada a otro sistema para modificar su estado.

## Consulta (*Query*)

Solicitud de información enviada a otro sistema o componente, que no modifica su estado ni genera efectos secundarios (*side-effects*).

> **✅ Lineamiento**
>
> Por definición, las consultas son idempotentes, ya que no cambian el estado sin importar cuántas veces se ejecuten.

> **ℹ️ Nota**
>
> Aunque algunas consultas usan funciones puras, idempotencia no es lo mismo que pureza. Las funciones puras siempre devuelven la misma salida para las mismas entradas y no tienen efectos secundarios (*side-effects*).

# Conciencia del destinatario (*awareness of recipient*)

Concepto clave para decidir aplicar EDA. ¿Qué implica que el emisor conozca las capacidades del receptor?. En una arquitectura orientada a eventos, el emisor no debe conocer al destinatario. Si conoce quién recibe el mensaje, el sistema deja de ser estrictamente "orientado a eventos" y se convierte en una arquitectura de "paso de mensajes" o "comandos".

# Reproducibilidad de eventos (*replayability of events*)

Capacidad de reproducir o reprocesar eventos históricos para reconstruir el estado, auditar, depurar o alimentar nuevos consumidores.

# Inmutabilidad

Los eventos no cambian; cualquier modificación se realiza mediante nuevos eventos compensatorios.

# Durabilidad

Los eventos no se eliminan tras ser leídos; permanecen disponibles para múltiples lecturas.

# Trazabilidad funcional

Capacidad para seguir eventos funcionales. Debe diferenciarse claramente de la reproducibilidad.

# Fuente única de verdad (SSOT)

¿Qué significa en EDA? ¿Cómo se diferencia una base de datos transaccional de un event store?

# Event Store vs Event Broker

Roles y diferencias: almacenamiento duradero frente a distribución de eventos.

# Framework de liberación de datos

Qué son y cómo habilitan la captura de cambios en bases transaccionales.

# Procesador de eventos

Función en la arquitectura: consumir eventos y generar vistas o nuevos eventos.

# Arquitectura Lambda vs Kappa

Diferencias y cuándo aplicar cada una en escenarios transaccionales y analíticos.

# Mensaje de confirmación (ACK)

Definiciones claras en lugar de acrónimos: ¿qué implica y cuándo es necesario?
