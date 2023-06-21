"""
Agus Teira
Div K
"""
import pygame
import sqlite3
from funciones import *
from constantes import *
from colores import *
import time
import random

reloj = pygame.time.Clock()

class Juego:
    def __init__(self, ANCHO_VENTANA, ALTO_VENTANA, PATH_FONDO, PATH_MENU) -> None:
        self.ANCHO = ANCHO_VENTANA
        self.ALTO = ALTO_VENTANA 
        self.FONDO = PATH_FONDO

        self.MENU = PATH_MENU
        self.menu_img = pygame.image.load(self.MENU)

    def iniciar(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.ANCHO,self.ALTO))
        pygame.display.set_caption("Anchoas vs aceitunas")
        return self.screen
    
    def jugar(self, cant_enemigos, vida_enemigos, nave_vida):
        nave = Nave(self.screen, nave_vida)
        segundero = -3
        flag_lugar = "juego"
        enemigos = crear_enemigos(Enemigo, self.screen, cant_enemigos, 60, 50, vida_enemigos)
        cancion_juego = reproducir_musica(PATH_CANCION,0)
        nave.secuencia_inicial(reloj, self.fondo_juego)
        return flag_lugar, enemigos, nave, segundero, cancion_juego

    def cerrar(self, evento, running):
        if evento.type == pygame.QUIT:
            running = False
        return running

    def fondear(self):
        self.fondo_juego = pygame.image.load(self.FONDO)
        self.fondo_juego = pygame.transform.scale(self.fondo_juego,(self.ANCHO, self.ALTO))
        return self.fondo_juego

    def button_play(self):
        self.menu_img = pygame.transform.scale(self.menu_img, (220, 85))
        menu_rect = self.menu_img.get_rect()
        menu_rect.x = self.screen.get_width() // 2 - menu_rect.width //2
        menu_rect.y = self.screen.get_height() // 2 - 100
        
        # Crear un objeto de fuente
        font = pygame.font.SysFont("Arial Bold", 50)  # Ajusta el tamaño de la fuente según tus necesidades

        # Renderizar el texto en una superficie
        texto_play = font.render("P  L  A  Y", True, WHITE)  # Ajusta el texto y el color según tus necesidades

        # Obtener el rectángulo del texto y centrarlo sobre la imagen
        texto_play_rect = texto_play.get_rect()
        texto_play_rect.centerx = menu_rect.centerx
        texto_play_rect.centery = menu_rect.centery

        self.screen.blit(self.menu_img, menu_rect)
        self.screen.blit(texto_play, texto_play_rect)
        return menu_rect

    def button_stats(self):
        self.menu_img = pygame.transform.scale(self.menu_img, (220, 85))
        menu_rect = self.menu_img.get_rect()
        menu_rect.x = self.screen.get_width() // 2 - menu_rect.width //2
        menu_rect.y = self.screen.get_height() // 2 
        
        # Crear un objeto de fuente
        font = pygame.font.SysFont("Arial Bold", 50)  # Ajusta el tamaño de la fuente según tus necesidades

        # Renderizar el texto en una superficie
        texto_stats = font.render("S  T  A  T  S", True, WHITE)  # Ajusta el texto y el color según tus necesidades

        # Obtener el rectángulo del texto y centrarlo sobre la imagen
        texto_stats_rect = texto_stats.get_rect()
        texto_stats_rect.centerx = menu_rect.centerx
        texto_stats_rect.centery = menu_rect.centery

        self.screen.blit(self.menu_img, menu_rect)
        self.screen.blit(texto_stats, texto_stats_rect)
        return menu_rect

    def botones_menu(self):
        button_stats = self.button_stats()
        button_play = self.button_play()

        return button_stats, button_play

    def button_atras(self):
        self.menu_img = pygame.transform.scale(self.menu_img, (150, 55))
        menu_rect = self.menu_img.get_rect()
        menu_rect.x = 10
        menu_rect.y = 650

        # Crear un objeto de fuente
        font = pygame.font.SysFont("Arial Bold", 30)  # Ajusta el tamaño de la fuente según tus necesidades

        # Renderizar el texto en una superficie
        texto_stats = font.render("A T R A S", True, WHITE)  # Ajusta el texto y el color según tus necesidades

        # Obtener el rectángulo del texto y centrarlo sobre la imagen
        texto_stats_rect = texto_stats.get_rect()
        texto_stats_rect.centerx = menu_rect.centerx
        texto_stats_rect.centery = menu_rect.centery

        self.screen.blit(self.menu_img, menu_rect)
        self.screen.blit(texto_stats, texto_stats_rect)
        return menu_rect

