"""
Agus Teira
Div K
"""

import pygame
from funciones import *
from constantes import *
from objetos import *
from objetos import Enemigo
from objetos import Juego
from objetos import Textos
from objetos import Base_datos

#-----------Variables y constantes----------
juego = Juego(ANCHO_VENTANA, ALTO_VENTANA, PATH_FONDO, PATH_MENU)
screen = juego.iniciar()
fondo_juego = juego.fondear()

reloj = pygame.time.Clock()
tempo = pygame.USEREVENT + 0
pygame.time.set_timer(tempo,1000)


textos = Textos(screen)
bd = Base_datos()
bd.crear()

while running:

    reloj.tick(FPS)
    lista_eventos = pygame.event.get() #Obtener la lista de eventos
    screen.blit(fondo_juego,fondo_juego.get_rect())

#-------------------------------------------------------------MENU-------------------------------------------------------------
    if flag_lugar == "menu":

        stats, play = juego.botones_menu() #Los rects y blits de los botones

        for evento in lista_eventos:
            running = juego.cerrar(evento,running)
            #--------Detectar que quiere hacer el usuario-------
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                #Abrir el juego
                if play.collidepoint(mouse_pos):
                    cant_enemigos = cantidad_enemigos_al_inicio
                    flag_lugar, enemigos, nave, segundero, cancion_juego = juego.jugar(cant_enemigos, vida_enemigos, nave_vida)
                #Abrir la puntuacion historica
                elif stats.collidepoint(mouse_pos):
                    flag_lugar = "stats"
#-------------------------------------------------------------JUEGO------------------------------------------------------------
    elif flag_lugar == "juego":
    #----------TOMA LOS EVENTOS TOCADOS PARA MOVER LA NAVE---------
        for evento in lista_eventos:
            running = juego.cerrar(evento,running)
            keys = pygame.key.get_pressed()
            if evento.type == tempo:
                segundero += 1

                #Si pasaron 15 segundos y seguis vivo se te suma al score la cant de enemigos x10
                if segundero % 15 == 0 and flag_tiempo:
                    nave.score += cant_enemigos * 10
                    flag_tiempo = False
                elif flag_tiempo == False and (not segundero % 15== 0):
                    flag_tiempo = True
            
            disparo_tempo += reloj.tick(FPS) 
            if keys[pygame.K_RIGHT]:
                tiempo_transcurrido = float(nave.actualizar_izquierda())

            elif keys[pygame.K_LEFT]:
                tiempo_transcurrido = float(nave.actualizar_derecha())

            elif keys[pygame.K_UP] and flag_enemigos == True and nave.movimiento == 6 and disparo_tempo>= espera_entre_disparos:
                    balas_actualizadas = nave.disparar()
                    disparo_tempo = 0
                    if nave.score > 0:
                        nave.score -=1 #Se le resta un punto cada vez que dispara

        tiempo_transcurrido += reloj.tick(FPS) 
        if tiempo_transcurrido > 150:
            nave.volver()
    #-------------------DISPARAMOS-------------------------------------------
        if len(balas_actualizadas)>0:
            for bala in balas_actualizadas:
                #Y si no colisiono, que siga avanzado
                if bala.rectangulo.y > 0:
                    bala.rectangulo.y -= bala.velocidad
                
                try:#Si la bala ya se fue de la pantalla, se elimina
                    if bala.rectangulo.y <= 0:
                        balas_actualizadas.remove(bala)
                except:
                    print("Se encontro un error, al eliminar la bala que llego al final de la ventana, se sigue")
                #--------ACA DETECTAMOS LAS COLISIONES-------------------------
                for enemigos_individual in enemigos:
                    if bala.rectangulo.colliderect(enemigos_individual) and flag_enemigos:
                        nave.score += enemigos_individual.vida*10
                        enemigos_individual.vida -=1

                        try:
                            balas_actualizadas.remove(bala)
                        except:
                            print("Se encontro un error, al eliminar la bala que choco, se sigue")
                        
                        #Si la vida del enemigo alcanza 0 se elimina el enemigo
                        if enemigos_individual.vida == 0:
                            enemigos.remove(enemigos_individual)
                            
                            #Si los enemigos son 0, se procede a reestablecer valores de nuevo nivel y limpiar balas
                            if len(enemigos) == 0:
                                balas_actualizadas.clear() # elimina todas las balas que hay
                                tiempo_transcurrido_nuevo_nivel = 0
                                flag_enemigos = False
                
    #------------------ENEMIGOS DISPARAN y DETECCION DE SU COLISION --------------------------

        balas_enemigas_actualizadas, tiempo_disparar_enemigo = enemigos_disparar(screen, enemigos, reloj, tiempo_disparar_enemigo)

        #Recorremos la lista de balas 
        for balas in balas_enemigas_actualizadas:
            #Si se fue fuera de la ventana que se elimine la bala, y si no, que siga bajando
            if balas.rectangulo.y < ALTO_VENTANA:
                balas.rectangulo.y += balas.velocidad 
            elif balas.rectangulo.y >= ALTO_VENTANA:
                balas_enemigas_actualizadas.remove(balas)

            #-----------ACA DETECTAMOS LAS COLISIONES-------------------
            if balas.rectangulo.colliderect(nave):
                nave.vida -= 1
                balas_enemigas_actualizadas.remove(balas)
                if nave.vida == 0:
                    nave.morir(fondo_juego, cancion_juego)
                    flag_lugar = "nombre"

    #--------------------------Cambio de niveles--------------------- 
        tiempo_transcurrido_nuevo_nivel += reloj.tick(FPS)
        if len(enemigos) == 0 and tiempo_transcurrido_nuevo_nivel > tiempo_entre_niveles:
            cant_enemigos += 1
            vida_enemigos = cant_enemigos // 2
            enemigos = crear_enemigos(Enemigo, screen, cant_enemigos, 60, 50, vida_enemigos)
            flag_enemigos = True

    #------------------------------Dibujar---------------------------
        textos.score_ingame(nave.score)#Score
        textos.tempo (segundero)
        nave.health_bar(nave_vida)
        nave.dibujar()

        for enemigo in enemigos:
            flag = enemigo.moverse(flag)
            enemigo.dibujar(screen)

        for balas in balas_enemigas_actualizadas:
            balas.dibujar((255,0,0))

        for bala in balas_actualizadas:
            bala.dibujar((255,255,255))
#----------------------------------------------------INGRESAR NOMBRE------------------------------------------------------------
    elif flag_lugar == "nombre":
        for evento in lista_eventos:
            running = juego.cerrar(evento,running)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    nombre_jugador = nombre_jugador[:-1]
                elif evento.key == pygame.K_RETURN:
                    if len(nombre_jugador) > 0:
                        bd.agregar(nombre_jugador, nave.score)
                        flag_lugar = "stats"
                    else:
                        continue
                else:
                    nombre_jugador += evento.unicode

        nombre_jugador = textos.pantalla_nombre(nombre_jugador,nave.score) 
#------------------------------------------------------MOSTRAR STATS------------------------------------------------------------
    elif flag_lugar == "stats":
        atras = juego.button_atras()

        for evento in lista_eventos:
            running = juego.cerrar(evento,running)
            mouse_pos = pygame.mouse.get_pos()
            #--------Detectar que quiere hacer el usuario-------
            if evento.type == pygame.MOUSEBUTTONDOWN and atras.collidepoint(mouse_pos):
                flag_lugar = "menu"

        jugadores = bd.imprimir(10)
        textos.pantalla_stats(jugadores)

    pygame.display.flip()
