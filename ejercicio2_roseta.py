# ejercicio2_roseta.py
# Taller de Programación de 5.ª Generación I - Tarea práctica Unidad III
# Ejercicio 2: rosetas geométricas (estilo mandala) con el algoritmo de Bresenham.
# Salida: roseta_12.png, roseta_24.png, roseta_36.png (700 x 700 píxeles)
#         + roseta.png (copia de la variante base N = 24)
#         + extensiones: roseta_no_adyacentes.png y roseta_fondo_color.png

import math
from PIL import Image


# ---------------------------------------------------------------------------
# Algoritmo de Bresenham (copiado de la clase, sin modificar su firma)
# ---------------------------------------------------------------------------
def bresenham(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Bresenham generalizado, aritmetica entera."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0

    while True:
        if 0 <= x < ancho and 0 <= y < alto:
            pixels[x, y] = color
        if x == x1 and y == y1: break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


# ---------------------------------------------------------------------------
# Paletas de colores para el gradiente (lista de colores "parada")
# ---------------------------------------------------------------------------
PALETA_BASE = [(255, 215, 0), (255, 0, 140), (0, 200, 255)]            # dorado -> magenta -> cian
PALETA_COMPLEMENTARIA = [(255, 110, 0), (255, 190, 0), (255, 250, 150)]  # naranja -> amarillo (sobre azul)


def interpolar_color(c1, c2, t):
    """Mezcla lineal entre dos colores RGB; t va de 0.0 (c1) a 1.0 (c2)."""
    return tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3))


def color_gradiente(t, paleta):
    """Devuelve el color del gradiente para un valor t entre 0.0 y 1.0."""
    t = max(0.0, min(1.0, t))
    tramo = t * (len(paleta) - 1)            # posición dentro de la paleta
    i = int(tramo)
    if i >= len(paleta) - 1:
        return paleta[-1]
    return interpolar_color(paleta[i], paleta[i + 1], tramo - i)


# ---------------------------------------------------------------------------
# Funciones pedidas por la consigna
# ---------------------------------------------------------------------------
def generar_puntos_circulo(cx, cy, radio, n):
    """Devuelve n puntos equiespaciados sobre una circunferencia imaginaria."""
    puntos = []
    for i in range(n):
        angulo = 2 * math.pi * i / n          # ángulo de cada punto (radianes)
        x = cx + int(radio * math.cos(angulo))
        y = cy + int(radio * math.sin(angulo))
        puntos.append((x, y))
    return puntos


def color_segun_distancia(p1, p2, centro, radio, paleta):
    """Color de una línea según la distancia de su punto medio al centro.

    Las líneas que pasan cerca del centro (diámetros) toman el primer color de
    la paleta; las cuerdas cortas, cercanas al borde, toman el último.
    """
    mx = (p1[0] + p2[0]) / 2
    my = (p1[1] + p2[1]) / 2
    distancia = math.hypot(mx - centro[0], my - centro[1])
    return color_gradiente(distancia / radio, paleta)


def dibujar_roseta(pixels, puntos, ancho, alto, paleta=None):
    """Conecta cada punto con todos los demás usando bresenham().

    Aplica un gradiente de color según la distancia de cada línea al centro.
    Devuelve la cantidad de líneas trazadas: n * (n - 1) / 2.
    """
    if paleta is None:
        paleta = PALETA_BASE
    n = len(puntos)
    centro = (ancho // 2, alto // 2)
    radio = math.hypot(puntos[0][0] - centro[0], puntos[0][1] - centro[1])

    # Se arma la lista de líneas con su color y se dibujan de las más externas
    # a las más centrales, para que los colores del centro queden por encima.
    lineas = []
    for i in range(n):
        for j in range(i + 1, n):             # cada par una sola vez
            color = color_segun_distancia(puntos[i], puntos[j], centro, radio, paleta)
            distancia = math.hypot((puntos[i][0] + puntos[j][0]) / 2 - centro[0],
                                   (puntos[i][1] + puntos[j][1]) / 2 - centro[1])
            lineas.append((distancia, i, j, color))
    lineas.sort(reverse=True)

    for _, i, j, color in lineas:
        bresenham(pixels, puntos[i][0], puntos[i][1],
                  puntos[j][0], puntos[j][1], color, ancho, alto)
    return len(lineas)


# ---------------------------------------------------------------------------
# Extensión: roseta solo con puntos no adyacentes
# ---------------------------------------------------------------------------
def dibujar_roseta_no_adyacentes(pixels, puntos, salto_minimo, ancho, alto, paleta=None):
    """Conecta solo pares separados por al menos 'salto_minimo' posiciones.

    Con salto_minimo = 5 se omiten las cuerdas cortas (vecinos y casi vecinos),
    lo que deja un anillo vacío cerca del borde de la roseta.
    """
    if paleta is None:
        paleta = PALETA_BASE
    n = len(puntos)
    centro = (ancho // 2, alto // 2)
    radio = math.hypot(puntos[0][0] - centro[0], puntos[0][1] - centro[1])
    cantidad = 0
    for i in range(n):
        for j in range(i + 1, n):
            separacion = min(j - i, n - (j - i))     # distancia circular entre puntos
            if separacion >= salto_minimo:
                color = color_segun_distancia(puntos[i], puntos[j], centro, radio, paleta)
                bresenham(pixels, puntos[i][0], puntos[i][1],
                          puntos[j][0], puntos[j][1], color, ancho, alto)
                cantidad += 1
    return cantidad


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    LADO = 700
    CENTRO = LADO // 2
    RADIO = 300

    # Tres variantes con distinto N (fondo negro, gradiente dorado-magenta-cian)
    for n in [12, 24, 36]:
        img = Image.new("RGB", (LADO, LADO), "black")
        pixels = img.load()
        puntos = generar_puntos_circulo(CENTRO, CENTRO, RADIO, n)
        lineas = dibujar_roseta(pixels, puntos, LADO, LADO)
        img.save(f"roseta_{n}.png")
        if n == 24:
            img.save("roseta.png")            # variante base
        print(f"N = {n:>2}: {lineas} líneas -> roseta_{n}.png")

    # Extensión 1: solo puntos no adyacentes (saltando de a 5)
    img = Image.new("RGB", (LADO, LADO), "black")
    pixels = img.load()
    puntos = generar_puntos_circulo(CENTRO, CENTRO, RADIO, 36)
    lineas = dibujar_roseta_no_adyacentes(pixels, puntos, 5, LADO, LADO)
    img.save("roseta_no_adyacentes.png")
    print(f"No adyacentes (N = 36, salto 5): {lineas} líneas -> roseta_no_adyacentes.png")

    # Extensión 2: fondo de color con colores de línea complementarios
    img = Image.new("RGB", (LADO, LADO), (10, 20, 70))   # azul noche
    pixels = img.load()
    puntos = generar_puntos_circulo(CENTRO, CENTRO, RADIO, 30)
    lineas = dibujar_roseta(pixels, puntos, LADO, LADO, PALETA_COMPLEMENTARIA)
    img.save("roseta_fondo_color.png")
    print(f"Fondo de color (N = 30): {lineas} líneas -> roseta_fondo_color.png")
