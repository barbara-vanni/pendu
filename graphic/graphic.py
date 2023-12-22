import pygame
import json
import sys
import button

pygame.init()
clock = pygame.time.Clock()

#create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hangman")

#game variables
running = True
game_paused = False
menu_state = "main"

#define fonts
font = pygame.font.SysFont("impact", 80)
base_font = pygame.font.SysFont("impact", 32)
user_text = '' 

#create rectangle
input_rect = pygame.Rect(20,20,140,52)
score_rect = pygame.Rect(20,20,500,500)

# color when input box is cliked
color_active = pygame.Color('green')

# color of input box
color_passive = pygame.Color('red')
color = color_passive
# for the inputbox
active = False

# colours
TEXT_COL = (255, 255, 255)

#load button images
resume_img = pygame.image.load("assets/button_resume.png").convert_alpha()
options_img = pygame.image.load("assets/button_options.png").convert_alpha()
quit_img = pygame.image.load("assets/button_quit.png").convert_alpha()
diff_facile_img = pygame.image.load("assets/Flamme_1.png").convert_alpha()
diff_moyen_img = pygame.image.load("assets/Flamme_1.png").convert_alpha()
diff_difficile_img = pygame.image.load("assets/Flamme_1.png").convert_alpha()
video_img = pygame.image.load('assets/button_video.png').convert_alpha()
audio_img = pygame.image.load('assets/button_audio.png').convert_alpha()
keys_img = pygame.image.load('assets/button_keys.png').convert_alpha()
back_img = pygame.image.load('assets/button_back.png').convert_alpha()

#create button instances
# en cliquant sur le bouton option => niveau de difficulté, score !
resume_button = button.Button(304, 125, resume_img, 1)
options_button = button.Button(297, 250, options_img, 1)
quit_button = button.Button(304, 375, quit_img, 1)
facile_button = button.Button(336, 75, diff_facile_img, 1)
moyen_button = button.Button(336, 175, diff_moyen_img, 1)
difficile_button = button.Button(336, 350, diff_difficile_img, 1)
video_button = button.Button(226, 75, video_img, 1)
audio_button = button.Button(225, 200, audio_img, 1)
keys_button = button.Button(246, 325, keys_img, 1)
back_button = button.Button(332, 450, back_img, 1)



def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def render_menu():
    global running, menu_state, state
    if game_paused == True :
        draw_text("Press SPACE", font, TEXT_COL, 160, 250)
    if resume_button.draw(screen):
        state = difficulty_menu
    if options_button.draw(screen):
        state = score_menu
    if quit_button.draw(screen):
        running = False
    return render_menu

def score_menu():
    global state
    pygame.draw.rect(screen, "white", score_rect)
    
    # Get player data from the JSON file
    players_data = charge_data()

    # Check if there is any player data
    if isinstance(players_data, list):
        # Initialize vertical offset
        vertical_offset = 10

        for player in players_data:
            if isinstance(player, dict):
                nom_joueur = player.get("nom", "")
                points_joueur = player.get("points", 0)

                # Display player information in the score menu
                text_surface = base_font.render(f"{nom_joueur} _-_-_-_-_-_-_ Pts: {points_joueur}", True, (0, 0, 0))
                screen.blit(text_surface, (score_rect.x + 10, score_rect.y + vertical_offset))

                vertical_offset += text_surface.get_height() + 5 

    # Draw back button
    if back_button.draw(screen):
        state = render_menu

    return score_menu





def difficulty_menu():
    global state  
    input_box_state()
    facile_button.draw(screen)
    moyen_button.draw(screen)
    difficile_button.draw(screen)
    if back_button.draw(screen):
        state = render_menu
    return difficulty_menu

state = render_menu 


def save_data(nom, points):
    try:
        with open("donnees_joueurs.json", "r") as fichier:
            data = json.load(fichier)
    except FileNotFoundError:
        # If file doesn't exist, create an empty list
        data = {}

    data.append({"nom": nom, "points": points} )

    with open("donnees_joueurs.json", "w") as fichier:
        json.dump(data, fichier, indent=2, separators=(',', ': '))
        fichier.write('\n')


def charge_data():
    try:
        with open("donnees_joueurs.json", "r") as fichier:
            data = json.load(fichier)
            # print("Loaded data:", data)  
            return data
    except FileNotFoundError:
        return None

    
def score_player():
    nom_joueur, points_joueur = charge_data()
    
    

def input_box_state():
    global user_text  
    if active:
        color = color_active
    else:
        color = color_passive

    # draw rectangle for input box
    pygame.draw.rect(screen, color, input_rect)
    text_surface = base_font.render(user_text, True, (255, 255, 255))
    # render
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    # set field for the text so it cannot get outside of the box
    input_rect.w = max(100, text_surface.get_width() + 10)

    return user_text


while running:
    screen.fill((25,25,112))
    state()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    # Save the entered name to the JSON file when Enter key is pressed
                    save_data(user_text, 0)  
                else:
                    user_text += event.unicode
                    if event.key == pygame.K_SPACE:
                        game_paused = True
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
