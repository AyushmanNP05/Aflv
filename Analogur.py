import pygame
import math
from datetime import datetime

pygame.init() # Initialize Pygame
screen = pygame.display.set_mode((1000, 1000)) # Laver en skræm med 1000 x 1000 pixels
screen.fill((77, 73, 69)) # Skræm bliver flydt med en selvvalgt farve
pygame.display.set_caption("En analog ur")

pygame.mixer.music.load('alarm-clock-ticking-6069.mp3')
pygame.mixer_music.play(100000,0,0)

text_font = pygame.font.SysFont("neonlights", 90, bold=False, italic=True)
text_num = pygame.font.SysFont('neonlights', 35, bold=False, italic=True)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

# Make sure the window stays open until the user closes it
run_flag = True
while run_flag is True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_flag = False

# Cikler for uren skiven 
    pygame.draw.circle(screen,(0,0,0),(500,500),(259),width=10)
    pygame.draw.circle(screen,(77, 73, 69),(500,500),(250))
    
#Tekst på skærmen for pynt :)
    draw_text("Analog ur", text_font,(0,0,0),290,145)
    draw_text("1", text_num,(0,0,0),595,305)
    draw_text("2", text_num,(0,0,0),670,373)
    draw_text("3", text_num,(0,0,0),700,485)
    draw_text("4", text_num,(0,0,0),671,594)
    draw_text("5", text_num,(0,0,0),596,667)
    draw_text("6", text_num,(0,0,0),491,697)
    draw_text("7", text_num,(0,0,0),384,668)
    draw_text("8", text_num,(0,0,0),306,593)
    draw_text("9", text_num,(0,0,0),280,484)
    draw_text("10", text_num,(0,0,0),305,373)
    draw_text("11", text_num,(0,0,0),378,306)
    draw_text("12", text_num,(0,0,0),481,275)


# Draw 60 lines evenly spaced around the center (500, 500)
    center_x, center_y = 500, 500
    radius = 250
    line_length = 30
    angle_step = 360 / 12  # 30 degrees between each line

# Hour lines 30 degress from each
    for i in range(12):
        angle = math.radians(i * angle_step)
        end_x = center_x + radius * math.cos(angle)
        end_y = center_y + radius * math.sin(angle)
        kod_x = center_x + 225 * math.cos(angle)  #Så linjer ikke er fra centrum til kanten er cirklen
        kod_y = center_y + 225 * math.sin(angle) 
        pygame.draw.line(screen, (0, 0, 0), (kod_x, kod_y), (end_x, end_y),width=5)


    angle_step = 360 / 60
# Minutes lines 6 degree from each
    for i in range(60):
        angle = math.radians(i * angle_step)
        end_x = (center_x + radius * math.cos(angle))
        end_y = (center_y + radius * math.sin(angle))
        kod_x = (center_x + 235 * math.cos(angle)) 
        kod_y = (center_y + 235 * math.sin(angle))
        pygame.draw.line(screen, (0, 0, 0), (kod_x, kod_y), (end_x, end_y),width=3)


#Time linje funkiton
    def draw_time(angle):
        angle -= 90  # Så den starter fra top altså ved "12:00"
        kod_x = (center_x + 175 * math.cos(math.radians(angle)))
        kod_y = (center_y + 175 * math.sin(math.radians(angle)))
        pygame.draw.line(screen,(0,0,0),(500,500),(kod_x, kod_y),width=7)

#Minut linje funktion
    def draw_minut(angle):
        angle -= 90  # Så den starter fra top altså ved "12:00"
        kod_x = (center_x + 210 * math.cos(math.radians(angle)))
        kod_y = (center_y + 210 * math.sin(math.radians(angle)))
        pygame.draw.line(screen,(0,0,0),(500,500),(kod_x, kod_y),width=5)


#Sekund linje funktion
    def draw_sekund(angle):
        angle -= 90  # Så den starter fra top altså ved "12:00"
        kod_x = (center_x + 225 * math.cos(math.radians(angle)))
        kod_y = (center_y + 225 * math.sin(math.radians(angle)))
        pygame.draw.line(screen,(0,0,0),(500,500),(kod_x, kod_y),width=4)

#Pynt:
    pygame.draw.circle(screen,(0, 0, 0),(500,500),(12)) 

#Jeg henter tid for ligenu fra datetime
    today = datetime.now()
    today_hour = today.hour
    today_min = today.minute
    today_sec = today.second

# Beregnes linjerne;
    second_angle = (today_sec % 60) * 6  
    minute_angle = ((today_min % 60) + today_sec / 60) * 6  
    hour_angle = ((today_hour % 12) + today_min / 60) * 30 

#Time linje:
    draw_time(hour_angle)

# Minut linje:
    draw_minut(minute_angle)

#Sekund linje:
    draw_sekund(second_angle)

    
    

    pygame.time.delay(1000) #En aktion per sekund

    pygame.display.flip() # Refresh the screen so drawing appears 

# Lavet for Mini Projekt 1 : Analog Ur
# Lavet af Ayushman Chaudhary