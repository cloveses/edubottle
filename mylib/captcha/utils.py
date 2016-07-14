#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import os

import random
from .config import *
import re
import math
# try:
##    import Crypto.Cipher.DES as Crypto
# except:
##    import Crypto
# from utils.captcha import Crypto
from . import Crypto


def encrypt1(s):
    return md5.new(s).hexdigest().upper()


def getTransform(x, y, a, p, o):
    return (math.sin((y + o[0]) * p) * a + x, math.sin((x + o[1]) * p) * a + y)


def gen_captcha(**kwargs):
    """Generate a captcha image"""
    from PIL import ImageFile
    from PIL import Image
    from PIL import ImageFont
    from PIL import ImageDraw
    from PIL import ImageFilter
    import random
    from PIL import ImageFile as pyImageFile
    import sys
    sys.modules['ImageFile'] = pyImageFile
    from io import StringIO, BytesIO
    # CHAR_BIT=(4,5,6,7,8)
    # CHAR_TYPE=(1,2,3)
    #随机选择字符位数和类型.
    # text=getstr( random.choice(CHAR_BIT), random.choice(CHAR_TYPE))
    text = kwargs.get('text', None)
    fnt_sz = kwargs.get('size', DEFAULT_IMAGE_SIZE)
    bkground = kwargs.get('bkground', DEFAULT_BG)
    font_color = kwargs.get('font_color', DEFAULT_FONT_COLOR)
    distortion = kwargs.get('distortion', DEFAULT_DISTORTION)
    addWidth = kwargs.get('addWidth', None)
    addHeight = kwargs.get('addHeight', None)

    period = distortion[0]
    amplitude = distortion[1]
    offset = distortion[2]

##    outFile = StringIO()
    outFile = BytesIO()

    DATA_PATH = os.path.abspath(os.path.dirname(__file__))
    FONT_PATH = DATA_PATH + '/fonts'

    # select font for captcha
    ALL_FONTS = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')
    rand_font = random.choice(ALL_FONTS)
    """font = ImageFont.truetype(FONT_PATH+'/font%s.ttf'%rand_font, fnt_sz)"""
    font = ImageFont.truetype(FONT_PATH + '/font' + rand_font + '.ttf', fnt_sz)

    #依据需求认定图片大小
    # textSize =[165,50]
    textSize = [kwargs.get('width', 165), kwargs.get('height', 50)]
    factTextSize = font.getsize(text)

    #如果定义尺寸小于实际尺寸则用实际的尺寸
    if factTextSize[0] > textSize[0]:
        textSize[0] = factTextSize[0]
    if factTextSize[1] > textSize[1]:
        textSize[1] = factTextSize[1]
#------------------------------render   background1 -----------------------
    image = Image.new(
        'RGB', (textSize[0] + addWidth, textSize[1] + addHeight), bkground)
    image.paste(bkground)
#------------------------------render       Text2 ------------------------
    draw = ImageDraw.Draw(image)
    alignment = (random.uniform(0, 1), random.uniform(0, 1))
    x = int((image.size[0] - textSize[0]) * alignment[0] + 0.5)
    y = int((image.size[1] - textSize[1]) * alignment[1] + 0.5)

    draw.text((x, y), text, font=font, fill=font_color)
#--------------new add line  i值越大线越粗------------------------
    width, height = image.size
    for i in range(0, 3):
        draw.line(((0, height / 1 + i), (width, height / 8 + i)), fill=128)

