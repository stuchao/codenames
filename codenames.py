from PIL import Image, ImageColor, ImageDraw, ImageFont
import random
import sha

# colors
key_bg = "#AAF"
background = "#CCC"
card_list = {
    '25': [
        ["bad", "good"], ["neutral", "good"], ["neutral", "good"], ["neutral", "good"], ["neutral", "good"],
        ["neutral", "good"], ["good", "good"], ["good", "good"], ["good", "good"], ["good", "neutral"],
        ["good", "neutral"], ["good", "neutral"], ["good", "neutral"], ["good", "neutral"], ["good", "bad"],
        ["neutral", "bad"], ["bad", "bad"], ["neutral", "neutral"], ["neutral", "neutral"], ["neutral", "neutral"],
        ["neutral", "neutral"], ["neutral", "neutral"], ["neutral", "neutral"], ["neutral", "neutral"], ["bad", "neutral"] ] ,
    '16': [
        ["neutral", "good"], ["neutral", "good"], ["neutral", "good"], ["good", "good"],
        ["good", "good"], ["good", "good"], ["good", "neutral"], ["good", "neutral"],
        ["good", "neutral"], ["neutral", "bad"], ["bad", "bad"], ["neutral", "neutral"],
        ["neutral", "neutral"], ["neutral", "neutral"], ["neutral", "neutral"], ["bad", "neutral"] ] ,
    '9': [
        ["good","good"], ["good","good"], ["good","good"],
        ["bad","bad"], ["bad","bad"], ["bad","bad"],
        ["neutral","neutral"], ["neutral","neutral"], ["neutral","neutral"] ] }

def create_neutral_square():
    neutral_color = "#AAA"

    # neutral -- gray
    square = Image.new("RGB",(160,160),background)
    draw = ImageDraw.Draw(square)
    draw.ellipse([ 10, 10, 50, 50],neutral_color)
    draw.ellipse([ 10,110, 50,150],neutral_color)
    draw.ellipse([110, 10,150, 50],neutral_color)
    draw.ellipse([110,110,150,150],neutral_color)
    draw.rectangle([ 30, 10, 130, 150],neutral_color)
    draw.rectangle([ 10, 30, 150, 130],neutral_color)
    del draw
    return square


def create_good_square():
    good_fg = "#060"
    good_bg = "#0F0"

    # good -- green circle on green background
    square = Image.new("RGB",(160,160),background)
    draw = ImageDraw.Draw(square)
    draw.ellipse([ 10, 10, 50, 50],good_bg)
    draw.ellipse([ 10,110, 50,150],good_bg)
    draw.ellipse([110, 10,150, 50],good_bg)
    draw.ellipse([110,110,150,150],good_bg)
    draw.rectangle([ 30, 10, 130, 150],good_bg)
    draw.rectangle([ 10, 30, 150, 130],good_bg)
    draw.ellipse([25,25,135,135],good_fg)
    draw.ellipse([38,38,122,122],good_bg)
    del draw
    return square

    # red -- red x on red background
def create_bad_square():
    bad_fg = "#800"
    bad_bg = "#F00"

    square = Image.new("RGB",(160,160),background)
    draw = ImageDraw.Draw(square)
    draw.ellipse([ 10, 10, 50, 50],bad_bg)
    draw.ellipse([ 10,110, 50,150],bad_bg)
    draw.ellipse([110, 10,150, 50],bad_bg)
    draw.ellipse([110,110,150,150],bad_bg)
    draw.rectangle([ 30, 10, 130, 150],bad_bg)
    draw.rectangle([ 10, 30, 150, 130],bad_bg)
    draw.polygon([30,40,40,30,130,120,120,130],bad_fg)
    draw.polygon([30,120,40,130,130,40,120,30],bad_fg)
    return square

