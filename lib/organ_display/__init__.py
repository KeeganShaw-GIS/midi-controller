class ODisplay:
    def __init__(self, display_obj, text1, text2, text3):
        self.display = display_obj
        self.text1 = text1
        self.text1_pos = [0, 15]
        self.text1_size = 2
        self.text2 = text2
        self.text2_pos = [50, 15]
        self.text2_size = 2
        self.text3 = text3
        self.text3_pos = [105, 15]
        self.text3_size = 2
        
        self.clear()
        self.set_text_1(text1)
        self.set_text_2(text2)
        self.set_text_3(text3)

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

    def set_text_3(self, text):
        # Clear Display
        self.display.text(
            str(self.text3), 
            self.text3_pos[0], 
            self.text3_pos[1],
            0,
            size=self.text3_size)
        self.display.show() 
        
        #Set Variable
        self.text3 = text

        # Set Display
        self.display.text(
            self.text3, 
            self.text3_pos[0], 
            self.text3_pos[1],
            1,
            size=self.text3_size)
        self.display.show()    


