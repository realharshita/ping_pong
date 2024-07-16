import tkinter as tk

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
PAD_WIDTH = 10
PAD_HEIGHT = 80
BALL_SIZE = 20
BALL_SPEED = 5  # Initial speed of the ball

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
    global ball_start_x, ball_start_y, ball_dx, ball_dy
    
    canvas.move(ball, ball_dx, ball_dy)
    
    ball_pos = canvas.coords(ball)
    ball_left = ball_pos[0]
    ball_top = ball_pos[1]
    ball_right = ball_pos[2]
    ball_bottom = ball_pos[3]
    
    if ball_top <= 0 or ball_bottom >= CANVAS_HEIGHT:
        ball_dy = -ball_dy
    
    if canvas.coords(ball)[2] >= canvas.coords(paddle2)[0] and canvas.coords(ball)[3] <= canvas.coords(paddle2)[3] and canvas.coords(ball)[1] >= canvas.coords(paddle2)[1]:
        canvas.move(ball, ball_dx, ball_dy)

def move_paddle(event):
    if event.keysym == "w":
        canvas.move(paddle1, 0, -20)
    elif event.keysym == "s":
        canvas.move(paddle1, 0, 20)
    elif event.keysym == "Up":
        canvas.move(paddle2, 0, -20)
    elif event.keysym == "Down":
        canvas.move(paddle2, 0, 20)

canvas.bind_all("<KeyPress-w>", move_paddle)
canvas.bind_all("<KeyPress-s>", move_paddle)
canvas.bind_all("<KeyPress-Up>", move_paddle)
canvas.bind_all("<KeyPress-Down>", move_paddle)

def game_loop():
    update_ball_position()
    window.after(30, game_loop)

game_loop()
window.mainloop()
