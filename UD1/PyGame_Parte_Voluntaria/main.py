if __name__ == '__main__':
    # Import the pygame module
    import pygame
    # Import random for random numbers
    import random
    import time
    from pygame.locals import *
    import os
    import sqlite3

    # Import pygame.locals for easier access to key coordinates
    # Updated to conform to flake8 and black standards
    from pygame.locals import (
        K_UP,
        K_DOWN,
        K_LEFT,
        K_RIGHT,
        K_ESCAPE,
        K_a,
        K_s,
        K_d,
        K_w,
        KEYDOWN,
        RLEACCEL,
        QUIT
    )
    
    
    #-----------------------------------------Creamos el avion------------------------------------------------------------------------#
    

    # Define a Player object by extending pygame.sprite.Sprite
    # The surface drawn on the screen is now an attribute of 'player'
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()         
            self.surf = pygame.image.load("resources/jet.png").convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect = self.surf.get_rect()

        # Move the sprite based on user keypresses
        def update(self, pressed_keys):
            if pressed_keys[K_w]:
                self.rect.move_ip(0, -5)
                move_up_sound.play()
            if pressed_keys[K_s]:
                self.rect.move_ip(0, 5)
                move_down_sound.play()
            if pressed_keys[K_a]:
                self.rect.move_ip(-5, 0)
            if pressed_keys[K_d]:
                self.rect.move_ip(5, 0)

            # Keep player on the screen
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                
    
    #-------------------------------------Creamos objetos y les damos sus valores----------------------------------------------------------------------------#
    

    # Define the enemy object by extending pygame.sprite.Sprite
    # The surface you draw on the screen is now an attribute of 'enemy'
    class Enemy(pygame.sprite.Sprite):
        
        def __init__(self):
            super(Enemy, self).__init__()
            self.surf = pygame.image.load("resources/missile.png").convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT),
                )
            )
            self.speed = random.randint(2 * nivel, 10 + 3 * nivel)

        # Move the sprite based on speed
        # Remove the sprite when it passes the left edge of the screen
        def update(self):
            self.rect.move_ip(-self.speed, 0)
            if self.rect.right < 0:
                self.kill()
                
    class Cloud(pygame.sprite.Sprite):
        def __init__(self):
            super(Cloud, self).__init__()
            self.surf = pygame.image.load("resources/cloud.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT),
                )
            )
            
            
        def update(self):
            self.rect.move_ip(-5, 0)
            if self.rect.right < 0:
                self.kill()
                
    class Heart(pygame.sprite.Sprite):
            
        def __init__(self):
            super(Heart, self).__init__()
            self.surf = pygame.image.load("resources/heart.png").convert()
            self.surf.set_colorkey((0, 0, 0), RLEACCEL)
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT),
                )
            )
            self.speed = 13

        # Move the sprite based on speed
        # Remove the sprite when it passes the left edge of the screen
        def update(self):
            self.rect.move_ip(-self.speed, 0)
            if self.rect.right < 0:
                self.kill()
        
          
    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()
    
    #---------------------------------------Iniciamos la musica y el juego--------------------------------------------------------------------------#
    
    # Initialitze mixer
    
    pygame.mixer.init()

    # Initialize pygame
    pygame.init()
    
    #-------------------------------------Creacion de variables dentro del juego----------------------------------------------------------------------------#
    
    vidas = 1
    
    puntos = 0
    
    nivel = 1
    
    negro = (0,0,0)
    
    azul = (135, 206, 250)
    
    grisAz = (50,50,100)
    
    enemies_maxspeed = 20
    
    enemies_minspeed = 10
    
    # Define constants for the screen width and height
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    
    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    enemies_spawntime = 100 + (450 - 50 * nivel)
    
    conn = sqlite3.connect('pygame.db')
    
    curs = conn.cursor()
    
    # Instantiate player. Right now, this is just a rectangle.
    player = Player()
    
    
    changetime = True
    
    screen_color = azul
    
    color_Ne = negro
    color_Az = azul
    color_GrAz = grisAz
    

    # Create groups to hold enemy sprites and all sprites
    # - enemies is used for collision detection and position updates
    # - all_sprites is used for rendering
    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    corazon = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    
    sql = "SELECT MAX(puntuacion) FROM ranking;"

    cursor = conn.cursor()
    cursor.execute(sql)

    maxpuntuacion = cursor.fetchall()
    
    menu = True
    end = True
    
    main_font = pygame.font.SysFont("comicsans",30)
    
    #---------------------------------------Configuracion de Sonido--------------------------------------------------------------------------#
    
    move_up_sound = pygame.mixer.Sound("resources/Rising_putter.ogg")
    move_down_sound = pygame.mixer.Sound("resources/Falling_putter.ogg")
    collision_sound = pygame.mixer.Sound("resources/Collision.ogg")
    collision_sound.set_volume(2)
    
    pygame.mixer.music.load("resources/Apoxode_-_Electric_1.ogg")
    pygame.mixer.music.play(loops=-1)
    
    #-----------------------------------------Creamos los eventos------------------------------------------------------------------------#

    # Create a custom event for adding a new enemy
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, enemies_spawntime)
    
    # Create a custom event for adding a new cloud
    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 1000)
    
    DiaNit = pygame.USEREVENT + 3
    pygame.time.set_timer(DiaNit, 18000)
    
    CORAZON = pygame.USEREVENT + 4
    pygame.time.set_timer(CORAZON, 10000)

    #--------------------------------------Menu Inicial---------------------------------------------------------------------------#

    #Menu intro
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        screen.fill((135, 206, 250))
        
        menu_title = main_font.render("BIENVEIDO A MI PYGAME", 1, (0,0,0))
        screen.blit(menu_title,(285, 200))
        
        intro_label = main_font.render("Pulsa P para empezar", 1, (0,0,0))
        screen.blit(intro_label,(300, 350))
        
        menu_ranking = main_font.render("Mejor Puntuacion", 1, (0,0,0))
        screen.blit(menu_ranking,(50, 150))
        
        menu2_puntuacion = main_font.render(str(maxpuntuacion[0][0]), 1, (0,0,0))
        screen.blit(menu2_puntuacion,(50, 170))
        
        
        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_p]:
            menu = False
        pygame.display.update()
        
    #-----------------------------------Bucle del Juego------------------------------------------------------------------------------#

    # Variable to keep the main loop running
    running = True

    # Main loop
    while running:
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    collision_sound.play()
                    running = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                collision_sound.play()
                running = False
            # Add a new enemy?
            elif event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
                
            elif event.type == ADDCLOUD:
                # Create the new cloud and add it to sprite groups
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)
            
            elif event.type == DiaNit:
                # Change background color
                if changetime == True:
                    screen_color = color_GrAz
                    changetime = False
                else:
                    screen_color = color_Az
                    changetime = True
            
            elif event.type == CORAZON:
                # Create the new heart and add it to sprite groups
                new_corazon = Heart()
                corazon.add(new_corazon)
                all_sprites.add(new_corazon)
        
        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        
        #------------------------------Refrescamos los objetos y listas------------------------------#
        
        player.update(pressed_keys)

        # Update enemy position
        enemies.update()
        
        # Update clouds position
        clouds.update()
        
        corazon.update()

        # Update the player sprite based on user keypresses
        player.update(pressed_keys)

        # Fill the screen with blue
        screen.fill((screen_color))

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
            
        #----------------------Comprovamos los choques de objetos para darle funcionalidades------------------------#
        
        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollide(player, enemies, True):
            # If so, then remove the player and stop the loop
            collision_sound.play()
            vidas -= 1
            if vidas <= 0:
                player.kill()
                running = False
            
        if pygame.sprite.spritecollide(player, corazon, True):
            # If so, then remove the player and stop the loop
            collision_sound.play()    
            vidas+=1
            for i in corazon:
                i.kill()
            
        #-----------------------Bucle para la puntuacion del juego + el sistema de niveles----------------------------#
        
        for x in enemies:
            if x.rect.right < 10:
                puntos += 10
                if puntos%500 == 0:
                    nivel += 1
                    
                    
        #-----------------------Texto por Pantalla---------------------------------------------------------------------------#
                    
 
        fuente = pygame.font.Font(None, 35)
        
        mensaje = fuente.render("Score : "+str(puntos),1,(0, 0, 0))
        screen.blit(mensaje, (15, 0))
        
        mensaje = fuente.render("Nivel : "+str(nivel),1,(0, 0, 0))
        screen.blit(mensaje, (15, 30))
        
        mensaje = fuente.render("Vidas : "+str(vidas),1,(0, 0, 0))
        screen.blit(mensaje, (15, 530))
        
        ayuda_velocidad = 500
        siguiente_nivel = 2

        # Update the display
        pygame.display.flip()

        clock.tick(60)
        
        
    #----------------------------------Creamos la tabla y insertamos la puntuacion-------------------------------------------------------------------------------#
    
        
    curs.execute("create table if not exists ranking(puntuacion int)")
    
    curs.execute("insert into ranking values ("+str(puntos)+")")
    
    conn.commit()
    
    #----------------------------------------Menu Final-------------------------------------------------------------------------#
        
    menu_final = True
    menu_final_salir = True
        
    main2_font = pygame.font.SysFont("comicsans",30)
    
    #Menu final
    while menu_final:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        screen.fill((50, 50, 100))
            
        menu2_title = main2_font.render("HAS MUERTO", 1, (0,0,0))
        screen.blit(menu2_title,(285, 200))
            
        intro2_label = main2_font.render("Pulsa Q para salir", 1, (0,0,0))
        screen.blit(intro2_label,(300, 350))
            
        menu2_ranking = main2_font.render("Tu Puntuacion", 1, (0,0,0))
        screen.blit(menu2_ranking,(50, 150))
        
        if puntos > maxpuntuacion[0][0]:
        
            menu2_puntuacion = main2_font.render(str(puntos), 1, (0,0,0))
            screen.blit(menu2_puntuacion,(50, 170))
            
            menu2_record = main2_font.render("Enhorabuena has superado el record", 1, (0,0,0))
            screen.blit(menu2_record,(300, 100))
        
        else:
            
            menu2_puntuacion = main2_font.render(str(puntos), 1, (0,0,0))
            screen.blit(menu2_puntuacion,(50, 170))
        
            
        tecla2 = pygame.key.get_pressed()

        if tecla2[pygame.K_q]:
            menu_final = False
            
            
        pygame.display.update()
        
    #---------------------------------Cerramos el juego/musica--------------------------------------------------------------------------------#

    conn.close()
        
    pygame.mixer.music.stop()
    pygame.mixer.quit()