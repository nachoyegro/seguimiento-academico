# Núcleo de Seguimiento Académico
[![Build Status](https://travis-ci.org/nachoyegro/seguimiento-academico.svg?branch=master)](https://travis-ci.org/nachoyegro/seguimiento-academico)
[![codecov](https://codecov.io/gh/nachoyegro/seguimiento-academico/branch/master/graph/badge.svg)](https://codecov.io/gh/nachoyegro/seguimiento-academico)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

## Resumen

El Núcleo de Seguimiento Académico se encarga de administrar los datos no sensibles de los estudiantes y sus materias cursadas, las inscripciones, planes de estudio con sus créditos, recorrido obligatorio y recomendado de inscripciones, entre otros.
A su vez, tiene la capacidad de servir dichos datos para que sean consumidos por los usuarios que tengan los permisos correspondientes.
Los usuarios tienen permisos asignados que corresponden con la carrera a la que pertenecen, que les permiten consultar datos de dicha carrera. 


## Tecnologías usadas

## Instalación con Docker

Docker

Si no se tiene instalado, correr el siguiente comando:

```
  $ apt install docker.io
```

Docker-compose

Si no se tiene instalado, correr el siguiente comando:

```
  $ apt install docker-compose
```

Es necesario crear una red para que todas las instancias puedan comunicarse

```
  $ docker network create seguimiento-academico
```

### Desarrollo

El deploy en desarrollo implica hacerlo con una base de datos SQLite de prueba, la cual se crea automáticamente.
Además, la aplicación queda corriendo con el Web server de Django, que no está destinado para ser usado en producción.

```
  $ docker-compose -f docker-compose.dev.yml up --build -d
```


### Producción

El deploy para producción tiene algunos aspectos extra, como correr la aplicación con Gunicorn y Nginx para resolver los requests.
Además, la configuración de docker-compose implica que se tenga una base de datos PostgreSQL.

```
  $ docker-compose -f docker-compose.prod.yml up --build -d
```

## Importadores

- [Materias Cursadas](alumnos/docs/md/IMPORTADOR_MATERIAS_CURSADAS.md)
- [Inscripciones](alumnos/docs/md/IMPORTADOR_INSCRIPCIONES.md)
- [Planes](alumnos/docs/md/IMPORTADOR_PLANES.md)
- [Requisitos de materias](alumnos/docs/md/IMPORTADOR_REQUISITOS.md)
- [Datos personales de alumnos](alumnos/docs/md/IMPORTADOR_DATOS_PERSONALES.md)
