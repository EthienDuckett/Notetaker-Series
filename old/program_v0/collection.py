"""
collection of notes
"""
import note

class Collection:
    def __init__(self, name, password, directory, import_settings):
        self.name = name
        self.password = password
        self.directory = directory
        self.collection = []
        self.lastpos=(0, 0)
        Collection.initialize_with_settings(self, import_settings)
        return

    def initialize_with_settings(self, import_settings):
        self.collection.append(Collection.new_note(self, import_settings))
        self.collection[-1].update_pos(self.collection[-1].note_body.sprites[0].x, self.collection[-1].note_body.sprites[0].y)
        return

    def draw(self):
        for i in self.collection:
            i.draw()
        return
    
    def update_pos(self, x, y):
        for i in self.collection:
            i.update_pos(x, y)
        return
    
    def transform_notes(self, x, y):
        for i in self.collection:
            i.transform(x, y)
        return

    # note that when streching out the notes, this will be bad, you need to work around this if you have a return to 0% zoom button
    def update_scale(self, scale_x, scale_y):
        for i in self.collection:
            i.update_scale(scale_x, scale_y)
        return

    def update_scale_percentage(self, percent_of_scale_x, percent_of_scale_y):
        for i in self.collection:
            i.update_scale(i.note_body_sprites[0].scale_x*percent_of_scale_x, i.note_body_sprites[0].scale_y*percent_of_scale_y)
        return

    def update_scale_percentage_linear(self, scale_x_addition, scale_y_addition):
        def if_less_than_zero_give_zero(num):
            if num < 0:
                return 0
            else:
                return num
        for i in self.collection:
            i.update_scale(if_less_than_zero_give_zero(i.note_body_sprites[0].scale_x+scale_x_addition), if_less_than_zero_give_zero(i.note_body_sprites[0].scale_y+scale_y_addition))
        return        

    def new_note(self, import_settings):
        return note.Note(self.name, None, import_settings[1], "Unnamed")
    

    def drag(self, x, y, dx, dy):
        for i in self.collection:
            if x <= i.note_body.sprites[0].x+i.note_body.sprites[0].width and x >= i.note_body.sprites[0].x and y <= i.note_body.sprites[0].y+i.note_body.sprites[0].height and y >= i.note_body.sprites[0].y:
                i.transform(dx, dy)

        return

        # note_body(head, midsection, tail, x, y) note_text(text, x, y)
# import_settings = 
# ('../collection1/resources/note_type1/head.png','../collection1/resources/note_type1/midsection.png','../collection1/resources/note_type1/tail.png', 0, 0, "hello its a test", 0, 0)