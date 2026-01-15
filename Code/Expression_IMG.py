from .Constant import TRANSPARENT, BLACK, WHITE, expression_font, IMAGE_PATH
from PIL import Image, ImageDraw, ImageFont

class Expression:
    def __init__(self, text):
        self.text = text
        self.img_width, self.img_height = 1200, 200
        self.background = TRANSPARENT
        self.font = ImageFont.truetype(expression_font, 70)
        self.color = [BLACK, WHITE]
        self.file_name = IMAGE_PATH
        
        self.create_image()
    
    def create_image(self):
        if self.text != None:
            for i in range(2):
                dummy = Image.new('RGBA', (1, 1))
                draw = ImageDraw.Draw(dummy)
                bbox = draw.textbbox((0, 0), self.text, font=self.font)
                
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1] + 10

                img = Image.new("RGBA", (text_width, text_height), self.background)
                draw = ImageDraw.Draw(img)
                draw.text((-bbox[0], -bbox[1]), self.text, font=self.font, fill=self.color[i])
                img.save(self.file_name[i])
