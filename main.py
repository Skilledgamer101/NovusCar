import pygame
import sys
import random

pygame.init()


screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h




window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Parking Spaces")


rect_width = int(screen_width * 0.9)
rect_height = int(screen_height * 0.9)


rect_x = (screen_width - rect_width) // 2
rect_y = (screen_height - rect_height) // 2


rectangle_height = 60
rectangle_width = 40
rectangle_color = (255, 0, 0)  

border_width = 5

space_width = 100  
space_distance = 30 
space_rows = 5  
space_cols = 8  


vertical_space = 20

font_size = 50
font = pygame.font.Font(None, font_size)

show_message_duration = 3  
start_time = pygame.time.get_ticks()
show_message = True


occupied_values = [[random.choice([0, 1]) for _ in range(space_cols)] for _ in range(space_rows)]



player_height = 20
player_width = 20
player_color = (0, 0, 255)  
player_speed = 5



player_x = rect_x
player_x_initial = rect_x
player_y_initial = rect_y
player_y = rect_y

move_down = True
move_left = False
move_right = True


pos_y = []
pos_x = []




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  

   
    window.fill((0, 0, 0))

   
    if show_message and elapsed_time < show_message_duration:
      
        text_surface = font.render("Generating parking spaces...", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen_width / 2, screen_height / 2))
        window.blit(text_surface, text_rect)
    else:
      
        total_width = space_cols * space_width + (space_cols - 1) * space_distance
        total_height = space_rows * space_width + (space_rows - 1) * space_distance

    
        start_x = rect_x + (rect_width - total_width) // 2
        start_y = rect_y + (rect_height - total_height) // 2

      
        for row in range(space_rows):
            for col in range(space_cols):
                occupied = occupied_values[row][col]
                space_x = start_x + col * (space_width + space_distance)
                space_y = start_y + row * (space_width + space_distance)
                rectangle_x = space_x + space_width // 2 - rectangle_width // 2
                rectangle_y = space_y + space_width // 2 - rectangle_height // 2

              
                pygame.draw.line(window, (255, 255, 255), (space_x, space_y), (space_x, space_y + space_width), 2)
                if occupied == 1:
                    pygame.draw.rect(window, rectangle_color, (rectangle_x, rectangle_y, rectangle_width, rectangle_height))
                    
                pygame.draw.line(window, (255, 255, 255), (space_x + space_width, space_y), (space_x + space_width, space_y + space_width), 2)

            
            start_y += space_width + space_distance + vertical_space
            circle_x = start_x + space_cols * (space_width + space_distance) + space_width // 2
            circle_y = start_y + row * (space_width + space_distance) + space_width // 2
            circle_radius = space_width // 4 
            pos_y.append(circle_y)
            pos_x.append(circle_x)
            if rect_x < circle_x < rect_x + rect_width and rect_y < circle_y < rect_y + rect_height:
                pygame.draw.circle(window, (0, 0, 0), (circle_x, circle_y), circle_radius)
       
        
        pygame.draw.rect(window, player_color, (player_x, player_y, player_width, player_height))
     
        print("Circle Y values: \n", pos_y[0])
        print("Player Position: X = \n", player_x, ", Y =", player_y)
        if move_down:
            player_y += player_speed
        if move_left:
            player_y -= player_speed
        if player_y >= pos_y[0] and move_right:
            player_x += player_speed
            move_down = False
        if player_x >= pos_x[0]:
            move_down = True
            move_right = False
        if player_y >= pos_y[1]:
            player_x -= player_speed
            move_down = False
        if player_x <= player_x_initial:
            move_down = True;
            

        

    pygame.draw.rect(window, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height), border_width)



    pygame.display.flip()
    pygame.time.Clock().tick(60)
