# taller5g-unidad3-rodriguez

Tarea práctica de la **Unidad III — Conversión por rastreo**
**Asignatura:** Taller de Programación de 5.ª Generación I — Universidad Americana
**Docente:** Prof. Mgtr. Alberto F. Giménez Méndez
**Alumno:** Osvaldo Matías Rodríguez Amarilla (apellido: Rodríguez)

## Contenido

| Archivo | Descripción |
|---|---|
| `ejercicio1_casa.py` | Ejercicio 1: casa estilizada de 600 × 500 px dibujada con el algoritmo **DDA**. |
| `ejercicio2_roseta.py` | Ejercicio 2: rosetas geométricas de 700 × 700 px con el algoritmo de **Bresenham**. |
| `ejercicio2_animacion.py` | Extensión del Ejercicio 2: GIF animado con 20 rosetas (N de 5 a 24). |
| `casa.png` | Imagen generada por el Ejercicio 1. |
| `roseta_12.png`, `roseta_24.png`, `roseta_36.png` | Imágenes generadas por el Ejercicio 2 (N = 12, 24 y 36). |
| `roseta.png` | Copia de la variante base (N = 24). |
| `roseta_no_adyacentes.png`, `roseta_fondo_color.png`, `roseta_animacion.gif` | Extensiones voluntarias del Ejercicio 2. |

## Requisitos

- Python 3.10 o superior
- Pillow (`pip install Pillow`)

## Cómo ejecutar

```bash
# Ejercicio 1: genera casa.png
python ejercicio1_casa.py

# Ejercicio 2: genera roseta_12.png, roseta_24.png, roseta_36.png (y las extensiones)
python ejercicio2_roseta.py

# Extensión: genera roseta_animacion.gif (requiere ejercicio2_roseta.py en la misma carpeta)
python ejercicio2_animacion.py
```

Las funciones `dda()` y `bresenham()` se reutilizan tal como fueron presentadas en clase, sin modificar su firma.
