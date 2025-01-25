import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
TILE_MARGIN = 10
BACKGROUND_COLOR = (255, 255, 255)  # White background
DARK_BACKGROUND_COLOR = (0, 0, 0)  # Black background for dark mode
TILE_COLORS = {
    0: (204, 192, 179),  # Light grey
    2: (238, 228, 218),  # Light beige
    4: (237, 224, 200),  # Beige
    8: (242, 177, 121),  # Light orange
    16: (245, 149, 99),  # Orange
    32: (246, 124, 95),  # Dark orange
    64: (246, 94, 59),   # Red-orange
    128: (237, 207, 114),# Light yellow
    256: (237, 204, 97), # Yellow
    512: (237, 200, 80), # Dark yellow
    1024: (237, 197, 63),# Light gold
    2048: (237, 194, 46),# Gold
}
DARK_TILE_COLORS = {
    0: (60, 58, 50),     # Dark grey for empty tiles
    2: (255, 189, 0),    # Yellow
    4: (255, 204, 51),   # Light yellow
    8: (255, 219, 102),  # Lighter yellow
    16: (255, 234, 153), # Even lighter yellow
    32: (255, 249, 204), # Very light yellow
    64: (255, 255, 255), # White
    128: (255, 189, 0),  # Yellow
    256: (255, 204, 51), # Light yellow
    512: (255, 219, 102),# Lighter yellow
    1024: (255, 234, 153),# Even lighter yellow
    2048: (255, 249, 204),# Very light yellow
}

# Initialize screen
screen = pygame.display.set_mode((600, 720))
pygame.display.set_caption('2048')

# Font
font = pygame.font.SysFont("Georgia", 55)
score_font = pygame.font.SysFont("Papyrus", 50)  
menu_font = pygame.font.SysFont("Consolas", 75)
select_font = pygame.font.SysFont("Comic Sans MS", 55)

# Load icons
moon_icon = pygame.image.load('moon_icon.png')
sun_icon = pygame.image.load('sun_icon.png')

# Function to draw the game board and score
def draw_board(board, score, tile_size, dark_mode):
    screen.fill(DARK_BACKGROUND_COLOR if dark_mode else BACKGROUND_COLOR)
    for row in range(len(board)):
        for col in range(len(board[0])):
            value = board[row][col]
            color = DARK_TILE_COLORS.get(value, (255, 189, 0)) if dark_mode else TILE_COLORS.get(value, (60, 58, 50))
            rect = pygame.Rect(
                col * (tile_size + TILE_MARGIN) + TILE_MARGIN,
                row * (tile_size + TILE_MARGIN) + TILE_MARGIN + 100,
                tile_size,
                tile_size
            )
            pygame.draw.rect(screen, color, rect, border_radius=5)
            if value != 0:
                text = font.render(str(value), True, (0, 0, 0) if dark_mode else (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
    
    # Draw score
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255) if dark_mode else (0, 0, 0))
    score_rect = score_text.get_rect(center=(300, 50))
    screen.blit(score_text, score_rect)
    
    # Draw dark mode button
    button_color = (255, 255, 255) if dark_mode else (0, 0, 0)
    button_rect = pygame.Rect(550, 10, 40, 40)
    pygame.draw.ellipse(screen, button_color, button_rect)
    icon = sun_icon if dark_mode else moon_icon
    icon = pygame.transform.scale(icon, (30, 30))
    screen.blit(icon, icon.get_rect(center=button_rect.center))
    
    pygame.display.flip()
    return button_rect