class Nave:
    def __init__(self,screen, nave_vida) -> None:
        self.caminar = getSuperficies(PATH_SHIP,7,4)
        self.movimiento = 6 #la imagen inicial
        self.vida = nave_vida
        self.score = 0
        self.animacion = self.caminar
        self.imagen = self.animacion[self.movimiento]
        self.rect = self.imagen.get_rect()
        self.rect.x = 185
        self.rect.y = 700
        self.screen = screen
        self.balas_nave = []
        #self.rect.y = 520
    
    def actualizar_derecha(self):
        self.rect.x = self.rect.x - 20

        #El cambio de la imagen del sprite dependiendo en que sprite se encuentre
        if(0< self.movimiento <= 2):
            self.movimiento -= 1
        elif (self.movimiento==0):
            self.movimiento = 0
        else:
            self.movimiento = 2
        if self.rect.x < 0:
            self.rect.x = 0

        tiempo_transcurrido = 0
        return tiempo_transcurrido

    def actualizar_izquierda(self):
        self.rect.x = self.rect.x + 20

        #El cambio de la imagen del sprite dependiendo en que sprite se encuentre
        if(3< self.movimiento <= 5):
            self.movimiento -= 1
        elif (self.movimiento==3):
            self.movimiento = 3
        else:
            self.movimiento = 5
        if self.rect.x > ANCHO_VENTANA - 90:  # Ajusta el valor según el tamaño del objeto
            self.rect.x = ANCHO_VENTANA - 90

        tiempo_transcurrido = 0 
        return tiempo_transcurrido # el TT es para que la nave vuelva a su valor predefinido cuando pase cierto tiempo

    def volver(self):
        if (self.movimiento in [5,4,3,2,1,0]):
            self.movimiento = 6

    def dibujar(self):
        self.imagen = self.animacion[self.movimiento]
        self.screen.blit(self.imagen, self.rect)

    def health_bar (self, nave_vida):
        #Carga la imagen
        self.barra = pygame.image.load(PATH_HELTH_BAR)
        self.barra = pygame.transform.scale(self.barra,(250, 50))
        self.rect_barra = self.barra.get_rect()
        self.rect_barra.y= 650
        self.rect_barra.x= 10
        try: #El try esta porque si la vida llega a 0 se bugue por la division en la segunda linea
            #Carga el contador de vida
            rectangulo_rojo = pygame.Rect(self.rect_barra.x+1, self.rect_barra.y+6, self.rect_barra.width-6, self.rect_barra.height-15)
            rectangulo_rojo.width = rectangulo_rojo.width / nave_vida * self.vida
            pygame.draw.rect(self.screen, (255, 0, 0),rectangulo_rojo)
            self.screen.blit(self.barra, self.rect_barra)
        except:
            print("Se encontro un error, se sigue")

    def morir(self, fondo_juego, cancion_juego):
        #Animacion de morir del sprite
        if self.vida == 0:
            cancion_juego.stop()
            reloj.tick(60)
            self.movimiento = 27
            self.screen.blit(fondo_juego,fondo_juego.get_rect())
            self.dibujar()
            pygame.display.flip()
            reproducir_musica(PATH_EXPLOSION,2)
            while self.movimiento > 21:
                time.sleep(0.5)
                self.movimiento -= 1
                self.screen.blit(fondo_juego,fondo_juego.get_rect())
                self.dibujar()
                pygame.display.flip()
            
    def secuencia_inicial(self,reloj,fondo_juego):
        while self.rect.y > 520:
            reloj.tick(60)
            self.rect.y -= 0.5000001
            self.screen.blit(fondo_juego,fondo_juego.get_rect())
            self.dibujar()
            pygame.display.flip()

    def disparar(self):
        self.balas_nave.append(Bala(self.screen, velocidad_balas))
        bala_actual_para_disparar = self.balas_nave[-1]  # Obtener la última bala disparada
        balas_actualizadas.append(bala_actual_para_disparar.disparar_nave (self))
        return balas_actualizadas

class Enemigo:
    def __init__(self,tamaño:int ,vida:int) -> None:
        self.imagen = pygame.image.load("SEGUNDO PARCIAL\Galaxy\Imgs\Enemys.png")
        self.nave_escalada = pygame.transform.scale(self.imagen,(tamaño, tamaño))
        self.movimiento = 2
        self.vida = vida
        self.rect = self.nave_escalada.get_rect()
        self.rect.x = 0
        self.rect.y = 20

    def dibujar(self, screen):
        self.dibujo = self.nave_escalada
        screen.blit(self.dibujo, self.rect)

    def moverse_derecha(self,flag):
        if self.rect.x >= ANCHO_VENTANA - 90: #Si llego al final de la ventana que cambie de direccion
            flag = "izquierda"
            self.rect.x = self.rect.x - self.movimiento
        else:
            self.rect.x = self.rect.x + self.movimiento
        return flag

    def moverse_izquierda(self,flag):
        if self.rect.x < 0:
            flag = "derecha"
            self.rect.x = self.rect.x + self.movimiento
        else:
            self.rect.x = self.rect.x - self.movimiento
        return flag

    def moverse(self,flag):
        if flag == "izquierda":
            flag = self.moverse_izquierda(flag)
        elif flag == "derecha":
            flag = self.moverse_derecha(flag)
        return flag

