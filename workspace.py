import collection 
import button
import pyglet

class WorkSpace(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_rate = 1/20

        self.user = {"pan_border":[20,20], "pan_speed":[10, 10]}

        # load all this stuff from a json file
        self.settings = [[None, None],['../collection1/resources/note_type1/head.png','../collection1/resources/note_type1/midsection.png','../collection1/resources/note_type1/tail.png', 200, 0, "hello its a test", 200, 0]]
        self.collection_of_collection = [collection.Collection("collection1", None, "../collection1", self.settings)]

        self.env = {"cursor_position_x":0, "cursor_position_y":0, "mouse_pressed":False, "panning":False, "mouse_in_window":False}
        self.debug = {"x_label":pyglet.text.Label(), "y_label":pyglet.text.Label(), "batch":pyglet.graphics.Batch()}
        self.debug["x_label"]=pyglet.text.Label(text="X position = "+str(self.env["cursor_position_x"]), x=0, y=10, batch=self.debug["batch"])
        self.debug["y_label"]=pyglet.text.Label(text="Y position = "+str(self.env["cursor_position_y"]), font_name="Arial", x=0, y=30, batch=self.debug["batch"])

        self.buttons = button.Buttons(WorkSpace.funcx(self), WorkSpace.funcx(self))
        return

    # functions for button.py.
    def funcx(self):
        return self.env["cursor_position_x"]
    def funcy(self):
        return self.env["cursor_position_y"]

    def update(self, dt):
        self.debug["x_label"].text="X position = {}".format(self.env["cursor_position_x"])
        self.debug["y_label"].text="Y position = {}".format(self.env["cursor_position_y"])
        if self.env["panning"] == True:
            WorkSpace.pan(self,self.env["cursor_position_x"], self.env["cursor_position_y"])
        return

    def on_draw(self):
        self.clear()
        for i in self.collection_of_collection:
            i.draw()
        self.debug["batch"].draw()
        return

    # def on_key_press(self, symbol, modifiers):
    #     if symbol == pyglet.window.key.SPACE:
    #     return
    # def on_key_release(self, symbol, modifiers):
    #     if symbol == pyglet.window.key.SPACE:
    #     return

    def on_mouse_leave(self, x, y):
        self.env["panning"] = False
        self.env["mouse_in_window"] = False
        return
    def on_mouse_enter(self, x, y):
        self.env["mouse_in_window"] = True
        return
    def on_mouse_press(self, x, y, button, modifiers):
        self.env["mouse_pressed"]=True
        return
    def on_mouse_release(self, x, y, button, modifiers):
        self.env["mouse_pressed"]=False
        return

    def on_mouse_motion(self, x, y, dx, dy):
        self.env["cursor_position_x"]=x
        self.env["cursor_position_y"]=y
        if self.env["mouse_in_window"] == True and self.env["panning"] == False:
            self.env["panning"] = True
            WorkSpace.pan(self, x, y)
        return
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for i in self.collection_of_collection:
            i.drag(x, y, dx, dy)
        return

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y): 
        print(scroll_x)
        return

    """
    The pan function is used to simulate panning across the work space by moving all notes
    the user stays at the origin at all times.
    Currently the function works by taking x and y, 
    then it sees if they are within the margins of the panning borders which are a part of the environment dictionary
    if it is then x and y will be put into a makeshift equation which
    formats them into a float which is (hopefully) always less than 1 and greater than -1
    this float is stored and multiplied by the pan speed of env and used to transform the notes
    which similulates the notes moving away from the cursor in a straight line.
    Afterwards if no panning occurred or panning has stopped then panning is set to False
    Documentation is pretty boring. Please give me pointers on how I can better my coding practices.
    """
    def pan(self, x, y):
        # any better systems are welcome!
        # I merely threw this together with my current skill set: no math and some patience
        total=0    
        if x > window.width-self.user["pan_border"][0]:
            total+=1
        elif x < self.user["pan_border"][0]:
            total+=1
        if y > window.height-self.user["pan_border"][1]:
            total+=1
        elif y < self.user["pan_border"][1]:
            total+=1
        if total > 0:    
            x2=(window.width/2-x)/self.user["pan_border"][0]**2
            y2=(window.height/2-y)/self.user["pan_border"][1]**2
        else:
            x2=0
            y2=0
        for i in self.collection_of_collection:
            i.transform_notes(self.user["pan_speed"][0]*x2, self.user["pan_speed"][1]*y2)
        if total == 0 or self.env["panning"] == False:
            self.env["panning"]=False
        return
if __name__ == "__main__":
    window = WorkSpace(650, 750, "Notetaker v0", resizable=True)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()