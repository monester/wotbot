#!/usr/bin/python
#import PIL
#import PIL.Image
import math
from math import sin, cos, atan

def genkey(a,b):
    return '.'.join((str(a),str(b)))


class walker:
    """ Pathfinding algorithm A* 
    
        Links:

    """
    closed_list = dict()
    opened_list = dict()
    simple = list()
    maze = list()
    x0 = None
    y0 = None
    x1 = None
    y1 = None

    def __init__(self, png_map):
        pass
#        self.i = PIL.Image.open(png_map)
#        (h,w) = self.i.size
#        for x in range(w):
#            self.maze.append(list())
#            for y in range(h):
#                r = self.i.getpixel((x,y))[0] & 1
#                r = 1 if r == 0 else 0
#                self.maze[x].append(r)
    def xy(self,a):
        (x,y) = a
        x = x + self.dx
        y = -y + self.dy
        return (int(x),int(y))

    def from_xy(self,a):
        (x,y) = a
        x = x - self.dx
        y = -y + self.dy
        return (float(x),float(y))

    def load_maze(self,file_name):
        f = open('myfile','rb')
        for x in range(700):
            self.maze.append(list())
            for y in range(700):
                r = f.read(1)
                r = 1 if r == '0' else 0
                self.maze[x].append(r)
        f.close()
                

    def find_adjacent(self,x0,y0,x1,y1):
        parent = genkey(x0,y0)
        for x in range(-1,2):
            for y in range(-1,2):
                key = genkey(x0+x,y0+y)
                if x0+x<0 or y0+y<0:
                    pass
                elif self.maze[x0+x][y0] != 0 or self.maze[x0][y0+y] != 0 or self.maze[x0+x][y0+y] != 0: # It is an obstacle
                    pass
                elif self.closed_list.has_key(key):
                    pass
                else:
                    g = 14 if abs(x) == abs(y) == 1 else 10
                    g += self.closed_list[parent]['g']
                    h = (abs(x1 - (x0+x)) + abs(y1 - (y0+y))) * 10
                    f = g+h
                    #print "add"
                    if not self.opened_list.has_key(key) or (self.opened_list.has_key(key) and self.opened_list[key]['f'] > f):
                        self.opened_list[key] = {'x':x0+x, 'y':y0+y, 'g': g, 'h': h, 'f': f, 'parent': parent}
    
        # Find lowest 'f'
        f_min = 100000000
        f_pos = ''
        for i in self.opened_list:
            f = self.opened_list[i]['f']
            if f < f_min:
                f_pos = i
                f_min = f
        return (self.opened_list[f_pos]['x'],self.opened_list[f_pos]['y'])

    def find(self, xy0,xy1):
        """ Todo: Add no route to point code """
        (x,y) = (x0,y0) = xy0
        (x1,y1) = xy1
        self.opened_list = dict()
        self.closed_list = dict()
        self.simple = list()
        key = genkey(x,y)
        print "Searching path: ", x0,y0, "=>", x1,y1
        (self.x0, self.y0, self.x1, self.y1) = (x0, y0, x1, y1)
        self.closed_list[key] = {'x':x, 'y':y, 'g': 0, 'h': 0, 'f': 0, 'parent': ''}
        while (x,y) != (x1,y1):
            (x,y) = self.find_adjacent(x,y,x1,y1)
            key = genkey(x,y)
            self.closed_list[key] = self.opened_list.pop(key)
        print "Path found"
        key = genkey(x1,y1)
        while key != '':
            #print "Add: ", self.closed_list[key]['x'],self.closed_list[key]['y']
            self.simple.append((self.closed_list[key]['x'],self.closed_list[key]['y']))
            key = self.closed_list[key]['parent']
        self.simple.reverse()
        return self.simple

    def draw(self):
        (x,y) = (self.x1, self.y1)
        key = '.'.join((str(x),str(y)))
        while key != '':
            (x,y)=(self.closed_list[key]['x'], self.closed_list[key]['y'])
            #self.i.putpixel ((x,y),(255,0,0))
            key = self.closed_list[key]['parent']
        #self.i.save('out.png', 'PNG')


    def simplify(self):
        (key_x, key_y) = (self.x0, self.y0)
        for (x,y) in self.simple[:]:
            if x == key_x or y == key_y:
                self.simple.remove((x,y))
                pass
            elif abs(x*1.0 - key_x)/abs(y*1.0 - key_y) == 1.0:
                self.simple.remove((x,y))
                pass
#            elif (cur_x - key_x)**2 + (cur_y - key_y)**2 < 64:
#                pass
            else:
                #self.i.putpixel ((x,y),(0,255,0))
                print key_x, key_y, "=>", x,y
                (key_x,key_y) = (x,y)
        self.simple.append((self.x1,self.y1))
        #self.i.save('out.png', 'PNG')
        return self.simple

    def center_path(self):
        (x0,y0) = (self.x0, self.y0)
        for i in range(len(self.simple)):
            (x1,y1) = self.simple[i]
            print x0,y0,"=>",x1,y1
            angle = math.atan2(x1-x0, -(y1-y0))
            (left_w, right_w)=(-10,10)
            for j in range(1,10,1):
                wall = self.maze[int(x1+math.cos(angle)*j)][int(y1+math.sin(angle)*j)]
                if wall != 0:
                    right_w = j
                    print "Right wall found:", j
                    break
            for j in range(-1,-10,-1):
                wall = self.maze[int(x1+math.cos(angle)*j)][int(y1+math.sin(angle)*j)]
                if wall != 0:
                    print "Left wall found:", j
                    left_w = j
                    break
            if left_w > -10 or right_w < 10:
                x1 += int(math.cos(angle)*(left_w+right_w)/2) 
                y1 += int(math.sin(angle)*(left_w+right_w)/2)
                self.simple[i] = (x1,y1)
            #self.i.putpixel ((x1,y1),(0,0,255))
            (x0,y0) = (x1,y1)
            #self.i.save('out.png', 'PNG')
        return self.simple

    def check_nowalls(self, xy0, xy1):
        """ Check if there is no walls between points
        """
        (x0,y0) = self.xy(xy0)
        (x1,y1) = self.xy(xy1)
        (x,y) = (x1-x0, y1-y0)
        angle = math.atan2(x,-y)
        for i in range(int(math.sqrt(x*x+y*y))):
            wall = self.maze[int(x0+cos(angle)*i)][int(y0+sin(angle)*i)]
            if wall != 0:
                return False
        return True


    def set_map(self, dx, dy):
        (self.dx, self.dy) = (dx,dy)
    
    def get_path(self, xy0, xy1):
        """ 
            dx=> -300, 
            dy=-300 
        """
#        x0 = int(x0+dx)
#        x1 = int(x1+dx)
#        y0 = int(-y0+dy)
#        y1 = int(-y1+dy)
        path = self.find(self.xy(xy0),self.xy(xy1))
        self.simplify()
        path = self.center_path()
        print path
        newpath = list()
        for i in path:
            newpath.append(self.from_xy(i))
        #print dx, dy
        #print "Searching (%i,%i) => (%i,%i)" % (x0,y0,x0+dx,-y0+dy)
        print newpath
        return newpath
