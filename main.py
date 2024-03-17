from pygame import*

def main(run, win_width, win_height, window_caption, background_img, FPS):
    
    class GameSprite(sprite.Sprite):
        def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
           super().__init__()
           self.image = transform.scale(image.load(player_image), (65, 65))
           self.speed = player_speed
           self.rect = self.image.get_rect()
           self.rect.x = player_x
           self.rect.y = player_y
        
        def reset(self):
            window.blit(self.image, (self.rect.x, self.rect.y))

    class Player(GameSprite):
        def update(self):
            keys = key.get_pressed()
            if keys[K_UP] and self.rect.y > 5:
                self.rect.y -= self.speed
            if keys[K_DOWN] and self.rect.y < win_height - 80:
                self.rect.y += self.speed 

    
    
    window = display.set_mode((win_width, win_height))
    display.set_caption(window_caption)
    background = transform.scale(image.load(background_img),(win_width, win_height))

    desk1 = Player('test.png', 0, 0, 1, 1, 10)

    clock = time.Clock()

    while run:
        window.blit(background, (0,0))

        for e in event.get():
            if e.type == QUIT:
                run = False

        desk1.reset()
        desk1.update()

        display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    run = True
    win_width = 700
    win_height = 500
    window_caption = 'Ping-Pong'
    background_img = "wooden-background.jpg"
    FPS = 60
    
    main(run, win_width, win_height, window_caption, background_img, FPS)