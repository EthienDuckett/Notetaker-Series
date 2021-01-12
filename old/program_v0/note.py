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
        self.name=pyglet.text.Label(name,
                          font_name='Times New Roman',
                          font_size=12,
                          x=0, y=0)

        # user data is globally applied stuff
        self.marginy=50
        self.marginx=20
        return

    def draw(self):
        self.note_body.batch.draw()
        self.note_text.text.draw()
        self.name.draw()
        return

    def update_pos(self, x, y):
        self.note_body.sprites[0].update(x=x, y=y+self.note_body.sprites[1].height)
        # self.note_body.sprites[0].update(x=x, y=y)
        self.note_body.sprites[1].update(x=x, y=y)
        self.note_body.sprites[2].update(x=x, y=y)
        self.note_text.text.x=self.note_body.sprites[1].x+self.marginx
        self.note_text.text.y=y+self.note_body.sprites[1].height-self.marginy
        self.name.x=x+self.note_body.sprites[0].width/2
        self.name.y=y+self.note_body.sprites[0].y+30
        print(self.name.y)
        return

    def transform(self, x, y):
        self.note_body.sprites[0].update(x=x+self.note_body.sprites[0].x, y=y+self.note_body.sprites[0].y)
        self.note_body.sprites[1].update(x=x+self.note_body.sprites[1].x, y=y+self.note_body.sprites[1].y)
        self.note_body.sprites[2].update(x=x+self.note_body.sprites[2].x, y=y+self.note_body.sprites[2].y)
        self.note_text.text.x=x+self.note_text.text.x
        self.note_text.text.y=y+self.note_text.text.y
        self.name.x=x+self.name.x
        self.name.y=y+self.name.y
        return

    # note: scale_x is literally a mathematical formula for scale applied on x
    # size is dependent on position and width/height of image
    # to make 10% smaller do update_scale(get_scale_x*.9, get_scale_y*.9)
    def update_scale(self, scale_x, scale_y):
        self.note_body.sprites[0].update(scale_x=scale_x, scale_y=scale_y)
        self.note_body.sprites[1].update(scale_x=scale_x, scale_y=scale_y)
        self.note_body.sprites[2].update(scale_x=scale_x, scale_y=scale_y)
        self.note_text.text.scale_x=scale_x
        self.note_text.text.scale_y=scale_y
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
        self.sprites = []
        note_body.gen_batch(self, x, y)
        return
        
    def gen_batch(self, x, y):
        self.sprites.clear()
       
        self.sprites.append(pyglet.sprite.Sprite(self.note_head, x=x, y=y, batch=self.batch))
        self.sprites.append(pyglet.sprite.Sprite(self.note_midsection, x=x, y=y, batch=self.batch)) 
        self.sprites.append(pyglet.sprite.Sprite(self.note_tail, x=x, y=y, batch=self.batch))
        return


# this thing will be terribly over-engineered
class note_text:
    def __init__(self, text, x, y):
        self.text = pyglet.text.Label(text,
                          font_name='Times New Roman',
                          font_size=36,
                          x=x, y=y)
        return
    # def addbold(pos1, pos2):
    #     self.text.insert(pos1, "<bold>")
    #     self.text.insert(pos2, "</bold>")
    # do this stuff later, for now give nice functionality
    