def create_key(seed,width,height,key_size):
    cards = card_list[str(width*height)]
    random.seed(seed)
    random.shuffle(cards)

    good = create_good_square()
    bad = create_bad_square()
    neutral = create_neutral_square()

    block = Image.new("RGB",(width*160,height*160),"white")
    labelled = False
    for j in range(height):
        for i in range(width):
            card = cards[i+j*width]
            region = (160*i,160*j,160*i+160,160*j+160)
            if card[0] == "bad":
                block.paste(bad,region)
            elif card[0] == "neutral":
                block.paste(neutral,region)
                if labelled == False:
                    labelled = True
                    draw = ImageDraw.Draw(block)
                    fnt = ImageFont.truetype("c:\windows\fonts\courbd.ttf", 48)
                    draw.text((20+160*i,20+160*j),str(seed)+"A","white",fnt)
                    del draw
            elif card[0] == "good":
                block.paste(good,region)
    sideA = Image.new("RGB",(key_size,key_size),key_bg)
    region =  ((key_size-160*width)/2, (key_size-160*height)/2, key_size-(key_size-160*width)/2, key_size-(key_size-160*height)/2)
    sideA.paste(block,region)

    labelled = False
    for j in range(height):
        for i in range(width):
            card = cards[i+j*width]
            region = (160*(width-1-i),160*(height-1-j),160*(width-1-i)+160,160*(height-1-j)+160)
            if card[1] == "bad":
                block.paste(bad,region)
            elif card[1] == "neutral":
                block.paste(neutral,region)
                if labelled == False:
                    labelled = True
                    draw = ImageDraw.Draw(block)
                    fnt = ImageFont.truetype("c:\windows\fonts\courbd.ttf", 48)
                    draw.text((20+160*(width-1-i),20+160*(height-1-j)),str(seed)+"B","white",fnt)
                    del draw
            elif card[1] == "good":
                block.paste(good,region)
    sideB = Image.new("RGB",(key_size,key_size),key_bg)
    region =  ((key_size-160*width)/2, (key_size-160*height)/2, key_size-(key_size-160*width)/2, key_size-(key_size-160*height)/2)
    sideB.paste(block,region)

    return (sideA, sideB)

def generate_sheet(seed,width,height):
    paper_width = 6.5
    paper_height = 9.5
    key_size = 826
    margin = 4
    side = [0,1,2,3,4,5,6,7,8,9,10,11]
    (side[0], side[7])  = create_key(seed+0,width,height,key_size)
    (side[1], side[6])  = create_key(seed+1,width,height,key_size)
    (side[2], side[9])  = create_key(seed+2,width,height,key_size)
    (side[3], side[8])  = create_key(seed+3,width,height,key_size)
    (side[4], side[11]) = create_key(seed+4,width,height,key_size)
    (side[5], side[10]) = create_key(seed+5,width,height,key_size)
    offset_x = (int(paper_width*300)-key_size*2-margin)/2
    offset_y = (int(paper_height*300)-key_size*3-margin*2)/2
    front = Image.new("RGB",(int(paper_width*300),int(paper_height*300)),"white")
    for j in range(3):
        for i in range(2):
            region = ( offset_x + i*key_size + margin*i,
                    offset_y + j*key_size + margin*j,
                    offset_x + i*key_size + margin*i + key_size,
                    offset_y + j*key_size + margin*j + key_size)
            front.paste(side[i+j*2],region)
    back = Image.new("RGB",(int(paper_width*300),int(paper_height*300)),"white")
    for j in range(3):
        for i in range(2):
            region = ( offset_x + i*key_size + margin*i,
                    offset_y + j*key_size + margin*j,
                    offset_x + i*key_size + margin*i + key_size,
                    offset_y + j*key_size + margin*j + key_size)
            back.paste(side[i+j*2+6],region)
    return (front, back)

def generate_random_sheet():
    seed = random.randint(17,166)*6
    (f, b) = generate_sheet(seed,5,5)
    f.save("key"+str(seed)+"A.png",dpi=(300,300))
    b.save("key"+str(seed)+"B.png",dpi=(300,300))
    print "Generate key cards " + str(seed) + " to " + str(seed+5) + ".  Saved as key"+str(seed)+"A.png and key"+str(seed)+"B.png."

def hash(seed,width,height):
    cards = card_list[str(width*height)]
    random.seed(seed)
    random.shuffle(cards)
    s = ""
    for c in cards:
        s += c[0] + c[1]
    return sha.new(s)

def check_collision(start,end):
    hashlist = {}
    for i in range(start,end):
        h = hash(i,4,4)
        if h in hashlist.keys():
            return (4, 4, i, hashlist[h])
        else:
            hashlist[h] = i
    hashlist = {}
    for i in range(start,end):
        h = hash(i,4,4)
        if h in hashlist.keys():
            return (5, 5, i, hashlist[h])
        else:
            hashlist[h] = i
    return (0, 0, 0, 0)

generate_random_sheet()
