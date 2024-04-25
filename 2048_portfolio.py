import random
import pygame

grid = [[0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
        ]
empty_squares = []  

def combine_and_compact_left_or_right(direction):
    changed_something = False
    for coloumn in range(4):
        empty_spaces = 0
        most_recent_number = 0
        for row in range(direction[0],direction[1],direction[2]): 

            if grid[row][coloumn] == 0: 
                empty_spaces += 1
                
            else:

                if most_recent_number == grid[row][coloumn] and most_recent_number != 0:
                    append_number = grid[row][coloumn] * 2
                    changed_something = True
                    most_recent_number = append_number

                    if direction[3] == "left":
                        row_to_move_to = row-(1+empty_spaces)
                    else:
                        row_to_move_to = row+(1+empty_spaces)

                    grid[row][coloumn], grid[row_to_move_to][coloumn] = 0, grid[row][coloumn] * 2

                    empty_spaces += 1

                else: 
                    most_recent_number = grid[row][coloumn]
                    if empty_spaces > 0:
                        changed_something = True

                    if direction[3] == "left":
                        grid[row][coloumn], grid[row-empty_spaces][coloumn] = 0, grid[row][coloumn]

                    else:
                        grid[row][coloumn], grid[row+empty_spaces][coloumn] = 0, grid[row][coloumn]

    return changed_something

                    

def combine_and_compact_up_or_down(direction):
    changed_something = False
    for row in range(4):
        empty_spaces = 0
        most_recent_number = 0
        for coloumn in range(direction[0],direction[1],direction[2]): 

            if grid[row][coloumn] == 0: 
                empty_spaces += 1
                
            else:
                if most_recent_number == grid[row][coloumn] and most_recent_number != 0:
                    append_number = grid[row][coloumn] * 2
                    changed_something = True
                    most_recent_number = append_number

                    if direction[3] == "up":
                        coloumn_move_to_number = coloumn-(1+empty_spaces)
                    else:
                        coloumn_move_to_number = coloumn+(1+empty_spaces)

                    grid[row][coloumn], grid[row][coloumn_move_to_number] = 0, grid[row][coloumn] * 2

                    empty_spaces += 1

                else: 
                    most_recent_number = grid[row][coloumn]
                    if empty_spaces > 0:
                        changed_something = True

                    if direction[3] == "up":
                        grid[row][coloumn], grid[row][coloumn-empty_spaces] = 0, grid[row][coloumn]


                    else:
                        grid[row][coloumn], grid[row][coloumn+empty_spaces] = 0, grid[row][coloumn]  


    return changed_something



def spawn_new_block():
    potential_squares = []
    for row in range(0,4):
        for coloumn in range(0,4):
            if grid[row][coloumn] == 0:
                potential_squares.append(f"{row}{coloumn}")
    if random.random() < 0.9:
        block_number = 2
    else:
        block_number = 4
    
    random_square = random.randint(0, len(potential_squares)-1)
    try:
        selected_row = int(potential_squares[random_square][0])
        selected_coloumn = int(potential_squares[random_square][1])
        grid[selected_row][selected_coloumn] = block_number
        place_new_block(selected_row, selected_coloumn, block_number)
    except:
        print("error cant place a block")


def place_new_block(x, y, block_number):
    pygame.time.wait(150)
    pygame.draw.rect(screen, colors_of_numbered_blocks[block_number],
                    pygame.Rect(x_and_y_of_blocks[x],x_and_y_of_blocks[y],110,110),
                                 border_radius=5)
    
    text = font.render(str(block_number), True, "#7B7168")
    textRect = text.get_rect()
    textRect.center = (x_and_y_of_blocks[x] + 55, x_and_y_of_blocks[y] + 55)
    display_surface = screen
    display_surface.blit(text, textRect)
    pygame.display.flip()



def show_all_blocks():
    for i in range(4):
        for j in range(4):
            color = colors_of_numbered_blocks[grid[i][j]]
            if grid[i][j] > 4:
                text_color = "#F9F6F2"
            else:
                text_color = "#7B7168"

            pygame.draw.rect(screen, color,
                        pygame.Rect(x_and_y_of_blocks[i],x_and_y_of_blocks[j],110,110), border_radius=5)
            
            if grid[i][j] != 0:
                if grid[i][j] >= 100 and grid[i][j] < 1000:
                    text = font_for_3_digits.render(str(grid[i][j]), True, text_color)
                elif grid[i][j] > 1000:
                    text = font_for_4_digits.render(str(grid[i][j]), True, text_color)
                else:
                    text = font.render(str(grid[i][j]), True, text_color)

                textRect = text.get_rect()
                textRect.center = (x_and_y_of_blocks[i] + 55,x_and_y_of_blocks[j] + 55)
                screen.blit(text, textRect)





def is_their_a_legal_move():
    comparing_to = []

    for row in range(0,4):
        for coloumn in range(0,4):

            if grid[row][coloumn] == 0:
                return True
            
            current_value = grid[row][coloumn]
            if row != 0:  # above row
                comparing_to.append(grid[row-1][coloumn])
            if row != 3: # beneath row
                comparing_to.append(grid[row+1][coloumn])
            if coloumn != 0: # left coloumn
                comparing_to.append(grid[row][coloumn-1])
            if coloumn != 3: # right coloumnn
                comparing_to.append(grid[row][coloumn+1])

            for i in range(len(comparing_to)):
                if comparing_to[i] == current_value:
                    return True
            comparing_to = []
    return False



pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption('2048')
screen.fill("#BBADA0")  
input_processing = False

x_and_y_of_blocks = [12,134,256,378]
colors_of_numbered_blocks = {0:"#CDC1B4",2:"#EEE4DA", 4:"#EEE1C9", 8:"#F3B27A", 16:"#F69664",32:"#F77C5F",64:"#F7613B",128:"#EDD073",256:"#EDCC62",512:"#EDC950",1024:"#EDC950",2048:"#EDC950",4096:"#EDC950"}
font = pygame.font.Font('freesansbold.ttf', 64)
font_for_3_digits = pygame.font.Font('freesansbold.ttf', 48)
font_for_4_digits = pygame.font.Font('freesansbold.ttf', 32)
key_converter = {4:[0,4,1,"left"],
                22:[3,-1,-1,"down"],
                7:[3,-1,-1,"right"],
                26:[0,4,1,"up"]
                }


for i in range(4):
    for j in range(4):
        color = colors_of_numbered_blocks[grid[i][j]]
        rectangle = pygame.draw.rect(screen, color,
                pygame.Rect(x_and_y_of_blocks[i],x_and_y_of_blocks[j],110,110), border_radius=5)

spawn_new_block()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed().index(1)
                if key == 4 or key == 22 or key == 7 or key == 26:
                    if not input_processing:
                        input_processing = True
                        direction = key_converter[key]
                            

                        if direction[3] == "left" or direction[3] == "right":
                            changed_something = combine_and_compact_left_or_right(direction)
                        else:
                            changed_something = combine_and_compact_up_or_down(direction) 

                        show_all_blocks()

                        key = None
                        direction = None

                        if changed_something == True:
                            spawn_new_block()

                        if is_their_a_legal_move() == False:
                            while True:
                                pygame.time.wait(1000)
                    
                    input_processing = False
                
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()