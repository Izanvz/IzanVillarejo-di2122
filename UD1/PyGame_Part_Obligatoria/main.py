if __name__ == '__main__':
    # Import the pygame module
    import pygame
    # Import random for random numbers
    import random
    import os
    import time

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
            self.speed = random.randint(5, 20)

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
            
            
            
    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()
    
    # Initialitze mixer
    
    pygame.mixer.init()

    # Initialize pygame
    pygame.init()
    
    
    move_up_sound = pygame.mixer.Sound("resources/Rising_putter.ogg")
    move_down_sound = pygame.mixer.Sound("resources/Falling_putter.ogg")
    collision_sound = pygame.mixer.Sound("resources/Collision.ogg")
    collision_sound.set_volume(2)
    
    pygame.mixer.music.load("resources/Apoxode_-_Electric_1.ogg")
    pygame.mixer.music.play(loops=-1)

    # Define constants for the screen width and height
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create a custom event for adding a new enemy
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 250)
    
    # Create a custom event for adding a new cloud
    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 1000)

    # Instantiate player. Right now, this is just a rectangle.
    player = Player()

    # Create groups to hold enemy sprites and all sprites
    # - enemies is used for collision detection and position updates
    # - all_sprites is used for rendering
    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

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
                # Create the new enemy and add it to sprite groups
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)

        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        # Update enemy position
        enemies.update()
        
        # Update clouds position
        clouds.update()

        # Update the player sprite based on user keypresses
        player.update(pressed_keys)

        # Fill the screen with black
        screen.fill((135, 206, 250))

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop the loop
            collision_sound.play()
            time.sleep(0.4)     
            player.kill()
            running = False

        # Update the display
        pygame.display.flip()

        clock.tick(45)
        
pygame.mixer.music.stop()
pygame.mixer.quit()