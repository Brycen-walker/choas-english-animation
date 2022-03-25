import turtle
import time
import random

# window
wn = turtle.Screen()
wn.title("Chaos by brycen")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

def start():
    # ball

    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("circle")
    ball.color("white")
    #change this variable for lines vs no lines
    ball.penup()
    ball.goto(0, 0)

    ball2 = turtle.Turtle()
    ball2.speed(0)
    ball2.shape("circle")
    ball2.color("blue")
    #change this variable for lines vs no lines
    ball2.penup()
    ball2.goto(0, 0)

    ball3 = turtle.Turtle()
    ball3.speed(0)
    ball3.shape("circle")
    ball3.color("pink")
    #change this variable for lines vs no lines
    ball3.penup()
    ball3.goto(0, 0)

    ball4 = turtle.Turtle()
    ball4.speed(0)
    ball4.shape("circle")
    ball4.color("green")
    #change this variable for lines vs no lines
    ball4.penup()
    ball4.goto(0, 0)

    count = 0
    while True:
        random_number = str(random.randint(1000, 2000))
        random_number = int(random_number) / 1982
        ball.dx = random_number
        ball.dy = random_number
        random_number2 = str(random.randint(1000, 2000))
        random_number2 = int(random_number2) / 1912
        ball2.dx = random_number2 * 1
        ball2.dy = random_number2 * -1
        random_number3 = str(random.randint(1000, 2000))
        random_number3 = int(random_number3) / 1982
        ball3.dx = random_number3 * -1
        ball3.dy = random_number3 * 1
        random_number4 = str(random.randint(1000, 2000))
        random_number4 = int(random_number4) / 1979
        ball4.dx = random_number4 * -1
        ball4.dy = random_number4 * -1


        while True:
            random_number = str(random.randint(1, 200))
            wn.update()
            ball.setx(ball.xcor() + ball.dx)
            ball.sety(ball.ycor() + ball.dy)
            #time.sleep(0.05)
            if ball.ycor() > 290:
                ball.sety(290)
                ball.dy *= -1
            if ball.ycor() < -290:
                ball.sety(-290)
                ball.dy *= -1
            if ball.xcor() > 390:
                ball.setx(390)
                ball.dx *= -1
            if ball.xcor() < -390:
                ball.setx(-390)
                ball.dx *= -1

            #wn.update()
            ball2.setx(ball2.xcor() + ball2.dx)
            ball2.sety(ball2.ycor() + ball2.dy)
            # time.sleep(0.05)
            if ball2.ycor() > 290:
                ball2.sety(290)
                ball2.dy *= -1
            if ball2.ycor() < -290:
                ball2.sety(-290)
                ball2.dy *= -1
            if ball2.xcor() > 390:
                ball2.setx(390)
                ball2.dx *= -1
            if ball2.xcor() < -390:
                ball2.setx(-390)
                ball2.dx *= -1
            ball3.setx(ball3.xcor() + ball3.dx)
            ball3.sety(ball3.ycor() + ball3.dy)
            # time.sleep(0.05)
            if ball3.ycor() > 290:
                ball3.sety(290)
                ball3.dy *= -1
            if ball3.ycor() < -290:
                ball3.sety(-290)
                ball3.dy *= -1
            if ball3.xcor() > 390:
                ball3.setx(390)
                ball3.dx *= -1
            if ball3.xcor() < -390:
                ball3.setx(-390)
                ball3.dx *= -1

            ball4.setx(ball4.xcor() + ball4.dx)
            ball4.sety(ball4.ycor() + ball4.dy)
            # time.sleep(0.05)
            if ball4.ycor() > 290:
                ball4.sety(290)
                ball4.dy *= -1
            if ball4.ycor() < -290:
                ball4.sety(-290)
                ball4.dy *= -1
            if ball4.xcor() > 390:
                ball4.setx(390)
                ball4.dx *= -1
            if ball4.xcor() < -390:
                ball4.setx(-390)
                ball4.dx *= -1


#experimental code
'''
        random_number = str(random.randint(1, 200))
        random_number = int(random_number) / 113
        ball.dx = random_number
        ball.dy = random_number

        if count % 3 == 0:
            random_number = str(random.randint(1, 200))
            random_number = int(random_number) / 999999
            ball.dx = random_number
            ball.dy = random_number
        if count % 2 == 0:
            random_number = str(random.randint(1, 200))
            random_number = int(random_number)
            ball.dx = random_number
            ball.dy = random_number

        for i in range(1,1000000000000000000000000):
            ball.dx = .01
            ball.dy = .01
            print(f"{ball.dx} {ball.dy}")
        
        random_number2 = str(random.randint(1, 200))
        wn.update()
        ball2.setx(ball2.xcor() + ball2.dx)
        ball2.sety(ball2.ycor() + ball2.dy)
        # time.sleep(0.05)
        if ball2.ycor() > 290:
            ball2.sety(290)
            ball2.dy *= -1
        if ball2.ycor() < -290:
            ball2.sety(-290)
            ball2.dy *= -1
        if ball2.xcor() > 390:
            ball2.setx(390)
            ball2.dx *= -1
        if ball2.xcor() < -390:
            ball2.setx(-390)
            ball2.dx *= -1
        random_number2 = str(random.randint(1, 200))
        random_number2 = int(random_number2) / 113
        ball2.dx = random_number2
        ball2.dy = random_number2

        if count % 3 == 0:
            random_number2 = str(random.randint(1, 200))
            random_number2 = int(random_number2) / 999999
            ball2.dx = random_number2
            ball2.dy = random_number2
        if count % 2 == 0:
            random_number2 = str(random.randint(1, 200))
            random_number2 = int(random_number2)
            ball2.dx = random_number2
            ball2.dy = random_number2
    
        for i in range(1, 1000000000000000000000000):
            ball2.dx = .01
            ball2.dy = .01
            print(f"{ball2.dx} {ball2.dy}")
            count += 1
        '''
start()

