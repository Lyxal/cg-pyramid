from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
from stackapi import StackAPI
import json
from math import floor
import re
import requests



THREE_FOUR_SIX = 346
FOUR_HUNDRED = 400

def hex_to_rgb(s):
    r = int(s[1:3],16)
    g = int(s[3:5],16)
    b = int(s[5:7],16)
    return str([r,g,b])

def rgb_to_hex(arr):
    s = "#"
    for i in arr:
        s += hex(i)[2:].zfill(2)
    return s

def gen_colors(s):
    primary = "#" + format(hash(s) % 16777215,'x').zfill(6)
    data = '{"input":['+str(hex_to_rgb(primary))+',"N","N","N","N","N","N","N","N","N"],"model":"default"}'
    response = requests.post('http://colormind.io/api/', data=data).text.strip()
    complimentary = eval(response)['result'][hash(s)%4+1]
    secondary = rgb_to_hex(complimentary)
    return primary, secondary


def get_data(question_id):
    data = {}
    SITE = StackAPI('codegolf')

    answers = SITE.fetch('questions/{ids}/answers', 
                        ids=[question_id], 
                        filter='!*SU8CGYZitCB.D*(BDVIficKj7nFMLLDij64nVID)N9aK3GmR9kT4IzT*5iO_1y3iZ)6W.G*')

    for answer in answers["items"]:
        soup = BeautifulSoup(answer["body"], features="lxml")
        if soup.html.body.h1:
            title = soup.html.body.h1.text
        elif soup.html.body.h2:
            title = soup.html.body.h2.text
        elif soup.html.body.p:
            title = soup.html.body.p.text
        else:break
        finds = re.findall(r".+[\,\-\:\s]{0,3}\d+[\d\s]*(?:\s(?i)byte(?:s)?)?",title)[0]
        score = finds.split()[-1]
        name = re.split(r"[\,\-\:]",finds)[0].strip()
        try:
            data[name] = str(floor(int(score) // int(score) > -1))
        except:pass
            
    return data


def get_offset(n):
    current_max = 1
    current_count = 0
    current_n = 0

    while True:
        current_n += 1
        current_count += 1

        if current_count == n + 1:
            y, x = current_max, current_n
            break
        if current_n == current_max:
            current_max += 1
            current_n = 0
        
    return x-1, y-1, current_max


def add_lang(draw,n,max_n,name,lang_data):
    try:
        data = lang_data["languages"][name]
    except:
        primary, secondary = gen_colors(name)
        data = {
            "primary color":primary,
            "secondary color":secondary,
            "font":"ArialUnicodeMS"
        }
    
     
    column, row, _ = get_offset(n)

    x = THREE_FOUR_SIX*2 * column + THREE_FOUR_SIX * (max_n - row)
    y = FOUR_HUNDRED*1.5 * row
    size = 1
    try:
        font_name = data["font"]
        font = ImageFont.truetype(f"fonts/{font_name}/{font_name}.ttf",size=size)
    except:
        font_name = "ArialUnicodeMS"
        font = ImageFont.truetype("fonts/ArialUnicodeMS/ArialUnicodeMS.ttf",size=size)

    draw.polygon([(THREE_FOUR_SIX*2+x,FOUR_HUNDRED//2+y),(THREE_FOUR_SIX+x,y),(x,FOUR_HUNDRED//2+y),(x,FOUR_HUNDRED*1.5+y),(THREE_FOUR_SIX+x,FOUR_HUNDRED*2+y),(THREE_FOUR_SIX*2+x,FOUR_HUNDRED*1.5+y)],fill=data["primary color"])
    while ((font.getsize(name)[0] < THREE_FOUR_SIX*1.6) and (font.getsize(name)[1] < FOUR_HUNDRED*1.6)):
        size += 1
        font = ImageFont.truetype(f"fonts/{font_name}/{font_name}.ttf",size=size)

    size = floor(size*0.9)
    font = ImageFont.truetype(f"fonts/{font_name}/{font_name}.ttf",size=size)

    
    w, h = font.getsize(name)
    offset_x, offset_y = font.getoffset(name)
    if name.upper() != name:
        _, h = font.getsize('a')
        _, offset_y = font.getoffset('a')
    
    w += offset_x
    h += offset_y

    coords = (x+(THREE_FOUR_SIX-w//2),y+FOUR_HUNDRED-h//2)#-floor(h*0.15))
    #draw.rectangle([coords,(coords[0]+w,coords[1]+h)],fill="#00000000",outline="yellow",width=2)
    draw.text(coords,name,fill=data["secondary color"],font=font)
    #draw.line([(coords[0],coords[1]+h//2),(coords[0]+w,coords[1]+h//2)],fill=(255,0,255),width=2)
    


if __name__ == "__main__":
    
    

    data = get_data(219109)
    '''
    data = {
        "05AB1E":"6",
        "Vyxal":"5",
        "J":"7",
        "Python 3":"67",
        "MAWP":"85",
        "Limn":"178",
        "Lua":"35",
        "Scheme":"183",
        "Malbolge":"72",
        "PHP":"91",
        "APL":"6",
        "Python 2":"65",
        "JavaScript (ES6)":"64",
        "R":"85",
        "Haskell":"90",
        "x86-16 machine code":"130",
        "PowerShell":"129",
        "asm2bf":"136",
        "naz":"158",
        "Seed":"194",
        "Pyth":"12",
        "><>":"100"
    }
    '''
    sorted_data = {k: v for k, v in sorted(data.items(), key=lambda item: int(item[1]))}

    ima_size_x, ima_size_y, max_ = get_offset(len(data.keys()))
    ima = Image.new('RGB',((max_-1) * 792,(ima_size_y + 2) * 600),"#36393E")
    draw = ImageDraw.Draw(ima)


    q, max_n, _ = get_offset(len(data.keys()))
    with open("data.json","r") as f:
        lang_data = json.load(f)
    #print(sorted_data)
    for i in range(len(data.keys())):
        add_lang(draw,i,max_n,list(sorted_data.keys())[i],lang_data)

    ima.show()
