import pyglet
import time
import threading

class Buttons:

    def __init__(self, funcx, funcy):
        self.kill=False
        self.buttons = []
        self.x=funcx
        self.y=funcy
        self.thread = threading.Thread(target=Buttons.loop, args=(self, self.x, self.y))

    def draw(self):
        for i in self.buttons:
            i.draw()

    def add_button(self, locations, x, y):
        self.buttons.append(Button(locations, x, y))

    # def refresh(self, , y):
    #     self.x=x
    #     self.y=y

    def thread_control(self):
        if self.thread.is_alive():
            self.kill=True
        else:
            self.kill=False
            self.thread.start()
        return

    def loop(self):
        # the state self is may not update (especially if __init__ is called again). 
        # If it does not, then revise the refresh function to return self and implement it in loop()
        while True:
            Buttons.check_for_button_clicks(self, self.x(), self.y())
            if self.kill==True:
                return
        return

    def check_for_button_clicks(self, x, y):
        for i in self.buttons:
            i.clicked(x, y)
        return

class Button:
    def __init__(self, locations, x, y, button_type):
        self.batch=pyglet.graphics.Batch()
        self.state1=pyglet.sprite.Sprite(locations[0], x=x, y=y, batch=batch, opacity=100)
        self.state2=pyglet.sprite.Sprite(locations[0], x=x, y=y, batch=batch, opacity=0)
        self.held_state=False
        self.button_type=button_type 

    def click(self, x, y):
        state1.opacity=0
        state2.opacity=100
        time.sleep(.3)
        state1.opacity=100
        state2.opacity=0
        return

    def clicked(self, x, y):
        if x <= self.state1.x+self.state1.width and x >= self.state1.x and y <= self.state1.y+self.state1.height and y >= self.state1.y:
            if self.button_type == "click":
                Button.click(self, x, y)
            if self.button_type == "toggle":
                Button.toggle(self, x, y)
        return
        

    def toggle(self, x, y):
        tmp = state1.opacity
        state1.opacity=state2.opacity
        state2.opacity=tmp
        return

    def draw(self):
        self.batch.draw()
        return