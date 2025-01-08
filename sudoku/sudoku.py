import pygame
import requests

# Initialising pygame
pygame.init()

# Setting width and height of the window
width, height = 550, 550
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sudoku")

font = pygame.font.Font("freesansbold.ttf", 35)

# Calling the API
response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
s_grid = response.json()['board']
grid_original = [[s_grid[x][y] for y in range(len(s_grid[0]))] for x in range(len(s_grid))]
grid_color = (52, 31, 151)

# Inserting user input
def insert(screen, position):
    i, j = position[1], position[0]  # Row, Column
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if grid_original[i][j] != 0:  # Cannot modify original grid
                    return
                if event.key == pygame.K_0:  # Handle 0 as input
                    s_grid[i][j] = 0
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (j * 50 + 50, i * 50 + 50, 50 - 5, 50 - 5))
                    pygame.display.update()
                    return
                if pygame.K_1 <= event.key <= pygame.K_9:  # Valid input 1-9
                    value = event.key - pygame.K_0
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (j * 50 + 50, i * 50 + 50, 50 - 5, 50 - 5))
                    text = font.render(str(value), True, (0, 0, 0))
                    screen.blit(text, (j * 50 + 65, i * 50 + 55))
                    s_grid[i][j] = value
                    pygame.display.update()
                    return

# Game Loop
running = True
while running:
    screen.fill((255, 255, 255))
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            if 50 <= pos[0] < 500 and 50 <= pos[1] < 500:
                col = (pos[0] - 50) // 50
                row = (pos[1] - 50) // 50
                insert(screen, (col, row))

    # Drawing the grid
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 2
        pygame.draw.line(screen, (0, 0, 0), (50 + i * 50, 50), (50 + i * 50, 500), thickness)
        pygame.draw.line(screen, (0, 0, 0), (50, 50 + i * 50), (500, 50 + i * 50), thickness)

    # Displaying numbers
    for i in range(9):
        for j in range(9):
            if s_grid[i][j] != 0:
                value = font.render(str(s_grid[i][j]), True, grid_color)
                screen.blit(value, (j * 50 + 65, i * 50 + 55))

    pygame.display.update()

pygame.quit()
