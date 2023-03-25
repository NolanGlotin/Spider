import tkinter
from PIL import Image, ImageTk
import random as rd
from math import floor
import time

# Comportement des cartes
class Card:
    def __init__ (self,pos,val):
        self.pos = pos
        if pos[0]==10: self.x, self.y = border, border
        else:
            self.x = pos[0]*(cardSize[0]+border)+border
            self.y = cardSize[1]+border*(2+pos[1])
        self.value = val
        if pos[0]<=3 and pos[1]==5 or 4<=pos[0]<=9 and pos[1]==4: self.showed = True
        else: self.showed = False
        if self.showed: img = CardsImgs[str(val[0])+val[1]]
        else: img = back
        self.im = canvas.create_image(self.x,self.y,image=img,anchor='nw')
    def reveal(self):
        canvas.delete(self.im)
        self.im = canvas.create_image(self.x,self.y,image=CardsImgs[str(self.value[0])+self.value[1]],anchor='nw')
        self.showed = True
    def hide(self):
        canvas.delete(self.im)
        self.im = canvas.create_image(self.x,self.y,image=back,anchor='nw')
        self.showed = False

# Gestion de la souris
def press (event):
    global t
    global Move_objects
    global mouse_x
    global mouse_y
    global move_dx
    global move_dy
    global start_x
    global ready
    global History
    if ready:
        if time.time()-t>0.3:
            t = time.time()
            mouse_x, mouse_y = event.x, event.y
            x = (mouse_x-border)/(cardSize[0]+border)
            y = (mouse_y-border)/(cardSize[1]+border)
            if x-floor(x)<ratio_x and (y-floor(y)<ratio_y or y>1):
                x = floor(x)
                if floor(y)==0 and x==0:
                    ready = False
                    if len(Pick)>0:
                        History.append(('Pick',None))
                        for i in range (10):
                            img = Objects[10][-1].im
                            canvas.tag_raise(img)
                            frames = 10
                            dx = i*(cardSize[0]+border)
                            dy = cardSize[1]+border*(len(Board[i])+1)
                            for f in range (frames):
                                canvas.move(img,dx/frames,dy/frames)
                                tk.update()
                                time.sleep(0.001)
                            Board[i].append(Pick[-1])
                            Objects[i].append(Objects[10][-1])
                            Objects[i][-1].x, Objects[i][-1].y = dx+border, dy+border
                            Objects[i][-1].reveal()
                            del Pick[-1]
                            del Objects[10][-1]
                            global dim
                            if len(Board[i])>(dim[1]-cardSize[1]-2*border-(cardSize[1]-border))/border:
                                dim = (dim[0],dim[1]+border)
                                canvas.config(width=dim[0],height=dim[1])
                    ready = True
                    return None
                else:
                    y = floor((mouse_y-cardSize[1]-2*border)/border)
                if y>=0 and (mouse_y-2*cardSize[1]-border)/border<len(Board[x]):
                    if y>=len(Board[x]):
                        y = len(Board[x])-1
                    value = Board[x][y]
                    Move_objects = [Objects[x][y]]
                    start_x = x
                    for dy in range (y+1, len(Board[x])):
                        if Board[x][dy][1]!=value[1] or Board[x][dy][0]!=value[0]-(dy-y) or not Objects[x][dy].showed:
                            Move_objects = []
                            return None
                        Move_objects.append(Objects[x][dy])
                    for o in Move_objects:
                        canvas.tag_raise(o.im)
                    move_dx = mouse_x-(border+x*(cardSize[0]+border))
                    move_dy = mouse_y-(cardSize[1]+(2+y)*border)
        else:
            mouse_x = event.x
            x = (mouse_x-border)/(cardSize[0]+border)
            if x-floor(x)<ratio_x:
                x = floor(x)
                y = len(Board[x])-1
                clr = Board[x][y][1]
                for i in range (13):
                    if Board[x][y-i][1]!=clr or Board[x][y-i][0]!=i+1:
                        return None
                global Progr
                for i in range (13):
                    canvas.delete(Objects[x][-1].im)
                    del Board[x][-1]
                    del Objects[x][-1]
                if len(Board[x])>0 and not Objects[x][-1].showed:
                    History.append(('Complete',x,clr,'reveal'))
                else:
                    History.append(('Complete',x,clr,'None'))
                Progr.append(canvas.create_image(border+(cardSize[0]+border)*(len(Progr)+2),border,image=CardsImgs['1'+clr],anchor='nw'))
                if len(Progr)==8:
                    print('Gagné !!!')

def move (event):
    global mouse_x
    global mouse_y
    if len(Move_objects)>0:
        for o in Move_objects:
            canvas.move(o.im,event.x-mouse_x,event.y-mouse_y)
        mouse_x, mouse_y = event.x, event.y

def release (event):
    mouse_x, mouse_y = event.x, event.y
    global Move_objects
    if len(Move_objects)>0:
        x = (mouse_x-move_dx-border+cardSize[0]/2)/(cardSize[0]+border)
        if x-floor(x)<ratio_x and (len(Board[floor(x)])==0 or Board[floor(x)][-1][0]==Move_objects[0].value[0]+1) :
            global History
            x = floor(x)
            l = len(Board[x])
            for o in Move_objects:
                Board[x].append(o.value)
                Objects[x].append(o)
                o.x, o.y = (cardSize[0]+border)*x+border,(len(Board[x])+1)*border+cardSize[1]
                canvas.move(o.im,(cardSize[0]+border)*x+border-mouse_x+move_dx,(l+2)*border+cardSize[1]-mouse_y+move_dy)
                del Board[start_x][-1]
                del Objects[start_x][-1]
            if len(Objects[start_x])>0 and not Objects[start_x][-1].showed:
                History.append((start_x,x,len(Move_objects),'reveal'))
                Objects[start_x][-1].reveal()
            else:
                History.append((start_x,x,len(Move_objects),'None'))
            global dim
            if len(Board[x])>(dim[1]-cardSize[1]-2*border-(cardSize[1]-border))/border:
                dim = (dim[0],dim[1]+border)
                canvas.config(width=dim[0],height=dim[1])
        else:
            x = floor(x)
            for o in Move_objects:
                canvas.move(o.im,(cardSize[0]+border)*start_x+border-mouse_x+move_dx,(len(Board[start_x])-len(Move_objects)+2)*border+cardSize[1]-mouse_y+move_dy)
        Move_objects = []

