from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
from stackapi import StackAPI
import json
from math import floor


def get_data(question_id):
    data = {}
    SITE = StackAPI('codegolf')

    answers = SITE.fetch('questions/{ids}/answers', 
                        ids=[question_id], 
                        filter='!*SU8CGYZitCB.D*(BDVIficKj7nFMLLDij64nVID)N9aK3GmR9kT4IzT*5iO_1y3iZ)6W.G*')

    for answer in answers["items"]:

        soup = BeautifulSoup(answer["body"], features="lxml")
        try:
            title = soup.body.h1.text
        except:pass
        parts = title.split(",")
        bytecount = str(min([int(i) for i in parts[1:] if i.isnumeric()]))
        data[parts[0]] = bytecount

    return data


def get_offset(n):
    current_max = 1
    current_count = 0
    current_n = 0

    while True:
        current_n += 1
        current_count += 1

        if current_count == n + 1:
            y = current_max
            x = current_n
            break
        if current_n == current_max:
            current_max += 1
            current_n = 0
        
    return x-1, y-1


def add_lang(draw,n,max_n,name,lang_data):
    try:
        data = lang_data["languages"][name]
    except:
        return
    column, row = get_offset(n)

    x = 346*2 * column + 346 * (max_n - row)
    y = 600 * row
    size = 1
    font = ImageFont.truetype("fonts/ArialUnicodeMS.ttf",size=size)

    draw.polygon([(692+x,200+y),(346+x,y),(x,200+y),(x,600+y),(346+x,800+y),(692+x,600+y)],fill=data["primary color"])
    while ((font.getsize(name)[0] < 650) and (font.getsize(name)[1] < 380)):
        size += 1
        font = ImageFont.truetype("fonts/ArialUnicodeMS.ttf",size=size)

    size = floor(size*0.9)
    font = ImageFont.truetype("fonts/ArialUnicodeMS.ttf",size=size)

    
    w, h = font.getsize(name)
    coords = (x+(346-w//2),y+400-h//2-floor(h*0.15))
    #draw.rectangle([coords,(coords[0]+w,coords[1]+h)],fill="#00000000",outline="yellow",width=2)
    draw.text(coords,name,fill=data["secondary color"],font=font)
    


if __name__ == "__main__":
    
    ima = Image.new('RGB',(15000,15000))
    draw = ImageDraw.Draw(ima)

    #data = get_data(58615)
    data = {
        "05AB1E":"6",
        "Vyxal":"5",
        "J":"7",
        "Python 3":"67",
        "MAWP":"85",
        "Limn":"178"
    }

    sorted_data = {k: v for k, v in sorted(data.items(), key=lambda item: int(item[1]))}

    q, max_n = get_offset(len(data.keys()))
    with open("data.json","r") as f:
        lang_data = json.load(f)
    #print(sorted_data)
    for i in range(len(data.keys())):
        add_lang(draw,i,max_n,list(sorted_data.keys())[i],lang_data)

    ima.show()
