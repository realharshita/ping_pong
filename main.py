import tkinter as tk
import random

# Constants
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
PAD_WIDTH = 10
PAD_HEIGHT = 80
BALL_SIZE = 20
BALL_SPEED = 5

# Game variables
score_player1 = 0
score_player2 = 0
game_over = False
is_multiplayer = False
ai_difficulty = 5

# Initialize tkinter
window = tk.Tk()
window.title("Ping Pong Game")

# Canvas setup
canvas = tk.Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
canvas.pack()

# Paddles and ball creation
paddle1 = canvas.create_rectangle(50, CANVAS_HEIGHT // 2 - PAD_HEIGHT // 2,
                                  50 + PAD_WIDTH, CANVAS_HEIGHT // 2 + PAD_HEIGHT // 2,
                                  fill="white")
paddle2 = canvas.create_rectangle(CANVAS_WIDTH - 50 - PAD_WIDTH, CANVAS_HEIGHT // 2 - PAD_HEIGHT // 2,
                                  CANVAS_WIDTH - 50, CANVAS_HEIGHT // 2 + PAD_HEIGHT // 2,
                                  fill="white")

ball = canvas.create_oval(CANVAS_WIDTH // 2 - BALL_SIZE // 2, CANVAS_HEIGHT // 2 - BALL_SIZE // 2,
                          CANVAS_WIDTH // 2 + BALL_SIZE // 2, CANVAS_HEIGHT // 2 + BALL_SIZE // 2,
                          fill="white")

center_line = canvas.create_line(CANVAS_WIDTH // 2, 0, CANVAS_WIDTH // 2, CANVAS_HEIGHT, fill="white", dash=(15, 10))

# Ball initial parameters
ball_start_x = CANVAS_WIDTH // 2
ball_start_y = CANVAS_HEIGHT // 2
ball_dx = BALL_SPEED
ball_dy = BALL_SPEED

# Function to update ball position
def update_ball_position():
    global ball_start_x, ball_start_y, ball_dx, ball_dy, score_player1, score_player2, game_over
    
    if not game_over:
        canvas.move(ball, ball_dx, ball_dy)
        
        ball_pos = canvas.coords(ball)
        ball_left = ball_pos[0]
        ball_top = ball_pos[1]
        ball_right = ball_pos[2]
        ball_bottom = ball_pos[3]
        
        # Ball collision with top or bottom walls
        if ball_top <= 0 or ball_bottom >= CANVAS_HEIGHT:
            ball_dy = -ball_dy
        
        # Ball collision with left paddle (player 1)
        if ball_left <= PAD_WIDTH:
            paddle1_pos = canvas.coords(paddle1)
            if paddle1_pos[1] <= ball_bottom and paddle1_pos[3] >= ball_top:
                ball_dx = abs(ball_dx)
            else:
                score_player2 += 1
                reset_ball()
        
        # Ball collision with right paddle (player 2 or AI)
        elif ball_right >= CANVAS_WIDTH - PAD_WIDTH:
            paddle2_pos = canvas.coords(paddle2)
            if paddle2_pos[1] <= ball_bottom and paddle2_pos[3] >= ball_top:
                ball_dx = -abs(ball_dx)
            else:
                score_player1 += 1
                reset_ball()
    
    # Check if game is over (one player reaches 5 points)
    if score_player1 >= 5 or score_player2 >= 5:
        game_over = True
        show_game_over()

# Function to reset the ball position and direction
def reset_ball():
    global ball_start_x, ball_start_y, ball_dx, ball_dy
    
    canvas.coords(ball, ball_start_x - BALL_SIZE // 2, ball_start_y - BALL_SIZE // 2,
                  ball_start_x + BALL_SIZE // 2, ball_start_y + BALL_SIZE // 2)
    ball_dx = random.choice([-BALL_SPEED, BALL_SPEED])
    ball_dy = random.choice([-BALL_SPEED, BALL_SPEED])

# Function to display game over message and options to restart or quit
def show_game_over():
    global is_multiplayer

    canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2 - 50, text="GAME OVER", font=("Helvetica", 40), fill="white")
    canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, text=f"Player 1: {score_player1}  Player 2: {score_player2}", font=("Helvetica", 20), fill="white")
    canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2 + 50, text="Press 'Restart' to Restart or 'Quit' to Quit", font=("Helvetica", 20), fill="white")

# Function to move player 1 paddle (for multiplayer or single player)
def move_paddle(event):
    global is_multiplayer

    if event.keysym == "w" and canvas.coords(paddle1)[1] > 0:
        canvas.move(paddle1, 0, -20)
    elif event.keysym == "s" and canvas.coords(paddle1)[3] < CANVAS_HEIGHT:
        canvas.move(paddle1, 0, 20)

    # Move player 2 paddle (only in multiplayer mode)
    if is_multiplayer:
        if event.keysym == "Up" and canvas.coords(paddle2)[1] > 0:
            canvas.move(paddle2, 0, -20)
        elif event.keysym == "Down" and canvas.coords(paddle2)[3] < CANVAS_HEIGHT:
            canvas.move(paddle2, 0, 20)

