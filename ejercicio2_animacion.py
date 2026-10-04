# ejercicio2_animacion.py
# Extensión voluntaria del Ejercicio 2: animación con 20 rosetas (N de 5 a 24).
# Reutiliza las funciones de ejercicio2_roseta.py (bresenham, generar_puntos_circulo
# y dibujar_roseta). Salida: roseta_animacion.gif

from PIL import Image
from ejercicio2_roseta import generar_puntos_circulo, dibujar_roseta

LADO = 700
CENTRO = LADO // 2
RADIO = 300
TAMANO_GIF = 400          # se reduce cada cuadro para que el GIF pese poco

cuadros = []
for n in range(5, 25):    # N = 5, 6, ..., 24  -> 20 cuadros
    img = Image.new("RGB", (LADO, LADO), "black")
    pixels = img.load()
    puntos = generar_puntos_circulo(CENTRO, CENTRO, RADIO, n)
    dibujar_roseta(pixels, puntos, LADO, LADO)
    cuadros.append(img.resize((TAMANO_GIF, TAMANO_GIF), Image.LANCZOS))

# Se guarda en bucle infinito, 250 ms por cuadro
cuadros[0].save("roseta_animacion.gif", save_all=True,
                append_images=cuadros[1:], duration=250, loop=0)
print(f"Animación generada con {len(cuadros)} cuadros: roseta_animacion.gif")
