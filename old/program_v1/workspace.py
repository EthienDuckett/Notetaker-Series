# are there any tools to inspect the code the python interpreter creates when supplied with python code?
import collection
# may be useful for threading the functions pyglet comes with, 
# also I only need to use one of the functions and take all the values it has
import button
import pyglet

# super inefficient but I do not know how to make a thread run more than once without breaking it.
import thread_mod as thread_mod
import threading
# could fix issue


class WorkSpace(pyglet.window.Window):
    """
    The way the threading works is a local variable is created inside the
    thread, the variable can be accessed through the thread which allows for all the functions to sync.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_rate = 1/20
        self.storage = threading.Thread(target=None, args=None, kwargs=None)
        # load all this stuff from a json file
        self.storage.__dict__ = {"usr":{"pan_border":[20,20], "pan_speed":[10,10]}, "env":{"cursor_position_x":0, "cursor_position_y":0, "mouse_pressed":False, "mouse_dragged":False, "panning":False, "mouse_in_window":False}}

        
        self.settings = [[None, None],['../collection1/resources/note_type1/head.png','../collection1/resources/note_type1/midsection.png','../collection1/resources/note_type1/tail.png', 200, 0, "hello its a test", 200, 0, '../collection1/resources/note_type1/select.png'],]
        self.storage.__dict__["collections"] = [collection.Collection("collection1", None, "../collection1", self.settings, self.storage)]

        
        self.debug = {"x_label":pyglet.text.Label(), "y_label":pyglet.text.Label(), "batch":pyglet.graphics.Batch()}
        self.debug["x_label"]=pyglet.text.Label(text="X position = "+str(self.storage.__dict__["env"]["cursor_position_x"]), x=0, y=10, batch=self.debug["batch"])
        self.debug["y_label"]=pyglet.text.Label(text="Y position = "+str(self.storage.__dict__["env"]["cursor_position_y"]), font_name="Arial", x=0, y=30, batch=self.debug["batch"])

        self.storage.__dict__["buttons"] = button.Buttons(self.storage)

        # If you do dialogue boxes where users enter what they want then you need to translate that to a specific object
        self.storage.__dict__["buttons"].add_button(["../buttons/resources/state1.png", "../buttons/resources/state2.png"], 0, 0, button.Button.click, self.storage.__dict__["collections"][0].initialize_with_settings, self.settings)
        # self.storage.__dict__["buttons"].add_button(["../buttons/resources/state1.png", "../buttons/resources/state2.png"], 100, 100, button.Button.click, self.storage.__dict__["collections"][0].new_note, self.settings)

        self.workspace_threads = {"pan":thread_mod.Thread(target=(WorkSpace.pan), args=(self, self.storage.__dict__["env"]["cursor_position_x"], self.storage.__dict__["env"]["cursor_position_y"]))}
        
        return

    # functions for button.py. which are bad, they don't work well at all.
    def funcx(self):
        return self.storage.__dict__["env"]["cursor_position_x"]
    def funcy(self):
        return self.storage.__dict__["env"]["cursor_position_y"]

    def update(self, dt):
        self.debug["x_label"].text="X position = {}".format(self.storage.__dict__["env"]["cursor_position_x"])
        self.debug["y_label"].text="Y position = {}".format(self.storage.__dict__["env"]["cursor_position_y"])


        if self.storage.__dict__["env"]["panning"] == True:
            self.workspace_threads["pan"]._args=(self, self.storage.__dict__["env"]["cursor_position_x"], self.storage.__dict__["env"]["cursor_position_y"])
            self.workspace_threads["pan"].run()
        return

    def on_draw(self):
        self.clear()
        for i in self.storage.__dict__["collections"]:
            i.draw()
        self.storage.__dict__["buttons"].draw()
        self.debug["batch"].draw()
        return

    # def on_key_press(self, symbol, modifiers):
    #     if symbol == pyglet.window.key.SPACE:
    #     return
    # def on_key_release(self, symbol, modifiers):
    #     if symbol == pyglet.window.key.SPACE:
    #     return

    def on_mouse_leave(self, x, y):
        self.storage.__dict__["env"]["panning"] = False
        self.storage.__dict__["env"]["mouse_in_window"] = False
        return
    def on_mouse_enter(self, x, y):
        self.storage.__dict__["env"]["mouse_in_window"] = True
        return
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.storage.__dict__["env"]["mouse_pressed"]=True
        self.storage.__dict__["env"]["mouse_dragged"]=True
        for i in self.storage.__dict__["collections"]:
            i.drag(x, y, dx, dy)
        return
    def on_mouse_press(self, x, y, button, modifiers):
        if self.storage.__dict__["env"]["mouse_pressed"] == False:
            self.storage.__dict__["env"]["mouse_pressed"]=True
            self.storage.__dict__["buttons"].refresh()
        return
    def on_mouse_release(self, x, y, button, modifiers):
        self.storage.__dict__["env"]["mouse_pressed"]=False
        # makes it essentially impossible for the user to click on a button when releasing their mouse
        if self.storage.__dict__["env"]["mouse_dragged"] == False:
            self.storage.__dict__["buttons"].refresh()
            for i in self.storage.__dict__["collections"]:
                i.check_for_select()
        self.storage.__dict__["env"]["mouse_dragged"]=False
        return

    def on_mouse_motion(self, x, y, dx, dy):
        self.storage.__dict__["env"]["cursor_position_x"]=x
        self.storage.__dict__["env"]["cursor_position_y"]=y
        if self.storage.__dict__["env"]["mouse_in_window"] == True and self.storage.__dict__["env"]["panning"] == False:
            self.storage.__dict__["env"]["panning"] = True
            WorkSpace.pan(self, x, y)
        return

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y): 
        for i in self.storage.__dict__["collections"]:
            i.update_scale_percentage_linear(scroll_y*.01, scroll_y*.01)
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
    which is to ensure if the cursor stops moving that panning can continue
    Documentation is pretty boring. Please give me pointers on how I can better my coding practices.
    """
    def pan(self, x, y):
        # any better systems are welcome!
        # I merely threw this together with my current skill set: no math and some patience
        total=0    
        if x > window.width-self.storage.__dict__["usr"]["pan_border"][0]:
            total+=1
        elif x < self.storage.__dict__["usr"]["pan_border"][0]:
            total+=1
        if y > window.height-self.storage.__dict__["usr"]["pan_border"][1]:
            total+=1
        elif y < self.storage.__dict__["usr"]["pan_border"][1]:
            total+=1
        if total > 0:    
            x2=(window.width/2-x)/self.storage.__dict__["usr"]["pan_border"][0]**2
            y2=(window.height/2-y)/self.storage.__dict__["usr"]["pan_border"][1]**2
        else:
            x2=0
            y2=0
        for i in self.storage.__dict__["collections"]:
            i.transform_notes(self.storage.__dict__["usr"]["pan_speed"][0]*x2, self.storage.__dict__["usr"]["pan_speed"][1]*y2)
        
        if total == 0 or self.storage.__dict__["env"]["panning"] == False:
            self.storage.__dict__["env"]["panning"]=False
        return
if __name__ == "__main__":
    window = WorkSpace(650, 750, "Notetaker v1", resizable=True)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
    
    
