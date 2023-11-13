import time
import random
import pygame

class Object:
    
    def __init__(self, x: int, y: int, vel: int, length: int, width: int, color: tuple) -> None:
        self.x = x
        self.y = y
        self.vel = vel
        self.length = length
        self.width = width
        self.color = color
        self.screen_length = window.get_size()[1]
        self.screen_width = window.get_size()[0]
        self.bgcolor = (0,0,0)

    def right(self) -> None:
        self.x += self.vel
        draw_all()

    def left(self) -> None:
        self.x -= self.vel
        draw_all()

    def up(self) -> None:
        self.y -= self.vel
        draw_all()

    def down(self) -> None:
        self.y += self.vel
        draw_all()

    def warp(self) -> None:

        if self.x >= self.screen_width - self.width:
            self.x, self.y = self.screen_width / 2 - self.width / 2, self.screen_length / 2 - self.length / 2

        elif self.x <= 10:
            self.x, self.y = self.screen_width / 2 - self.width / 2, self.screen_length / 2 - self.length / 2

        elif self.y <= 0:
            self.x, self.y = self.screen_width / 2 - self.width / 2, self.screen_length / 2 - self.length / 2

        elif self.y >= self.screen_length - self.length:          # too down. down is higher value
            self.x, self.y = self.screen_width / 2 - self.width / 2, self.screen_length / 2 - self.length / 2

        draw_all()


pygame.init()

window = pygame.display.set_mode()
pygame.display.set_caption("Autonomous Car")
# user_car is blue, other_cars are red, pedestrian is green
user_car = Object(60, 100, 3, 20, 40, (0, 0, 255))         # all the characteristics of each Car
other_car1 = Object(100, user_car.screen_length - 100, 2, 20, 40, (255, 0, 0))
other_car2 = Object(200, user_car.screen_length - 100, 2, 20, 40, (255, 0, 0))
other_car3 = Object(300, user_car.screen_length - 100, 2, 20, 40, (255, 0, 0))
width = user_car.screen_width
pedestrian = Object(400, user_car.screen_length - 100, 2, 20, 40, (0, 255, 0))

x_center = width // 2
y_center = user_car.screen_length // 2
run = True


def follow(enemy, hero):            # enemy and hero must be objects of the Object class

    if enemy.x < hero.x - 10:
        enemy.right()

    elif enemy.x > hero.x + 10:
        enemy.left()

    elif enemy.y > hero.y + 10:
        enemy.up()

    elif enemy.y < hero.y - 10:
        enemy.down()

def draw_all():
    window.fill(user_car.bgcolor)
    pygame.draw.rect(window, user_car.color, (user_car.x, user_car.y, user_car.length, user_car.width), 2, 6)
    pygame.draw.rect(window, other_car1.color, (other_car1.x, other_car1.y, other_car1.length, other_car1.width), 2, 6)
    pygame.draw.rect(window, other_car2.color, (other_car2.x, other_car2.y, other_car2.length, other_car2.width), 2, 6)
    pygame.draw.rect(window, other_car3.color, (other_car3.x, other_car3.y, other_car3.length, other_car3.width), 2, 6)
    pygame.draw.rect(window, pedestrian.color, (pedestrian.x, pedestrian.y, pedestrian.length, pedestrian.width), 2, 6)
    pygame.display.update()

def set_creator(car):
    car_set, x_set, y_set = set(), set(), set()
    # add each pixel value to set (good for seeing if there is overlap between two cars)
    for i in range(int(car.x), int(car.x + car.length + 1)):
        x_set.add(i)
        for j in range(int(car.y), int(car.y + car.width + 1)):
            y_set.add(j)
            car_set.add((i, j))
    return car_set, x_set, y_set


