from pygame import*

def game(run, finish, win_width, win_height, window_caption, background_img, platform_1_img, platform_2_img, ball_img, FPS, gamemode):
    
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
        def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, direction):
            super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
            self.direction = direction

        def first_player(self):
            keys = key.get_pressed()
            if keys[K_w] and self.rect.y > 40:
                self.rect.y -= self.speed
            if keys[K_s] and self.rect.y < win_height - 100:
                self.rect.y += self.speed

        def second_player(self):
            keys = key.get_pressed()
            if keys[K_UP] and self.rect.y > 40:
                self.rect.y -= self.speed
            if keys[K_DOWN] and self.rect.y < win_height - 100:
                self.rect.y += self.speed

        def computer(self, ball):
            if self.rect.y + self.rect.height / 2 < ball.rect.y + ball.rect.height / 2:
                self.rect.y += self.speed
            elif self.rect.y + self.rect.height / 2 > ball.rect.y + ball.rect.height / 2:
                self.rect.y -= self.speed

    class Ball(GameSprite):
        def __init__(self, player_image, player_x, player_y, size_x, size_y, speed_x, speed_y, player_speed):
            super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
            self.speed_x = speed_x
            self.speed_y = speed_y

        def update(self):
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            if self.rect.y > win_height - 50 or self.rect.y < 0:
                self.speed_y *= -1

            if self.rect.colliderect(platform_1.rect):
                global score_player_1
                knock_sound.play()
                score_player_1 += 1
                self.speed_x *= -1

            if self.rect.colliderect(platform_2.rect):
                global score_player_2
                knock_sound.play()
                score_player_2 += 1
                self.speed_x *= -1

            if self.rect.colliderect(platform_2_computer.rect):
                knock_sound.play()
                score_player_2 += 1
                self.speed_x *= -1
    
    
    window = display.set_mode((win_width, win_height))
    display.set_caption(window_caption)
    background = transform.scale(image.load(background_img),(win_width, win_height))

    platform_1 = Player(platform_1_img, 0, 50, 1, 1, 10, 0)
    platform_2 = Player(platform_2_img, 640, 50, 1, 1, 10, 1)
    platform_2_computer = Player(platform_2_img, 640, 50, 1, 1, 3, 1)
    ball = Ball(ball_img, 60, 30, 0, 0, 5, 3, 3)
    
    global score_player_1
    score_player_1 = 0
    global score_player_2
    score_player_2 = 0

    font.init()
    font1 = font.SysFont(None, 80)
    font2 = font.SysFont(None, 36)

    game_over = font1.render('GAME OVER', 1, (180, 0, 0))

    mixer.init()
    knock_sound = mixer.Sound('data/Ping Pong Ball Hit Sound Effect.ogg')


    clock = time.Clock()

    while run:

        for e in event.get():
            if e.type == QUIT:
                run = False

        if not finish:

            if ball.rect.x < -70 or ball.rect.x > win_width:
                finish = True
            
            score_player_1_text = font2.render("Player 1 score: " + str(score_player_1), 1, (255, 255, 255))
            score_player_2_text = font2.render("Player 2 score: " + str(score_player_2), 1, (255, 255, 255))
            
            score_computer_text = font2.render("Computer score: " + str(score_player_2), 1, (255, 255, 255))
            score_player_text = font2.render("Player score: " + str(score_player_1), 1, (255, 255, 255))
            
            gamemode_text = font2.render(str(gamemode), 1, (255, 255, 255))

            window.blit(background, (0,0))
            window.blit(gamemode_text, (290, 20))

            platform_1.reset()
            platform_1.first_player()

            if gamemode == 'player':
                window.blit(score_player_1_text, (10, 20))
                window.blit(score_player_2_text, (470, 20))
                platform_2.reset()
                platform_2.second_player()
            
            if gamemode == 'computer':
                window.blit(score_player_text, (10, 20))
                window.blit(score_computer_text, (450, 20))
                platform_2_computer.reset()
                platform_2_computer.computer(ball)

            ball.reset()
            ball.update()
        
        if finish == True:
            window.blit(game_over, (180, 200))

        display.update()
        clock.tick(FPS)


