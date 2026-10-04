# ejercicio1_casa.py
# Taller de Programación de 5.ª Generación I - Tarea práctica Unidad III
# Ejercicio 1: composición geométrica (casa estilizada) usando el algoritmo DDA.
# Salida: casa.png (600 x 500 píxeles)

import math
from PIL import Image


# ---------------------------------------------------------------------------
# Algoritmo DDA (copiado de la clase, sin modificar su firma)
# ---------------------------------------------------------------------------
def dda(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Traza una linea usando el algoritmo DDA."""
    dx = x1 - x0
    dy = y1 - y0

    pasos = max(abs(dx), abs(dy))

    if pasos == 0:         # los dos puntos coinciden
        return

    x_inc = dx / pasos
    y_inc = dy / pasos

    x, y = x0, y0
    for _ in range(int(pasos) + 1):
        px, py = round(x), round(y)
        if 0 <= px < ancho and 0 <= py < alto:
            pixels[px, py] = color
        x += x_inc
        y += y_inc


# ---------------------------------------------------------------------------
# Paleta de colores (cada elemento usa un color distinto)
# ---------------------------------------------------------------------------
COLOR_CUERPO = (170, 60, 40)      # ladrillo
COLOR_TECHO = (110, 20, 20)       # rojo oscuro
COLOR_PUERTA = (90, 50, 20)       # marrón
COLOR_VENTANA = (20, 80, 200)     # azul
COLOR_SOL = (255, 160, 0)         # naranja
COLOR_PISO = (20, 120, 20)        # verde
COLOR_CHIMENEA = (60, 60, 60)     # gris oscuro
COLOR_TRONCO = (100, 60, 20)      # marrón tronco
COLOR_COPA = (0, 140, 0)          # verde copa
COLOR_NUBE = (130, 140, 170)      # gris azulado
COLOR_HUMO = (110, 110, 110)      # gris humo


# ---------------------------------------------------------------------------
# Elementos gráficos: cada uno es una función separada que usa dda()
# ---------------------------------------------------------------------------
def dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Rectángulo con esquinas (x0, y0) y (x1, y1): cuatro llamadas a dda()."""
    dda(pixels, x0, y0, x1, y0, color, ancho, alto)  # lado superior
    dda(pixels, x1, y0, x1, y1, color, ancho, alto)  # lado derecho
    dda(pixels, x1, y1, x0, y1, color, ancho, alto)  # lado inferior
    dda(pixels, x0, y1, x0, y0, color, ancho, alto)  # lado izquierdo


def dibujar_triangulo(pixels, p1, p2, p3, color, ancho, alto):
    """Triángulo definido por tres vértices: tres llamadas a dda()."""
    dda(pixels, p1[0], p1[1], p2[0], p2[1], color, ancho, alto)
    dda(pixels, p2[0], p2[1], p3[0], p3[1], color, ancho, alto)
    dda(pixels, p3[0], p3[1], p1[0], p1[1], color, ancho, alto)


def dibujar_puerta(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Puerta: un rectángulo más una manija formada por una línea corta."""
    dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto)
    ym = (y0 + y1) // 2
    dda(pixels, x1 - 10, ym, x1 - 5, ym, color, ancho, alto)  # manija


def dibujar_ventana(pixels, x, y, lado, color, ancho, alto):
    """Ventana cuadrada con esquina superior izquierda (x, y) y tamaño 'lado'."""
    dibujar_rectangulo(pixels, x, y, x + lado, y + lado, color, ancho, alto)


def dibujar_sol(pixels, cx, cy, radio, n_rayos, color, ancho, alto):
    """Sol: n_rayos líneas que irradian desde el punto central (cálculo polar)."""
    for i in range(n_rayos):
        angulo = 2 * math.pi * i / n_rayos
        x1 = cx + int(radio * math.cos(angulo))
        y1 = cy + int(radio * math.sin(angulo))
        dda(pixels, cx, cy, x1, y1, color, ancho, alto)


def dibujar_piso(pixels, y, color, ancho, alto):
    """Línea de piso que atraviesa toda la imagen horizontalmente."""
    dda(pixels, 0, y, ancho - 1, y, color, ancho, alto)


# ---------------------------------------------------------------------------
# Extensiones voluntarias: chimenea con humo, árboles y nubes
# ---------------------------------------------------------------------------
def dibujar_chimenea(pixels, x0, y_tope, x1, y_base_izq, y_base_der, color, ancho, alto):
    """Chimenea abierta por abajo: apoya sobre la pendiente del techo."""
    dda(pixels, x0, y_base_izq, x0, y_tope, color, ancho, alto)  # lado izquierdo
    dda(pixels, x0, y_tope, x1, y_tope, color, ancho, alto)      # tapa
    dda(pixels, x1, y_tope, x1, y_base_der, color, ancho, alto)  # lado derecho


def dibujar_humo(pixels, x, y, n_tramos, color, ancho, alto):
    """Humo: poligonal ondulada que sube desde (x, y) usando segmentos cortos."""
    x_ant, y_ant = x, y
    for i in range(1, n_tramos + 1):
        x_nuevo = x + int(10 * math.sin(i * 1.1))   # oscilación lateral
        y_nuevo = y - 14 * i                         # avance hacia arriba
        dda(pixels, x_ant, y_ant, x_nuevo, y_nuevo, color, ancho, alto)
        x_ant, y_ant = x_nuevo, y_nuevo


def dibujar_arbol(pixels, x, y_base, color_tronco, color_copa, ancho, alto):
    """Árbol: tronco rectangular + copa triangular."""
    dibujar_rectangulo(pixels, x - 8, y_base - 40, x + 8, y_base,
                       color_tronco, ancho, alto)
    dibujar_triangulo(pixels, (x - 38, y_base - 40), (x, y_base - 115),
                      (x + 38, y_base - 40), color_copa, ancho, alto)


def dibujar_nube(pixels, cx, cy, color, ancho, alto):
    """Nube: tres semicírculos (poligonales de líneas cortas) sobre una base."""
    for dx_c, radio in [(-26, 18), (0, 25), (26, 18)]:
        centro_x = cx + dx_c
        x_ant = centro_x - radio
        y_ant = cy
        for paso in range(1, 9):
            angulo = math.pi + math.pi * paso / 8     # de 180° a 360° (arco superior)
            x_nuevo = centro_x + int(radio * math.cos(angulo))
            y_nuevo = cy + int(radio * math.sin(angulo))
            dda(pixels, x_ant, y_ant, x_nuevo, y_nuevo, color, ancho, alto)
            x_ant, y_ant = x_nuevo, y_nuevo
    dda(pixels, cx - 44, cy, cx + 44, cy, color, ancho, alto)  # base plana


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
ancho, alto = 600, 500
imagen = Image.new("RGB", (ancho, alto), (200, 230, 255))   # cielo celeste
pixels = imagen.load()                                       # acceso al frame buffer

# Línea de piso (atraviesa toda la imagen)
dibujar_piso(pixels, 400, COLOR_PISO, ancho, alto)

# Cuerpo de la casa
dibujar_rectangulo(pixels, 150, 250, 400, 400, COLOR_CUERPO, ancho, alto)

# Techo triangular
dibujar_triangulo(pixels, (130, 250), (275, 150), (420, 250),
                  COLOR_TECHO, ancho, alto)

# Chimenea y humo (extensión)
dibujar_chimenea(pixels, 340, 160, 370, 195, 215, COLOR_CHIMENEA, ancho, alto)
dibujar_humo(pixels, 355, 160, 5, COLOR_HUMO, ancho, alto)

# Puerta
dibujar_puerta(pixels, 250, 320, 300, 400, COLOR_PUERTA, ancho, alto)

# Dos ventanas cuadradas
dibujar_ventana(pixels, 175, 280, 50, COLOR_VENTANA, ancho, alto)
dibujar_ventana(pixels, 325, 280, 50, COLOR_VENTANA, ancho, alto)

# Sol en la esquina superior derecha: 12 rayos desde el centro
dibujar_sol(pixels, 510, 80, 50, 12, COLOR_SOL, ancho, alto)

# Árboles a ambos lados (extensión)
dibujar_arbol(pixels, 70, 400, COLOR_TRONCO, COLOR_COPA, ancho, alto)
dibujar_arbol(pixels, 520, 400, COLOR_TRONCO, COLOR_COPA, ancho, alto)

# Nubes (extensión)
dibujar_nube(pixels, 130, 80, COLOR_NUBE, ancho, alto)
dibujar_nube(pixels, 320, 55, COLOR_NUBE, ancho, alto)

imagen.save("casa.png")
print("Imagen generada: casa.png")
