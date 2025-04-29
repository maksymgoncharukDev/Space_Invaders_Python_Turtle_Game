import turtle
import time

# ==== ЕКРАН ====
screen = turtle.Screen()
screen.title("Space Invaders")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

# ==== ГРАНИЦІ ====
def draw_border():
    border = turtle.Turtle()
    border.hideturtle()
    border.speed(0)
    border.color("white")
    border.penup()
    border.goto(-380, -280)
    border.pendown()
    for _ in range(2):
        border.forward(760)
        border.left(90)
        border.forward(560)
        border.left(90)
draw_border()

# ==== ГРАВЕЦЬ ====
player = turtle.Turtle()
player.shape("triangle")
player.color("blue")
player.penup()
player.goto(0, -250)
player.setheading(90)
player_speed = 20

# ==== КУЛЯ ====
bullet = turtle.Turtle()
bullet.shape("circle")
bullet.color("yellow")
bullet.shapesize(0.3, 0.3)
bullet.penup()
bullet.hideturtle()
bullet_speed = 25
bullet_state = "ready"

# ==== ПЕРЕШКОДИ ====
def create_barriers():
    barriers_list = []
    for x in [-200, 0, 200]:
        b = turtle.Turtle()
        b.shape("square")
        b.color("green")
        b.shapesize(stretch_wid=2, stretch_len=4)
        b.penup()
        b.goto(x, -180)
        barriers_list.append({"turtle": b, "health": 3})
    return barriers_list
barriers = create_barriers()

# ==== ІНОПЛАНЕТЯНИ ====
def create_aliens(rows=3, cols=6):
    aliens_list = []
    for row in range(rows):
        for col in range(cols):
            a = turtle.Turtle()
            a.shape("turtle")
            a.color("red")
            a.penup()
            a.goto(-250 + col * 80, 180 - row * 50)
            aliens_list.append(a)
    return aliens_list
aliens = create_aliens()
alien_speed = 10

# ==== РАХУНОК ====
score = 0
score_pen = turtle.Turtle()
score_pen.hideturtle()
score_pen.color("white")
score_pen.penup()
score_pen.goto(-370, 260)
score_pen.write(f"Score: {score}", font=("Courier", 14, "normal"))

# ==== GAME OVER ====
game_over_pen = turtle.Turtle()
game_over_pen.hideturtle()
game_over_pen.color("white")

def show_game_over():
    game_over_pen.goto(-100, 0)
    game_over_pen.write("GAME OVER", font=("Courier", 30, "bold"))

# ==== РУХ ГРАВЦЯ ====
def move_left():
    x = player.xcor()
    if x > -350:
        player.setx(x - player_speed)

def move_right():
    x = player.xcor()
    if x < 350:
        player.setx(x + player_speed)

# ==== ВОГОНЬ ====
def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(player.xcor(), player.ycor() + 10)
        bullet.showturtle()

# ==== ПЕРЕВІРКА ЗІТКНЕНЬ ====
def is_collision(t1, t2):
    return t1.distance(t2) < 20

# ==== КЛАВІШІ ====
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")

# ==== ОСНОВНИЙ ЦИКЛ ====
game_over = False
last_alien_move = time.time()

while not game_over:
    screen.update()

    # Рух кулі
    if bullet_state == "fire":
        bullet.sety(bullet.ycor() + bullet_speed)
        if bullet.ycor() > 275:
            bullet.hideturtle()
            bullet_state = "ready"

    # Перевірка влучань у прибульців
    for alien in aliens[:]:
        if is_collision(bullet, alien):
            bullet.hideturtle()
            bullet_state = "ready"
            alien.goto(1000, 1000)
            aliens.remove(alien)
            score += 10
            score_pen.clear()
            score_pen.write(f"Score: {score}", font=("Courier", 14, "normal"))

    # Перевірка влучання кулі в бар'єр
    for barrier in barriers[:]:
        b = barrier["turtle"]
        if is_collision(bullet, b):
            bullet.hideturtle()
            bullet_state = "ready"
            barrier["health"] -= 1
            if barrier["health"] == 2:
                b.color("yellow")
            elif barrier["health"] == 1:
                b.color("orange")
            elif barrier["health"] <= 0:
                b.goto(1000, 1000)
                barriers.remove(barrier)

    # Рух прибульців
    if time.time() - last_alien_move > 1:
        last_alien_move = time.time()
        for alien in aliens:
            alien.setx(alien.xcor() + alien_speed)
        if any(a.xcor() > 350 or a.xcor() < -350 for a in aliens):
            alien_speed *= -1
            for a in aliens:
                a.sety(a.ycor() - 30)

    # Програш
    for alien in aliens:
        if is_collision(alien, player) or alien.ycor() <= -250:
            show_game_over()
            game_over = True

        # Прибульці знищують бар'єри
        for barrier in barriers[:]:
            if is_collision(alien, barrier["turtle"]):
                barrier["turtle"].goto(1000, 1000)
                barriers.remove(barrier)

    time.sleep(0.02)

screen.mainloop()
