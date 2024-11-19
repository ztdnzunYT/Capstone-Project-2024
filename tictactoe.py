import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
width = 600
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic Tac Toe")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Board size
board_size = 3

# Cell size
cell_size = width // board_size

# Font for displaying text
font = pygame.font.Font(None, 60)

# Create board
board = [['' for _ in range(board_size)] for _ in range(board_size)]

# Player symbols
player_symbol = 'X'
cpu_symbol = 'O'

# Game state
game_over = False
player_turn = True

# Function to draw the board
def draw_board():
    screen.fill(white)
    for i in range(1, board_size):
        pygame.draw.line(screen, black, (i * cell_size, 0), (i * cell_size, height), 2)
        pygame.draw.line(screen, black, (0, i * cell_size), (width, i * cell_size), 2)

# Function to draw the symbols
def draw_symbols():
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] != '':
                text = font.render(board[row][col], True, black)
                text_rect = text.get_rect(center=((col + 0.5) * cell_size, (row + 0.5) * cell_size))
                screen.blit(text, text_rect)

# Function to check for a winner
def check_win():
    # Check rows
    for row in range(board_size):
        if board[row][0] != '' and board[row][0] == board[row][1] == board[row][2]:
            return board[row][0]

    # Check columns
    for col in range(board_size):
        if board[0][col] != '' and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]

    # Check diagonals
    if board[0][0] != '' and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] != '' and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    # No winner
    return None

# Function to check for a draw
def check_draw():
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] == '':
                return False
    return True

# Function for the CPU's move
def cpu_move():
    global player_turn
    available_moves = []
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] == '':
                available_moves.append((row, col))
    if available_moves:
        move = random.choice(available_moves)
        board[move[0]][move[1]] = cpu_symbol
        player_turn = True

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and player_turn and not game_over:
            # Get mouse position
            pos = pygame.mouse.get_pos()
            # Calculate row and column
            row = pos[1] // cell_size
            col = pos[0] // cell_size
            # Check if cell is empty
            if board[row][col] == '':
                board[row][col] = player_symbol
                player_turn = False
                # Check for win or draw after player's move
                winner = check_win()
                if winner:
                    game_over = True
                    if winner == player_symbol:
                        print("Player wins!")
                    else:
                        print("CPU wins!")
                elif check_draw():
                    game_over = True
                    print("It's a draw!")

    # CPU's turn
    if not player_turn and not game_over:
        cpu_move()
        # Check for win or draw after CPU's move
        winner = check_win()
        if winner:
            game_over = True
            if winner == player_symbol:
                print("Player wins!")
            else:
                print("CPU wins!")
        elif check_draw():
            game_over = True
            print("It's a draw!")

    # Draw the board and symbols
    draw_board()
    draw_symbols()

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()