class Bala:
    def __init__(self,screen, velocidad_balas):
        self.velocidad = velocidad_balas
        self.screen = screen
        self.rectangulo = pygame.Rect(0, 0, 3, 10)
        self.rectangulo.x = 0
        self.rectangulo.y = 0

    def dibujar(self,color):
        pygame.draw.rect(self.screen, (color), self.rectangulo)

    def disparar_nave(self,nave):
        if nave.movimiento == 6:
            reproducir_musica(PATH_DISPAROS,1)
            self.rectangulo.x = nave.rect.x + (nave.rect.width)/2
            self.rectangulo.y = nave.rect.y
            self.rectangulo.y -= self.velocidad
            self.dibujar((255,255,255))
            return self

    def disparar_enemigo(self,enemigo):
        self.rectangulo.x = enemigo.rect.x + (enemigo.rect.width)/2
        self.rectangulo.y = enemigo.rect.y
        self.rectangulo.y += self.velocidad
        self.dibujar((255,0,0))
        return self

class Textos:
    def __init__(self,screen) -> None:
        self.rect = pygame.Rect(0, 0, 0, 0) #Esta seria la caja de texto
        self.screen = screen
        self.fuente_tmr25 = pygame.font.SysFont("Times New Roman", 25)
        self.fuente_ab40 = pygame.font.SysFont("Arial Bold", 40)
        self.fuente_ab50 = pygame.font.SysFont("Arial Bold", 50)
