import tkinter as tk

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
PAD_WIDTH = 10
PAD_HEIGHT = 80
BALL_SIZE = 20
BALL_SPEED = 5

score_player1 = 0
score_player2 = 0
game_over = False

window = tk.Tk()
window.title("Ping Pong Game")

canvas = tk.Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
canvas.pack()

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

ball_start_x = CANVAS_WIDTH // 2
ball_start_y = CANVAS_HEIGHT // 2
ball_dx = BALL_SPEED
ball_dy = BALL_SPEED

def update_ball_position():
    global ball_start_x, ball_start_y, ball_dx, ball_dy, score_player1, score_player2, game_over
    
    if not game_over:
        canvas.move(ball, ball_dx, ball_dy)
        
        ball_pos = canvas.coords(ball)
        ball_left = ball_pos[0]
        ball_top = ball_pos[1]
        ball_right = ball_pos[2]
        ball_bottom = ball_pos[3]
        
        if ball_top <= 0 or ball_bottom >= CANVAS_HEIGHT:
            ball_dy = -ball_dy
        
        if ball_left <= PAD_WIDTH:
            if canvas.coords(ball)[1] >= canvas.coords(paddle1)[1] and canvas.coords(ball)[3] <= canvas.coords(paddle1)[3]:
                ball_dx = -ball_dx
            else:
                score_player2 += 1
                reset_ball()
        
        elif ball_right >= CANVAS_WIDTH - PAD_WIDTH:
            if canvas.coords(ball)[1] >= canvas.coords(paddle2)[1] and canvas.coords(ball)[3] <= canvas.coords(paddle2)[3]:
                ball_dx = -ball_dx
            else:
                score_player1 += 1
                reset_ball()
    
    if score_player1 >= 5 or score_player2 >= 5:
        game_over = True
        show_game_over()

def reset_ball():
    global ball_start_x, ball_start_y, ball_dx, ball_dy
    
    canvas.coords(ball, ball_start_x - BALL_SIZE // 2, ball_start_y - BALL_SIZE // 2,
                  ball_start_x + BALL_SIZE // 2, ball_start_y + BALL_SIZE // 2)
    ball_dx = -ball_dx

def show_game_over():
    canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, text="GAME OVER", font=("Helvetica", 40), fill="white")
    canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2 + 50, text=f"Player 1: {score_player1}  Player 2: {score_player2}", font=("Helvetica", 20), fill="white")
    canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2 + 100, text="Press 'R' to Restart", font=("Helvetica", 20), fill="white")

def move_paddle(event):
    if event.keysym == "w" and canvas.coords(paddle1)[1] > 0:
        canvas.move(paddle1, 0, -20)
    elif event.keysym == "s" and canvas.coords(paddle1)[3] < CANVAS_HEIGHT:
        canvas.move(paddle1, 0, 20)
    elif event.keysym == "Up" and canvas.coords(paddle2)[1] > 0:
        canvas.move(paddle2, 0, -20)
    elif event.keysym == "Down" and canvas.coords(paddle2)[3] < CANVAS_HEIGHT:
        canvas.move(paddle2, 0, 20)

def restart_game(event):
    global score_player1, score_player2, game_over
    score_player1 = 0
    score_player2 = 0
    game_over = False
    reset_ball()

canvas.bind_all("<KeyPress-w>", move_paddle)
canvas.bind_all("<KeyPress-s>", move_paddle)
canvas.bind_all("<KeyPress-Up>", move_paddle)
canvas.bind_all("<KeyPress-Down>", move_paddle)
canvas.bind_all("<KeyPress-R>", restart_game)

def game_loop():
    update_ball_position()
    if not game_over:
        window.after(30, game_loop)

game_loop()
window.mainloop()
