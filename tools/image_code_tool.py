from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os


def gen_code_image(width=400, height=100, num_count=4, line_count=10, point_count=50, blur=False):
    # 随机数字:
    def rndChar():
        return random.randint(0, 9)

    # 图像混淆色(点,线):
    def rndColor():
        return (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))

    # 字体颜色混淆:
    def textRndColor():
        return (random.randint(0, 127), random.randint(0, 127), random.randint(0, 127))

    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font_path = os.getcwd() + '/static/814yzx.TTF'

    font = ImageFont.truetype(font_path, 70)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)

    # 划线
    for i in range(line_count):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=rndColor())

    # 画点
    point_size = 5  # 点的大小
    for i in range(point_count):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + point_size, y + point_size), 0, 180, fill=rndColor())  # 0, 180 圆弧的角度

    # 画数字:
    code = ""
    for t in range(num_count):
        sum_code = str(rndChar())
        draw.text((width / num_count * t + random.randint(0, 35), random.randint(0, 30)), sum_code, font=font, fill=textRndColor())
        code += sum_code

    # 模糊:
    if blur:
        image = image.filter(ImageFilter.BLUR)

    return image, code