#------------------------------render       Distortion -----------------------
    r = 1
    xPoints = image.size[0] //r + 2
    yPoints = image.size[1] //r + 2

    # Create a list of arrays with transformed points
    xRows = []
    yRows = []
    for j in range(yPoints):
        xRow = []
        yRow = []
        for i in range(xPoints):
            x, y = getTransform(i * r, j * r, amplitude, period, offset)

            # Clamp the edges so we don't get black undefined areas
            x = max(0, min(image.size[0] - 1, x))
            y = max(0, min(image.size[1] - 1, y))

            xRow.append(x)
            yRow.append(y)
        xRows.append(xRow)
        yRows.append(yRow)

    # Create the mesh list, with a transformation for
    # each square between points on the grid
    mesh = []
    for j in range(yPoints - 1):
        for i in range(xPoints - 1):
            mesh.append((
                # Destination rectangle
                (i * r, j * r,
                 (i + 1) * r, (j + 1) * r),
                # Source quadrilateral
                (xRows[j][i], yRows[j][i],
                 xRows[j + 1][i], yRows[j + 1][i],
                 xRows[j + 1][i + 1], yRows[j + 1][i + 1],
                 xRows[j][i + 1], yRows[j][i + 1]),
            ))

    img = image.transform(image.size, Image.MESH, mesh, Image.BILINEAR)

    # save the image to a file
    img.save(outFile, format='jpeg')
    outFile.seek(0)
    # img.save("captchas.jpg")  #测试用,正式系统请删除.
    src = outFile.read()
    size = len(src)
    sys.modules['ImageFile'] = ImageFile
    return {'text': text, 'src': src, 'size': size}


def getCaptchasCount(havePIL):
    def getLen():
        return len(basic_english.words.split())
    return havePIL and getLen() or CAPTCHAS_COUNT


def formKey(num):
    def normalize(s):
        return (not len(s) % 8 and s) or normalize(s + str(randint(0, 9)))

    return normalize('%s_%i_' % (str(DateTime().timeTime()), num))


def encrypt(key, s):
    return toHex(Crypto.new(key).encrypt(s))


def decrypt(key, s):
    return Crypto.new(key).decrypt(toStr(s))


def parseKey(s):
    ps = re.match('^(.+?)_(.+?)_', s)
    return {'date': ps.group(1), 'key': ps.group(2)}


def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0' + hv
        lst.append(hv)

    return reduce(lambda x, y: x + y, lst)


def toStr(s):
    return s and chr(int(s[:2], base=16)) + toStr(s[2:]) or ''
# n是字符位数,flag是设置  1--数字,2--字母,3--数字和字母混合.


def getstr(n, flag,filte_chars):
    if n < 2:
        n = 2
    st = ''
    temp = ''
    while len(temp) < n:
        if flag == 1:  # 数字
            temp = temp + filte_char(chr(97 + random.randint(0, 25)),filte_chars)
        if flag == 2:  # 字母
            temp = temp + filte_char(chr(48 + random.randint(0, 9)),filte_chars)
        if flag == 3:  # 数字和字母混合
            temp = temp + filte_char(chr(97 + random.randint(0, 25)),filte_chars)
            temp = temp + filte_char(chr(48 + random.randint(0, 9)),filte_chars)
    if len(temp) > n:
        temp = temp[:n]
    if st.find(temp) == -1:
        st = st.join(['', temp])
    return st

def filte_char(ch,filte_chars):
    if ch in filte_chars:
        return ''
    else:
        return ch

INK = "red", "black", "green", "blue", "gray", "purple", "chocolate", "deeppink", "blueviolet", "royalblue", "olivedrab", "firebrick", "seagreen", "darkslateblue", "darkslategray", "darkolivegreen", "darkgoldenrod", "deepskyblue", "darkcyan", "darkorchid" # 字符颜色


def get_image(charbit, chartype, bkground, size, width, height, w=60, h=8):
    kwargs = {'text': getstr(charbit, chartype),
              'size': size,
              'bkground': bkground,
              'font_color': random.choice(INK),
              'width': width,
              'height': height,
              'addWidth': w,
              'addHeight': h}
    period = random.uniform(0.11, 0.15)
    amplitude = random.uniform(3.0, 6.5)
    kwargs['distortion'] = [period, amplitude, (2.0, 0.2)]
    return gen_captcha(**kwargs)

if __name__ == '__main__':

    INK = "red", "blue", "green", "yellow", "black"
    kwargs = {'text': getstr(4, 1),
              'size': 36,
              'bkground': '#999',
              'font_color': random.choice(INK),
              'addWidth': 60,
              'addHeight': 8}

    period = random.uniform(0.11, 0.15)
    amplitude = random.uniform(3.0, 6.5)
    kwargs['distortion'] = [period, amplitude, (2.0, 0.2)]
    image = gen_captcha(**kwargs)
