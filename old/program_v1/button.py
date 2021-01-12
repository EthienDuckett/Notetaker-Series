import pyglet
import time
import thread_mod as thread_mod

class Buttons:

    def __init__(self, of_thread):
        self.of_thread=of_thread
        self.buttons = []
        self.x=0
        self.y=0
        self.thread = thread_mod.Thread(target=Buttons.check_for_button_clicks, args=(self, 0, 0))

    def draw(self):
        for i in self.buttons:
            i.draw()

    """
    locations are the locations of the images which are used
    to draw the sprites, x and y are used to assign the location
    of the sprites
    """
    def add_button(self, locations, x, y, button_type, function, arguments):
        self.buttons.append(Button(locations, x, y, button_type, function, arguments))


    """
    for the button function, I really wanted to find a method
    which can update the self variable belonging to windows
    but I could not figure out how to update it without reassigning
    a variable manually.
    """
    def refresh(self):
        self.thread._args=(self, self.of_thread.__dict__["env"]["cursor_position_x"], self.of_thread.__dict__["env"]["cursor_position_y"])
        self.thread.run()


    def check_for_button_clicks(self, x, y):
        for i in self.buttons:
            i.clicked(x, y)
        return

class Button:
    """
    state 1 is the button when it has not been clicked
    state 2 is the button when it has been clicked
    """
    def __init__(self, locations, x, y, button_type, function, arguments):
        self.batch=pyglet.graphics.Batch()
        
        self.state1=pyglet.sprite.Sprite(pyglet.image.load(locations[0]), x=x, y=y, batch=self.batch)
        # self.state1.scale=5
        self.state1.visible=True
        self.state2=pyglet.sprite.Sprite(pyglet.image.load(locations[1]), x=x, y=y, batch=self.batch)
        self.state2.visible=False
        self.held_state=False
        self.button_type=button_type
        self.function=function
        self.arguments=arguments

        # buttons will be clicked again when mouse is released
        # but this click will act differently depending on the click type
    def clicked(self, x, y):
        if self.held_state == False:
            self.held_state = True
            if x <= self.state1.x+self.state1.width and x >= self.state1.x and y <= self.state1.y+self.state1.height and y >= self.state1.y:
                self.button_type(self)
                self.function(self.arguments)
        else:
            self.held_state = False
            if self.button_type == Button.click and self.state1.visible == False:
                # I didn't think the click method would turn out this well...
                time.sleep(.3)
                self.button_type(self)
        return

        
        
    def draw(self):
        self.batch.draw()
        return

    def click(self):
        Button.toggle(self)
        return

    def toggle(self):
        tmp = self.state1.visible
        self.state1.visible=self.state2.visible
        self.state2.visible=tmp
        return
