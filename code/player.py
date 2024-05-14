import pygame
from settings import *
from support import import_folder
from weapon import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load(
            '../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0
        self.fram_index = 0
        self.animation_speed = 0.15

        #Weapon
        self.create_attack = create_attack
        self.weapon_index = 2
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.destroy_attack = destroy_attack
        #print(self.weapon)

        # graphics set up
        self.import_player_assets()
        self.status = 'down'

        self.obstacle_sprites = obstacle_sprites

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
        # self.rect.center += self.direction * speed

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'

            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'

            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # attacks
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print('Magic')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox) == True:
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        elif direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if (current_time - self.attack_time) >= self.attack_cooldown:
            self.attacking = False
            self.destroy_attack()

    def import_player_assets(self):
        character_path = '../graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []
                           }
        for animation in self.animations.keys():
            full_character_path = character_path + animation
            self.animations[animation] = import_folder(full_character_path)
            # print(self.animations)

    def get_status(self):
        # idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.x = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'

        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def animate(self):
        animation = self.animations[self.status]

        self.fram_index += self.animation_speed
        if self.fram_index >= len(animation):
            self.fram_index = 0

        self.image = animation[int(self.fram_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.input()
        self.move(self.speed)
        self.cooldowns()
        self.animate()
        self.get_status()
