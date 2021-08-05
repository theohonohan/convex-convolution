import turtle, math
#import OpenGL.GLU

turtle.hideturtle()
turtle.speed(0)

bez =  [(200, 200),
        (213.77105712890625, 208.8043212890625),
        (239.59197998046875, 223.2635498046875),
        (263.17901611328125, 234.1339111328125),
        (284.60540771484375, 242.1478271484375),
        (312.85400390625, 250.4150390625),
        (336.65313720703125, 256.3751220703125),
        (350.16937255859375, 260.2874755859375),
        (361.89117431640625, 265.0054931640625),
        (371.89178466796875, 271.2615966796875),
        (378.30677032470703, 277.4036407470703),
        (382.08370208740234, 282.36045837402344),
        (387.02239990234375, 291.3177490234375),
        (392.29888916015625, 306.5826416015625),
        (396.14715576171875, 326.3153076171875),
        (398.64044189453125, 351.2481689453125),
        (399.85198974609375, 382.1136474609375),
        (400, 400)]

def half(pair):
    x, y = pair
    return (x*2,y*2)

bez2 = list(map(half, bez))
b_t = bez2.copy()
bez2.reverse()

bez2.extend(b_t[1:])

def br(p1, p2):
  x1, y1 = p1
  x2, y2 = p2
  return math.atan2(y2-y1,x2-x1)

def point_add(p1, p2):
  x1, y1 = p1
  x2, y2 = p2
  return (x1+x2,y1+y2)

def clockwise(currentAngle, targetAngle):
    if targetAngle < 0:
        targetAngle += math.pi*2
    if currentAngle < 0:
        currentAngle += math.pi*2
    if targetAngle < currentAngle:
        targetAngle += math.pi*2

    if (targetAngle - currentAngle) < math.pi:
        return True
    else:
        return False

class Path:
    def __init__(self, points):
        self.points = points
        self.current = 0
    
    def in_range(self, bearing):
        start, end =  self.active_range()
        return (start >= bearing >= end) or ((start <= end) and (bearing <= start)) or ((start <= end) and (bearing >= end))
    
    def active_range(self):
        return (br(self.points[self.current-1], self.points[self.current]), br(self.points[self.current], self.points[(self.current+1)%len(self.points)]))
    
    def set_active(self, bearing):
        while not self.in_range(bearing):
            self.forward()
        return self.points[self.current]
    
    def shift_active(self, bearing):
        if self.in_range(bearing):
            return False
                
        start, end = self.active_range()
        
        if clockwise(bearing, end):
            self.forward()
        elif not clockwise(bearing, start):
           # print("reversing: ", bearing, self.slope())
            self.back()
        else:
            print("bearing error")
        
        return True
            
    def slope(self):
        return br(self.points[self.current], self.points[(self.current+1)%len(self.points)])
    
    def forward(self):
        self.current = (self.current+1)%len(self.points)
    
    def back(self):
        self.current = (self.current-1)%len(self.points)
    
    def get(self):
#        if self.current == len(self.points)-1:
 #           print("getting last vertex")
        return self.points[self.current]
    
    def at_end(self):
        return self.current == (len(self.points) -1)

def draw_segments(list, x, y):
  turtle.penup()
  sx, sy = list[0][1]
  turtle.goto(x+sx,y+sy)
  turtle.pendown()
  
  for point1, point2 in list:
    x1, y1 = point1
    x2, y2 = point2
    turtle.color("black")
    turtle.goto(x+x1, y+y1)
    turtle.goto(x+x2, y+y2)
  turtle.color("red")
  
def draw_poly_points(list, x, y):
  output = []
  for n in range(len(list)):
    x1, y1 = list[n%len(list)]
    x2, y2 = list[(n+1)%len(list)]
    output.append(((x1,y1), (x2, y2)))
  draw_segments(output, x, y)

def circle(size):
  list = []
  for angle in range(0,360,20):
    list.append((math.sin(math.radians(angle))*size,math.cos(math.radians(angle))*size))
  return list

def ellipse(size):
  list = []
  for angle in range(0,360,9):
    list.append((math.sin(math.radians(angle))*size*1.2,math.cos(math.radians(angle))*size*0.5))
  return list

def e(a, b, phi, size):
    result = []
    p = math.radians(phi);
    a *= size;
    b *= size;
  
    for theta in range(0,360,10):
      t = math.radians(theta)
      x = a * math.cos(t) * math.cos(p) - b * math.sin(t) * math.sin(p)
      y = a * math.cos(t) * math.sin(p) + b * math.sin(t) * math.cos(p)
      
      result.append((x,y))
    result.reverse()
    return result

pen = Path(e(1,3.0,-30,40))
#print(pen.active_range())

#shape = Path([(0,0),(50, 100),(200, 200),(140, 0)])

#shape = Path([(0,0),(50, 100),(200, 200),(140, 0),(200,200),(50,100)])

shape = Path(bez2[:-1])

conv = []
final = False

v = shape.get()
a = pen.set_active(shape.slope())
#print(pen.active_range())

vertices = len(shape.points)

while True:
    conv.append(point_add(v, a))
    # pseudocode:
    # if bearing of shape at v is out of active range of pen, move pen forward or back
    # else advance v
    if pen.shift_active(shape.slope()):
        a = pen.get()
    else:
        if (final == True and shape.current == 0):
            break
        shape.forward()
        v = shape.get()
        if shape.at_end():
            final = True


#print(conv)

draw_poly_points(bez2, -595, -600)
draw_poly_points(conv, -595, -600)