def draw_text(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)


def main_menu(win_width, win_height, background, window_caption):
    font.init()
    running = True
    while running:
        white = (255, 255, 255)
        black = (0, 0, 0)
        display.set_caption(window_caption)
        window = display.set_mode((win_width, win_height))
        window.blit(background, (0,0))

        draw_text("Main menu", font.Font(None, 48), white, window, win_width // 2, win_height // 4)
        # Відображення кнопок
        mouse_pos = mouse.get_pos()
        click = False
        for e in event.get():
            if e.type == QUIT:
                quit()
                break
            
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True
        # Перевірка, чи користувач клікнув на кнопки
        if win_width // 2 - 100 < mouse_pos[0] < win_width // 2 + 100 and win_height // 2 - 50 < mouse_pos[1] < win_height // 2 - 10:
            draw.rect(window, black, (win_width // 2 - 100, win_height // 2 - 50, 200, 40))
            if click:    
                game(run=run, finish=finish, win_width=win_width, win_height=win_height, window_caption=window_caption_computer, background_img=background_img_path, platform_1_img=platform_1_img_path, platform_2_img=platform_2_img_path, ball_img=ball_img_path, FPS=FPS, gamemode='computer')
        else:
            draw.rect(window, white, (win_width // 2 - 100, win_height // 2 - 50, 200, 40), 2)
        draw_text("Play with computer", font.Font(None, 30), white, window, win_width // 2, win_height // 2 - 30)


        if win_width // 2 - 100 < mouse_pos[0] < win_width // 2 + 100 and win_height // 2 + 10 < mouse_pos[1] < win_height // 2 + 50:
            draw.rect(window, black, (win_width // 2 - 100, win_height // 2 + 10, 200, 40))
            if click:
                game(run=run, finish=finish, win_width=win_width, win_height=win_height, window_caption=window_caption_player, background_img=background_img_path, platform_1_img=platform_1_img_path, platform_2_img=platform_2_img_path, ball_img=ball_img_path, FPS=FPS, gamemode='player')
        else:
            draw.rect(window, white, (win_width // 2 - 100, win_height // 2 + 10, 200, 40), 2)
        draw_text("Play with player", font.Font(None, 30), white, window, win_width // 2, win_height // 2 + 30)


        if win_width // 2 - 100 < mouse_pos[0] < win_width // 2 + 100 and win_height // 2 + 70 < mouse_pos[1] < win_height // 2 + 110:
            draw.rect(window, black, (win_width // 2 - 100, win_height // 2 + 70, 200, 40))
            if click:
                quit()
                break

        else:
            draw.rect(window, white, (win_width // 2 - 100, win_height // 2 + 70, 200, 40), 2)
        draw_text("Exit", font.Font(None, 30), white, window, win_width // 2, win_height // 2 + 90)
        display.update()


if __name__ == '__main__':
    run = True
    finish = False
    win_width = 700
    win_height = 500
    window_caption_computer = 'Ping-Pong - Computer'
    window_caption_player = 'Ping-Pong - Player'
    window_menu_caption = 'Ping-Pong - Main Menu'
    background_img_path = 'data/wooden-background.jpg'
    platform_1_img_path = 'data/wooden-rocket-1.png'
    platform_2_img_path = 'data/wooden-rocket-2.png'
    ball_img_path = 'data/ball.png'
    FPS = 60
    background = transform.scale(image.load(background_img_path),(win_width, win_height))
    
    main_menu(win_width, win_height, background, window_menu_caption)
    

    # Ручний запуск
    # game(run, finish, win_width, win_height, window_caption, background_img, platform_1_img, platform_2_img, ball_img, FPS)