def check(other_car, user_car):

    global run
    font = pygame.font.Font('CascadiaCode-Light.ttf', 32)
    text8 = font.render('You crashed into a car!', True, (255, 0, 0))
    textRect8 = text8.get_rect()
    textRect8.center = (user_car.screen_width // 2, user_car.screen_length // 2 + 300)
    user_car_set, user_car_x, user_car_y = set_creator(user_car)
    other_car_set, other_car_x, other_car_y = set_creator(other_car)

    if user_car_set.isdisjoint(other_car_set) == False:
        # False means one or more pixels are shared between the two cars
        pygame.mixer.Channel(0).stop()
        pygame.mixer.Channel(2).play(pygame.mixer.Sound('death.mp3'))
        window.blit(text8, textRect8)
        pygame.display.update()
        time.sleep(0.5)
        run = False

    else:
        for x2 in other_car_x:
            for x1 in user_car_x:
                # other car is too close to right of user car AND both have same y-values
                if user_car_y.isdisjoint(other_car_y) == False:
                    if 0 <= (x2 - x1) <= 100:
                        return "left"
                    # too close to left    
                    elif -100 <= (x2 - x1) <= 0:
                        return "right"    

        for y2 in other_car_y:
            for y1 in user_car_y:
                # other car is too close behind of user car AND both have same x-values
                if user_car_x.isdisjoint(other_car_x) == False:
                    if 0 <= (y2 - y1) <= 100:
                        return "up"
                    # too close in front    
                    elif -100 <= (y2 - y1) <= 0:
                        return "down"



def move(other_car, user_car):
    font = pygame.font.Font('CascadiaCode-Light.ttf', 32)
    text9 = font.render('Object close on left', True, (7, 186, 13))
    text10 = font.render('Object close on right', True, (7, 186, 13))
    text11 = font.render('Object close in front', True, (7, 186, 13))
    text12 = font.render('Object close behind', True, (7, 186, 13))


    textRect9 = text9.get_rect()
    textRect10 = text10.get_rect()
    textRect11 = text11.get_rect()
    textRect12 = text12.get_rect()

    textRect9.center = (user_car.screen_width // 2, user_car.screen_length // 2 + 300)
    textRect10.center = (user_car.screen_width // 2, user_car.screen_length // 2 + 300)
    textRect11.center = (user_car.screen_width // 2, user_car.screen_length // 2 + 300)
    textRect12.center = (user_car.screen_width // 2, user_car.screen_length // 2 + 300)
    ticks = pygame.time.get_ticks()

    # NEED TO MOVE LEFT (OTHER CAR IS ON RIGHT)
    if (check(other_car, user_car) == "left"):
        window.blit(text10, textRect10)
        pygame.display.update()
        time.sleep(0.5)
        for i in range(25):
            user_car.left()
        #return "stop"
    elif (check(other_car, user_car) == "right"):
        window.blit(text9, textRect9)
        pygame.display.update()
        time.sleep(0.5)
        for i in range(25):
            user_car.right()
            #time.sleep(?)        
        #return "stop"

    elif (check(other_car, user_car) == "up"):
        window.blit(text12, textRect12)
        pygame.display.update()
        time.sleep(0.5) 
        for i in range(25):
            user_car.up()  
        #return "stop"
    elif (check(other_car, user_car) == "down"):
        window.blit(text11, textRect11)
        pygame.display.update()
        time.sleep(0.5)
        for i in range(25):
            user_car.down()
        #return "stop"
    else:
        
        if 10500 <= ticks <= 12500:
            user_car.right()
            other_car1.right()
            other_car2.right()
            other_car3.right()
            pedestrian.right()
        elif 12500 <= ticks <= 25000:
            user_car.down()
            other_car1.up()
            other_car2.up()
            other_car3.up()
            pedestrian.up()
        elif 25000 <= ticks <= 30000:
            user_car.left()
            other_car1.left()
            other_car2.left()
            other_car3.left()
            pedestrian.left()
        elif 30000 <= ticks <= 35000:
            user_car.up()
            other_car1.down()
            other_car2.down()
            other_car3.down()
            pedestrian.down()
        elif 35000 <= ticks <= 40000:
            user_car.right()
            other_car1.right()
            other_car2.right()
            other_car3.right()
            pedestrian.right()
        elif 40000 <= ticks <= 45000:
            user_car.down()
            other_car1.up()
            other_car2.up()
            other_car3.up()
            pedestrian.up()
        elif 45000 <= ticks <= 50000:
            user_car.left()
            other_car1.left()
            other_car2.left()
            other_car3.left()
            pedestrian.left()
        elif 50000 <= ticks <= 55000:
            user_car.up()
            other_car1.down()
            other_car2.down()
            other_car3.down()
            pedestrian.down()
        if 55000 <= ticks <= 60000:
            user_car.right()
            other_car1.right()
            other_car2.right()
            other_car3.right()
            pedestrian.right()
        elif 60000 <= ticks <= 65000:
            user_car.down()
            other_car1.up()
            other_car2.up()
            other_car3.up()
            pedestrian.up()
        elif 65000 <= ticks <= 70000:
            user_car.left()
            other_car1.left()
            other_car2.left()
            other_car3.left()
            pedestrian.left()
        elif 70000 <= ticks <= 75000:
            user_car.up()
            other_car1.down()
            other_car2.down()
            other_car3.down()
            pedestrian.down()
        elif 75000 <= ticks <= 80000:
            user_car.right()
            other_car1.right()
            other_car2.right()
            other_car3.right()
            pedestrian.right()
        elif 80000 <= ticks <= 85000:
            user_car.down()
            other_car1.up()
            other_car2.up()
            other_car3.up()
            pedestrian.up()
        elif 85000 <= ticks <= 90000:
            user_car.left()
            other_car1.left()
            other_car2.left()
            other_car3.left()
            pedestrian.left()
        elif 90000 <= ticks <= 95000:
            user_car.up()
            other_car1.down()
            other_car2.down()
            other_car3.down()
            pedestrian.down()
        if 95000 <= ticks <= 100000:
            user_car.right()
            other_car1.right()
            other_car2.right()
            other_car3.right()
            pedestrian.right()
        elif 100000 <= ticks <= 105000:
            user_car.down()
            other_car1.up()
            other_car2.up()
            other_car3.up()
            pedestrian.up()
        elif 105000 <= ticks <= 110000:
            user_car.left()
            other_car1.left()
            other_car2.left()
            other_car3.left()
            pedestrian.left()
        elif 110000 <= ticks <= 115000:
            user_car.up()
            other_car1.down()
            other_car2.down()
            other_car3.down()
            pedestrian.down()
        elif 115000 <= ticks <= 120000:
            user_car.right()
            other_car1.right()
            other_car2.right()
            other_car3.right()
            pedestrian.right()
        elif 120000 <= ticks <= 125000:
            user_car.down()
            other_car1.up()
            other_car2.up()
            other_car3.up()
            pedestrian.up()
        elif 125000 <= ticks <= 130000:
            user_car.left()
            other_car1.left()
            other_car2.left()
            other_car3.left()
            pedestrian.left()
        elif 130000 <= ticks <= 135000:
            user_car.up()
            other_car1.down()
            other_car2.down()
            other_car3.down()
            pedestrian.down()
        elif 135000 <= ticks <= 140000:
            user_car.right()
            other_car1.right()
            other_car2.right()
            other_car3.right()
            pedestrian.right()
                      
def main():
    speed = 50
    global run

    pygame.mixer.Channel(0).play(pygame.mixer.Sound('prismatic.mp3'))

    font = pygame.font.Font('CascadiaCode-Light.ttf', 32)
    text1 = font.render('The blue car is autonomous.', True, (255, 255, 255))
    text2 = font.render('It will avoid the other cars (red) and pedestrians (green).', True, (255, 255, 255))
    text3 = font.render('It will provide warnings when it comes too close to cars or pedestrians.', True, (255, 255, 255))
    text4 = font.render('Any object that goes outside the screen will be placed back in the center.', True, (255, 255, 255))
    text5 = font.render('Start!', True, (255, 255, 255))

    textRect1 = text1.get_rect()
    textRect2 = text2.get_rect()
    textRect3 = text3.get_rect()
    textRect4 = text4.get_rect()
    textRect5 = text5.get_rect()
    textRect1.center = textRect2.center = textRect3.center = textRect4.center = textRect5.center = (user_car.screen_width // 2, user_car.screen_length // 2 + 300)
    stop = False
    while run:
        ticks = pygame.time.get_ticks()
        print(ticks)
        pygame.time.delay(speed)
        draw_all()
        # user_car has warp (bounce) AND move (check) which has default move (up)
        # other objects only have warp (bounce) which has default move (right)
        user_car.warp()        
        other_car1.warp()
        other_car2.warp()
        other_car3.warp()
        pedestrian.warp()

        move(other_car1, user_car)
        move(other_car2, user_car)
        move(other_car3, user_car)
        move(pedestrian, user_car)

        # follow(other_car1, user_car)
        # follow(other_car2, user_car)
        # follow(other_car3, user_car)
        # follow(pedestrian, user_car)
                
        while ticks <= 8000:
            if ticks <= 2000:
                draw_all()
                window.blit(text1, textRect1)
                pygame.display.update()
                time.sleep(2)
                ticks = pygame.time.get_ticks()
            if 2000 < ticks <= 4000:
                draw_all()
                window.blit(text2, textRect2)
                pygame.display.update()
                time.sleep(2)
                ticks = pygame.time.get_ticks()  
            
            if 4000 < ticks <= 6000:
                draw_all()
                window.blit(text3, textRect3)
                pygame.display.update()
                time.sleep(2)
                ticks = pygame.time.get_ticks()
           
            if 6000 < ticks <= 8000:
                draw_all()
                window.blit(text4, textRect4)
                pygame.display.update()
                time.sleep(2)
                ticks = pygame.time.get_ticks()
            ticks = pygame.time.get_ticks()

        if 8250 <= ticks <= 10500:                                                # blue
            while ticks <= 10500:
                user_car.bgcolor = (0, 0, ticks % 255)                                  
                window.fill(user_car.bgcolor)                                         # have to expand draw_all() function here to make sure one display update satisfies both text and Cars (to avoid flashing and still see both)
                pygame.draw.rect(window, user_car.color, (user_car.x, user_car.y, user_car.length, user_car.width), 2, 6)
                pygame.draw.rect(window, other_car1.color, (other_car1.x, other_car1.y, other_car1.length, other_car1.width), 2, 6)
                pygame.draw.rect(window, other_car2.color, (other_car2.x, other_car2.y, other_car2.length, other_car2.width), 2, 6)
                pygame.draw.rect(window, other_car3.color, (other_car3.x, other_car3.y, other_car3.length, other_car3.width), 2, 6)
                pygame.draw.rect(window, pedestrian.color, (pedestrian.x, pedestrian.y, pedestrian.length, pedestrian.width), 2, 6)
                window.blit(text5, textRect5)
                pygame.display.update()
                ticks = pygame.time.get_ticks()

            user_car.bgcolor = (0, 0, 100)
            speed = 40

        if 20000 < ticks < 30000:
            speed = 30

        if 30000 < ticks < 40000:
            speed = 20

        if 40000 < ticks < 50000:
            speed = 10

        if ticks > 50000:
            speed = 5



        if ticks > 144000:
            run = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False



    pygame.quit()

main()
