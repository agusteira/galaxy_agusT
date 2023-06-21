"""
Agus Teira
Div K
"""

ANCHO_VENTANA = 480
ALTO_VENTANA = 720
FPS = 120

##-----------TEMPOS-------------------
tiempo_transcurrido = 0
tiempo_disparar_enemigo = 0
tiempo_transcurrido_nuevo_nivel = 0
disparo_tempo = 0
tiempo_entre_niveles = FPS/2*3
espera_entre_disparos = FPS/5*2

#-----------Banderas---------------------
running = True #True para que este abierta la ventana, y false para que se scierre
flag_nuevo_nivel = False
flag_enemigos = True #Este flag sirve para saber si hay enemigos vivos
flag_tiempo = False #Flag para el segundero
flag = "derecha"
flag_lugar = "menu"


#-----------ruta de imagenes--------------
PATH_FONDO = fr"Imgs\Espacial.jpg"
PATH_MENU = fr"Imgs\Menu.png"
PATH_EXPLOSION = fr"Imgs\Explosion_nave.mp3"
PATH_CANCION = fr"Imgs\Mountains.mp3"
PATH_SHIP = fr"Imgs\Sprite-Ship.png"
PATH_HELTH_BAR = fr"Imgs\healt_bar.png"
PATH_DISPAROS = fr"Imgs\Disparos.mp3"
PATH_BD = fr"base de datos\bd_score.db"
#-----------LISTA DE BALAS-------------------
balas_enemigas = []
balas_enemigas_colisionadas = []
balas_actualizadas = []
balas_enemigas_actualizadas = []

#-----------VARIABLES Y PARAMETROS-------------------
vida_enemigos = 1
cantidad_enemigos_al_inicio = 1
nave_vida = 5
velocidad_balas = 15
nombre_jugador = ''