# Montrer au premier plan / replacer une carte
def show(event):
    mouse_x, mouse_y = event.x, event.y
    x = (mouse_x-border)/(cardSize[0]+border)
    y = (mouse_y-border)/(cardSize[1]+border)
    if x-floor(x)<ratio_x and (y-floor(y)<ratio_y or y>1):
        x, y = floor(x), floor((mouse_y-cardSize[1]-2*border)/border)
        if y<len(Board[x])-1 and Objects[x][y].showed:
            global front
            front = canvas.create_image(x*(cardSize[0]+border)+border,(y+2)*border+cardSize[1],image=CardsImgs[str(Board[x][y][0])+Board[x][y][1]],anchor='nw')

def hide(event):
    global front
    if not front is None:
        canvas.delete(front)
        front = None

# Annuler une action
def backward(event):
    if ready:
        global History
        if len(History)>0:
            move = History[-1]
            del History[-1]
            if move[0]=='Pick':
                for x in range (9,-1,-1):
                    obj = Objects[x][-1]
                    Pick.append(Board[x][-1])
                    obj.x, obj.y = border, border
                    obj.hide()
                    del Board[x][-1]
                    del Objects[x][-1]
                    Objects[10].append(obj)
            elif move[0]=='Complete':
                global Progr
                x = move[1]
                if move[3]=='reveal':
                    Objects[x][-1].hide()
                for y in range (13,0,-1):
                    Board[x].append((y,move[2]))
                    Objects[x].append(Card((x,len(Board[x])-1),(y,move[2])))
                    Objects[x][-1].reveal()
                canvas.delete(Progr[-1])
                del Progr[-1]
            else:
                if move[3]=='reveal':
                    Objects[move[0]][-1].hide()
                for i in range (move[2]):
                    obj = Objects[move[1]][-1]
                    canvas.tag_raise(obj.im)
                    canvas.move(obj.im,(move[0]-move[1])*(border+cardSize[0]),(len(Board[move[0]])+1-len(Board[move[1]]))*border)
                    obj.x = border+move[0]*(border+cardSize[0])
                    obj.y = cardSize[1]+(len(Board[move[0]])+3)*border
                    Board[move[0]].append(Board[move[1]][-1])
                    Objects[move[0]].append(obj)
                    del Board[move[1]][-1]
                    del Objects[move[1]][-1]


# Variables et paramètres
colors = ['c','d','h','s'] # clubs, diamond, heart, spades
cardSet = 'Classic' # 'Classic' / 'Modern'
cardSize = (124,168)
border = 30
ratio_x = cardSize[0]/(cardSize[0]+border)
ratio_y = cardSize[1]/(cardSize[1]+border)
Move_objects = []
mouse_x, mouse_y = 0, 0
move_dx, move_dy = 0, 0
start_x = 0
t = time.time()
Progr = []
ready = True
front = None
History = []

# Création de l'interface graphique
tk = tkinter.Tk()
tk.title('Spider')
try:
    tk.iconbitmap('assets/ICON.ico')
except:
    pass
dim = (10*(border+cardSize[0])+border,750)
canvas = tkinter.Canvas(tk,width=dim[0],height=dim[1],bg='darkgreen')
canvas.pack()

# Importation des images
# cartes
# dimensions des images : 146x198
CardsImgs = {}
Cards = []
for val in range (1,14):
    for col in colors:
        CardsImgs[str(val)+col] = ImageTk.PhotoImage(Image.open('assets/cards/'+cardSet+'/'+str(val)+'_'+col+'.png').resize(cardSize))
        for i in range (2):
            Cards.append((val,col))
# dos
back = ImageTk.PhotoImage(Image.open('assets/cards/back.png').resize(cardSize))
# emplacement
spot = ImageTk.PhotoImage(Image.open('assets/cards/spot.png').resize(cardSize))

# Mise en place du jeu
# création des emplacements
for x in range (10):
    for y in range (2):
        if x!=1 or y!=0:
            canvas.create_image(x*(cardSize[0]+border)+border,y*(cardSize[1]+border)+border,image=spot,anchor='nw')
# mélange des cartes
Pick = []
for i in range (len(Cards)):
    r = rd.randint(0,len(Cards)-1)
    Pick.append(Cards[r])
    del Cards[r]
# distribution des cartes
Board, Objects = [], []
n = 6
for x in range (10):
    if x==4: n = 5
    Board.append([])
    Objects.append([])
    for y in range (n):
        Board[x].append(Pick[0])
        Objects[x].append(Card((x,y),(Pick[0])))
        del Pick[0]
Objects.append([])
for i in range (len(Pick)):
    Objects[-1].append(Card((10,i),(Pick[i])))
tk.update()

# Association des touches
canvas.bind_all('<B1-Motion>',move)
canvas.bind_all('<Button-1>',press)
canvas.bind_all('<ButtonRelease-1>',release)
canvas.bind_all('<Button-3>',show)
canvas.bind_all('<ButtonRelease-3>',hide)
canvas.bind_all('<Control-z>',backward)
canvas.bind_all('<Button-4>',backward)

canvas.mainloop()
