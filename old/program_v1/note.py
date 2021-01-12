import pyglet

"""
module used to render only notes, not text.
"""

class Note:
    # of_collection is used for formatting, list_data contains generic information used to draw notes,
    #  user_data is used for formatting based on the user of the application
    def __init__(self, of_collection, user_data, list_data, name):
        self.of_collection = of_collection
        self.user_data = user_data
        self.note_body = note_body((list_data[0], list_data[1], list_data[2]), list_data[3], list_data[4])
        self.note_text = note_text(list_data[5], list_data[6], list_data[7])
        self.note_select = pyglet.sprite.Sprite(pyglet.image.load(list_data[8]), x=list_data[4], y=list_data[4])
        self.note_select.visible=False
        self.name=pyglet.text.Label(name,
                          font_name='Times New Roman',
                          font_size=12,
                          x=0, y=0, color=(0,0,0,255))

        # user data is globally applied stuff. it was an idea but I don't know a use for it now.

        # may want to make a linked_to variable so notes can be connected to each other
        self.marginy=50
        self.marginx=20
        self.selected=False
        # make a function in workspace called apply on selected which does iterates and if the object
        # is selected a passed function is called on the object
        return
    
    # if someone wants to type in the selected note they will need to press a hotkey or something
    def select(self, x=0, y=0, override=False):
        if override == True or (x>=self.note_body.sprites[1].x and x<=self.note_body.sprites[1].x+self.note_body.sprites[1].width and y>=self.note_body.sprites[1].y and y<=self.note_body.sprites[1].y+self.note_body.sprites[1].height):
            self.selected=(not self.selected)
            self.note_select.visible=self.selected
            return True
        return False

    def flip_visible_body(self):
        self.note_body.sprites[1].visible=(not self.note_body.sprites[1].visible)

    def draw(self):
        self.note_body.batch.draw()
        self.note_text.text.draw()
        self.name.draw()
        self.note_select.draw()
        return

    def update_pos(self, x, y):
        self.note_select.update(x=x, y=y)
        self.note_body.sprites[1].update(x=x, y=y)
        self.note_body.sprites[0].update(x=x, y=self.note_body.sprites[1].height+self.note_body.sprites[1].y)
        self.note_body.sprites[2].update(x=x, y=y)
        self.note_text.text.x=self.note_body.sprites[1].x+self.marginx
        self.note_text.text.y=self.note_body.sprites[1].y+self.note_body.sprites[1].height-self.marginy
        self.name.x=x+self.note_body.sprites[0].width/2-40
        self.name.y=self.note_body.sprites[0].y+self.note_body.sprites[0].height/2
        return

    def transform(self, x, y):
        self.note_select.update(x=x+self.note_select.x, y=y+self.note_select.y)
        self.note_body.sprites[0].update(x=x+self.note_body.sprites[0].x, y=y+self.note_body.sprites[0].y)
        self.note_body.sprites[1].update(x=x+self.note_body.sprites[1].x, y=y+self.note_body.sprites[1].y)
        self.note_body.sprites[2].update(x=x+self.note_body.sprites[2].x, y=y+self.note_body.sprites[2].y)
        # += cannot be used for the update method, because I am passing variables to a function
        self.note_text.text.x=x+self.note_text.text.x
        self.note_text.text.y=y+self.note_text.text.y
        self.name.x=x+self.name.x
        self.name.y=y+self.name.y
        return

    def update_scale(self, scale_x, scale_y):
        self.note_select.update(scale_x=scale_x, scale_y=scale_y)
        self.note_body.sprites[0].update(scale_x=scale_x, scale_y=scale_y)
        self.note_body.sprites[1].update(scale_x=scale_x, scale_y=scale_y)
        self.note_body.sprites[2].update(scale_x=scale_x, scale_y=scale_y)
        # shrink the text, I tried to change scale_x but nothing seemed to change
        # also the text will go off the notes if they are shrunk enough, I
        # think this is due to the y margin but I am tempted to leave it the same
        self.note_text.text.font_size=scale_x*self.note_text.font_size

        # link up the note's parts
        Note.update_pos(self, self.note_body.sprites[2].x, self.note_body.sprites[2].y)
        return


    # def get_x(self):
    #     return self.note_body.sprites[0].x
    # def get_y(self):
    #     return self.note_body.sprites[0].y
    # def get_scale_x(self):
    #     return self.note_body.sprites[0].scale_x
    # def get_scale_y(self):
    #     return self.note_body.sprites[0].scale_y




"""
list_data
((x int, y int, z int), note_body)

note_body
((note_head pyglet.image, note_midsection pyglet.image, note_tail pyglet.image), batch pyglet.graphics.Batch)
"""

class note_body:
    def __init__(self, locations, x, y):
        self.note_head = pyglet.image.load(locations[0])
        self.note_midsection = pyglet.image.load(locations[1])
        self.note_tail = pyglet.image.load(locations[2])
        self.batch = pyglet.graphics.Batch()
        # used groups to avoid an odd bug where the note_tail would sometimes
        # be drawn behind the note_body for a long period of time.
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)
        self.sprites = []
        note_body.gen_batch(self, x, y)
        return
        
    def gen_batch(self, x, y):
        self.sprites.clear()
        self.sprites.append(pyglet.sprite.Sprite(self.note_head, x=x, y=y, batch=self.batch, group=self.foreground))
        self.sprites.append(pyglet.sprite.Sprite(self.note_midsection, x=x, y=y, batch=self.batch, group=self.background)) 
        self.sprites.append(pyglet.sprite.Sprite(self.note_tail, x=x, y=y, batch=self.batch, group=self.foreground))
        return


# this thing will be terribly over-engineered
class note_text:
    def __init__(self, text, x, y):
        self.font_size=36
        self.text = pyglet.text.Label(text,
                          font_name='Times New Roman',
                          font_size=self.font_size,
                          x=x, y=y)
        return
        # ignore this
    # def addbold(pos1, pos2):
    #     self.text.insert(pos1, "<bold>")
    #     self.text.insert(pos2, "</bold>")
    # do this stuff later, for now give nice functionality
    