# Function to toggle between single player and multiplayer modes
def toggle_multiplayer():
    global is_multiplayer
    is_multiplayer = not is_multiplayer

    # Adjust paddle positions for single or multiplayer
    if is_multiplayer:
        canvas.coords(paddle1, 50, CANVAS_HEIGHT // 2 - PAD_HEIGHT // 2,
                      50 + PAD_WIDTH, CANVAS_HEIGHT // 2 + PAD_HEIGHT // 2)
        canvas.coords(paddle2, CANVAS_WIDTH - 50 - PAD_WIDTH, CANVAS_HEIGHT // 2 - PAD_HEIGHT // 2,
                      CANVAS_WIDTH - 50, CANVAS_HEIGHT // 2 + PAD_HEIGHT // 2)
    else:
        canvas.coords(paddle1, 50, CANVAS_HEIGHT // 4 - PAD_HEIGHT // 2,
                      50 + PAD_WIDTH, CANVAS_HEIGHT // 4 + PAD_HEIGHT // 2)
        canvas.coords(paddle2, CANVAS_WIDTH - 50 - PAD_WIDTH, CANVAS_HEIGHT // 4 * 3 - PAD_HEIGHT // 2,
                      CANVAS_WIDTH - 50, CANVAS_HEIGHT // 4 * 3 + PAD_HEIGHT // 2)

# Function to restart the game
def restart_game():
    global score_player1, score_player2, game_over, ball_dx, ball_dy, ai_difficulty
    score_player1 = 0
    score_player2 = 0
    game_over = False
    ball_dx = BALL_SPEED
    ball_dy = BALL_SPEED
    ai_difficulty = 5
    reset_ball()
    canvas.delete("all")
    canvas.create_line(CANVAS_WIDTH // 2, 0, CANVAS_WIDTH // 2, CANVAS_HEIGHT, fill="white", dash=(15, 10))
    paddle1 = canvas.create_rectangle(50, CANVAS_HEIGHT // 2 - PAD_HEIGHT // 2,
                                      50 + PAD_WIDTH, CANVAS_HEIGHT // 2 + PAD_HEIGHT // 2,
                                      fill="white")
    paddle2 = canvas.create_rectangle(CANVAS_WIDTH - 50 - PAD_WIDTH, CANVAS_HEIGHT // 2 - PAD_HEIGHT // 2,
                                      CANVAS_WIDTH - 50, CANVAS_HEIGHT // 2 + PAD_HEIGHT // 2,
                                      fill="white")
    canvas.bind_all("<KeyPress-w>", move_paddle)
    canvas.bind_all("<KeyPress-s>", move_paddle)
    canvas.bind_all("<KeyPress-Up>", move_paddle)
    canvas.bind_all("<KeyPress-Down>", move_paddle)

# Function to update AI paddle position based on ball movement
def update_ai_paddle():
    paddle2_center = canvas.coords(paddle2)[1] + PAD_HEIGHT // 2
    ball_center = canvas.coords(ball)[1] + BALL_SIZE // 2

    if paddle2_center < ball_center:
        canvas.move(paddle2, 0, ai_difficulty)
    elif paddle2_center > ball_center:
        canvas.move(paddle2, 0, -ai_difficulty)

# Function to increase AI difficulty
def increase_difficulty():
    global ai_difficulty, ball_dx, ball_dy
    ai_difficulty += 1
    ball_dx += 1 if ball_dx > 0 else -1
    ball_dy += 1 if ball_dy > 0 else -1

# Function to quit the game
def quit_game():
    window.destroy()

# Buttons and UI setup
button_frame = tk.Frame(window)
button_frame.pack()

multiplayer_button = tk.Button(button_frame, text="Toggle Multiplayer", command=toggle_multiplayer)
multiplayer_button.grid(row=0, column=0, padx=10, pady=10)

restart_button = tk.Button(button_frame, text="Restart", command=restart_game)
restart_button.grid(row=0, column=1, padx=10, pady=10)

quit_button = tk.Button(button_frame, text="Quit", command=quit_game)
quit_button.grid(row=0, column=2, padx=10, pady=10)

difficulty_button = tk.Button(button_frame, text="Increase Difficulty", command=increase_difficulty)
difficulty_button.grid(row=0, column=3, padx=10, pady=10)

# Initial key bindings
canvas.bind_all("<KeyPress-w>", move_paddle)
canvas.bind_all("<KeyPress-s>", move_paddle)
canvas.bind_all("<KeyPress-Up>", move_paddle)
canvas.bind_all("<KeyPress-Down>", move_paddle)

# Game loop function
def game_loop():
    update_ball_position()
    if not is_multiplayer:
        update_ai_paddle()
    if not game_over:
        window.after(30, game_loop)

# Start the game loop
game_loop()
window.mainloop()
