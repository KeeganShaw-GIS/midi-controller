class ODisplay:
    def __init__(self, display_obj, text1, text2):
        self.display = display_obj
        self.text1 = text1
        self.text1_pos = [0, 20]
        self.text1_size = 1
        self.text2 = text2
        self.text2_pos = [62, 15]
        self.text2_size = 2
        
        self.clear()
        self.set_text_1(text1)
        self.set_text_2(text2)

    def clear(self):
        self.display.fill(0)
        self.display.show()
    def set_text_1(self, text):
        # Clear Display
        self.display.text(
            self.text1, 
            self.text1_pos[0], 
            self.text1_pos[1],
            0,
            size=self.text1_size)
        self.display.show() 
        
        #Set Variable
        self.text1 = text

        # Set Display
        self.display.text(
            self.text1, 
            self.text1_pos[0], 
            self.text1_pos[1],
            1,
            size=self.text1_size)
        self.display.show()    

    def set_text_2(self, text):
        # Clear Display
        self.display.text(
            self.text2, 
            self.text2_pos[0], 
            self.text2_pos[1],
            0,
            size=self.text2_size)
        self.display.show() 
        
        #Set Variable
        self.text2 = text

        # Set Display
        self.display.text(
            self.text2, 
            self.text2_pos[0], 
            self.text2_pos[1],
            1,
            size=self.text2_size)
        self.display.show()    





def clear_display(display_obj):
    display_obj.fill(0)
    display_obj.show()

def set_text_1(text, display, size=1):
    display.text(text, 0, 20,1,size=size)
    display.show()

def set_text_2(text, display, size=2):
    display.text(text, 62, 15,1,size=size)
    display.show()

def reset_text_1(prev_text, display_obj):
    display_obj.fill(0)
    display_obj.show()

def reset_text_2(prev_text, display_obj):
    display_obj.fill(0)
    display_obj.show()