# Function to move tiles left and merge them
def move_left(board):
    new_board = []
    score = 0
    for row in range(len(board)):
        new_row = [i for i in board[row] if i != 0]
        new_row += [0] * (len(board) - len(new_row))
        for i in range(len(board) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                score += new_row[i]
                new_row[i + 1] = 0
        new_row = [i for i in new_row if i != 0]
        new_row += [0] * (len(board) - len(new_row))
        new_board.append(new_row)
    return new_board, score

# Function to rotate the board
def rotate_board(board, times=1):
    for _ in range(times):
        board = [list(row) for row in zip(*board[::-1])]
    return board

# Function to add a new tile to the board
def add_new_tile(board):
    empty_tiles = [(r, c) for r in range(len(board)) for c in range(len(board[0])) if board[r][c] == 0]
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        board[r][c] = 2 if random.random() < 0.9 else 4

# Function to check if the game is over
def check_game_over(board):
    for row in board:
        if 0 in row:
            return False
    for row in board:
        for i in range(len(board) - 1):
            if row[i] == row[i + 1]:
                return False
    for col in range(len(board)):
        for row in range(len(board) - 1):
            if board[row][col] == board[row + 1][col]:
                return False
    return True

# Function to check if the player has won
def check_win(board):
    for row in board:
        if 2048 in row:
            return True
    return False

# Function to display the game over screen
def game_over_screen(score, dark_mode):
    screen.fill(DARK_BACKGROUND_COLOR if dark_mode else BACKGROUND_COLOR)
    game_over_text = menu_font.render("Game Over", True, (255, 255, 255) if dark_mode else (0, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(300, 310))
    score_text = score_font.render(f"Final Score: {score}", True, (255, 255, 255) if dark_mode else (0, 0, 0))
    score_rect = score_text.get_rect(center=(300, 410))
    restart_text = score_font.render("Press R to Restart", True, (255, 255, 255) if dark_mode else (0, 0, 0))
    restart_rect = restart_text.get_rect(center=(300, 510))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                    return

# Function to display the main menu and select the level
def main_menu(dark_mode):
    levels = [("4x4", 4), ("5x5", 5), ("6x6", 6)]
    selected = 0

    while True:
        screen.fill(DARK_BACKGROUND_COLOR if dark_mode else BACKGROUND_COLOR)
        title_text = menu_font.render("2048", True, (255, 255, 255) if dark_mode else (0, 0, 0))
        title_rect = title_text.get_rect(center=(300, 100))
        screen.blit(title_text, title_rect)

        select_text = select_font.render("Select Level", True, (255, 255, 255) if dark_mode else (0, 0, 0))
        select_rect = select_text.get_rect(center=(300, 200))
        screen.blit(select_text, select_rect)

        # Draw dark mode button on main menu
        button_color = (255, 255, 255) if dark_mode else (0, 0, 0)
        button_rect = pygame.Rect(550, 10, 40, 40)
        pygame.draw.ellipse(screen, button_color, button_rect)
        icon = sun_icon if dark_mode else moon_icon
        icon = pygame.transform.scale(icon, (30, 30))
        screen.blit(icon, icon.get_rect(center=button_rect.center))

        for i, (level_text, _) in enumerate(levels):
            color = (255, 255, 255) if i == selected and dark_mode else (0, 0, 0) if i == selected else (100, 100, 100)
            level_surface = score_font.render(level_text, True, color)
            level_rect = level_surface.get_rect(center=(300, 300 + i * 50))
            screen.blit(level_surface, level_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(levels)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(levels)
                elif event.key == pygame.K_RETURN:
                    return levels[selected][1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_rect.collidepoint(mouse_pos):
                    dark_mode = not dark_mode

# Main game function
def main():
    dark_mode = False
    level = main_menu(dark_mode)
    tile_size = (600 - (level + 1) * TILE_MARGIN) // level
    board = [[0] * level for _ in range(level)]
    add_new_tile(board)
    add_new_tile(board)
    score = 0
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not paused:
                    if event.key == pygame.K_LEFT:
                        board, gained_score = move_left(board)
                        score += gained_score
                        add_new_tile(board)
                    elif event.key == pygame.K_RIGHT:
                        board = rotate_board(board, 2)
                        board, gained_score = move_left(board)
                        board = rotate_board(board, 2)
                        score += gained_score
                        add_new_tile(board)
                    elif event.key == pygame.K_UP:
                        board = rotate_board(board, 3)
                        board, gained_score = move_left(board)
                        board = rotate_board(board, 1)
                        score += gained_score
                        add_new_tile(board)
                    elif event.key == pygame.K_DOWN:
                        board = rotate_board(board, 1)
                        board, gained_score = move_left(board)
                        board = rotate_board(board, 3)
                        score += gained_score
                        add_new_tile(board)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_rect.collidepoint(mouse_pos):
                    dark_mode = not dark_mode

        if not paused:
            button_rect = draw_board(board, score, tile_size, dark_mode)

            if check_win(board):
                game_over_screen(score, dark_mode)
                return

            if check_game_over(board):
                game_over_screen(score, dark_mode)
                return

if __name__ == '__main__':
    main()