#------Pantalla para ingresar nombre--------
    def score_ingame(self,score):
        img_score = self.fuente_tmr25.render (fr"SCORE: {score}", True, (255,255,255), (0,0,0))
        rect_score = img_score.get_rect()
        rect_score.x = 10
        rect_score.y = 610
        self.screen.blit(img_score, rect_score)

    def tempo(self,tempo):
        img_score = self.fuente_tmr25.render (fr"SEC: {tempo}", True, (255,255,255), (0,0,0))
        rect_score = img_score.get_rect()
        rect_score.x = 340
        rect_score.y = 660
        self.screen.blit(img_score, rect_score)

    def texto_ingresar_nombre(self):
        texto = "Ingrese su nombre"
        superficie_texto = self.fuente_tmr25.render(texto, True, (255, 255, 255))
        self.screen.blit(superficie_texto, (self.rect.centerx - superficie_texto.get_width() // 2,self.screen.get_height() // 2 + 120))

    def texto_input_jugador(self,nombre_jugador):
        nombre_jugador = nombre_jugador.upper() #Pasamos el nombre a mayus
        superficie_texto_jugador = self.fuente_ab50.render(nombre_jugador, True, (255, 255, 255)) #Creamos la superficie del texto
        
        #-------Definimos las dimensiones de la caja de texto--------
        self.rect.width = 250
        self.rect.height = 50
        self.rect.centerx = self.screen.get_width() // 2
        self.rect.y = self.screen.get_height() // 2 + 150

        if superficie_texto_jugador.get_width() > self.rect.width: #Por si el texto es mas grande que la caja, lo ajustamos
            self.rect.width = superficie_texto_jugador.get_width() + 10
            self.rect.centerx = self.screen.get_width() // 2

            #Definimos un limite de superficie a ocupar el texto
            if self.rect.width > 430: 
                nombre_jugador = nombre_jugador [:-1]
                self.rect.width = self.rect.width - 10

        #Definimos las coordenadas y dimensiones del texto
        superficie_texto_jugador = self.fuente_ab50.render(nombre_jugador, True, (255, 255, 255))
        texto_jugador_x = self.rect.centerx - superficie_texto_jugador.get_width() // 2             
        texto_jugador_y = self.rect.y + (self.rect.height - superficie_texto_jugador.get_height()) // 2

        #Dibujamos en la pantalla
        pygame.draw.rect(self.screen, (255,255,255), self.rect, 1)
        self.screen.blit(superficie_texto_jugador, (texto_jugador_x, texto_jugador_y))
        return nombre_jugador
    
    def texto_puntuacion_final(self, score):
        texto = f"PUNTUACION FINAL:"
        superficie_texto = self.fuente_ab50.render(texto, True, (255, 255, 255))
        texto_x = self.screen.get_width() // 2 - superficie_texto.get_width() // 2         
        texto_y = 100

        fuente_score = pygame.font.SysFont("Arial Bold", 130)
        texto_score = f"{score}"
        superficie_texto_score = fuente_score.render(texto_score, True, (255, 255, 255))
        texto_score_x = self.screen.get_width() // 2 - superficie_texto_score.get_width() // 2
        texto_score_y = 150

        self.screen.blit(superficie_texto, (texto_x, texto_y))
        self.screen.blit(superficie_texto_score, (texto_score_x, texto_score_y))

    def pantalla_nombre(self, nombre_jugador,score):
        nombre_jugador = self.texto_input_jugador(nombre_jugador)
        self.texto_ingresar_nombre()
        self.texto_puntuacion_final(score)

        return nombre_jugador
#------Pantalla de stats--------
    def texto_puntajes(self):
        texto = "PUNTUACION HISTORICA"
        superficie_texto = self.fuente_ab50.render(texto, True, (255, 255, 255))
        texto_x = self.screen.get_width() // 2 - superficie_texto.get_width() // 2         
        texto_y = 50
        self.screen.blit(superficie_texto, (texto_x, texto_y))

    def texto_jugadores(self,jugadores):
        texto_nombre_y = 130
        for jugador in jugadores:
            texto = f"{jugador[1]}"
            superficie_texto_nombre = self.fuente_tmr25.render(texto, True, (255, 255, 255))
            texto_nombre_x = self.screen.get_width() // 2 - superficie_texto_nombre.get_width() // 2 - 100
            texto_nombre_y += 40

            texto_score = f"{jugador[2]}"
            superficie_texto_score = self.fuente_ab40.render(texto_score, True, (255, 255, 255))
            texto_score_x = self.screen.get_width() // 2 - superficie_texto_score.get_width() // 2+ 150

            self.screen.blit(superficie_texto_nombre, (texto_nombre_x, texto_nombre_y))
            self.screen.blit(superficie_texto_score, (texto_score_x, texto_nombre_y))

    def pantalla_stats(self,jugadores):
        self.texto_puntajes()
        self.texto_jugadores(jugadores)

class Base_datos:
    def crear(self):
        with sqlite3.connect(PATH_BD) as conexion:
            try:
                sentencia = """create table SCORES 
                                (
                                    id integer primary key autoincrement,
                                    nombre text,
                                    score integer
                                )
                            """
                conexion.execute (sentencia)
            except sqlite3.OperationalError:
                print("La tabla ya existe")

    def agregar(self,nombre, score):
        with sqlite3.connect(PATH_BD) as conexion:
            try:
                conexion.execute ("insert into SCORES(nombre,score) values(?,?)", (nombre, score))
                conexion.commit()
                print("Se cargaron los datos")
            except:
                print ("Error al cargar los datos")
    
    def eliminar_bd(self):
        with sqlite3.connect(PATH_BD) as conexion:
            try:
                conexion.execute("DROP TABLE IF EXISTS SCORES")
                print("Base de datos eliminada exitosamente.")
            except sqlite3.Error as e:
                print(f"Error al eliminar la base de datos: {e}")
    
    def imprimir(self,cant_jugadores):
        with sqlite3.connect(PATH_BD) as conexion:
            try:
                puntuacion = []
                cursor = conexion.execute("SELECT * FROM SCORES ORDER BY score DESC")
                a=0
                for fila in cursor:
                    puntuacion.append(fila)
                    a+=1
                    if a== cant_jugadores:
                        break
                return puntuacion
            except Exception as e:
                print("Error al imprimir la base de datos:", e)

def enemigos_disparar(screen, enemigos:list, reloj, tiempo_disparar_enemigo):
    cant_enemigos_restantes = len (enemigos) - 1
    if cant_enemigos_restantes <= 5:
        tiempo_random = random.randint(100, 2000)
    else:
        tiempo_random = 200
    tiempo_disparar_enemigo += reloj.tick(FPS)
    if cant_enemigos_restantes>=0 and tiempo_disparar_enemigo > tiempo_random:
        enemigo_a_disparar = random.randint(0,cant_enemigos_restantes)
        balas_enemigas.append(Bala(screen, velocidad_balas))
        bala_actual_enemiga_para_disparar = balas_enemigas[-1]  # Obtener la última bala disparada
        balas_enemigas_actualizadas.append(bala_actual_enemiga_para_disparar.disparar_enemigo(enemigos[enemigo_a_disparar])) #Agregamos cada bala a una lista
        
        tiempo_disparar_enemigo = 0

    return balas_enemigas_actualizadas, tiempo_disparar_enemigo