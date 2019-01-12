import math

class Vector:

    def __init__(self, x, y):

        self.x = x
        self.y = y
        
    
    def printf(self):

        print "<" , self.x , "," , self.y , ">" ,

    def inttuple(self):

        return (int(self.x), int(self.y))    

    def magnitude(self):

        return (self.x**2 +self.y**2) ** 0.5

    def magnitudesqr(self):

        return self.x**2 + self.y**2

    def theta(self):

        if self.x == 0:     # to avoid "divide by zero" error
            if self.y >= 0:
                return   math.pi / 2
            else:
                return  - math.pi / 2    

        else:
            return  math.atan(self.y /self.x)
    

    def component(self, vector):

        return dot(self, vector)/ vector.magnitude()

    def componentVector(self, vector):

        return constMultiply(dot(self, vector)/ (vector.magnitude() ** 2) , vector)


def vectorsum(a,b):

    return Vector(a.x + b.x, a.y + b.y)

def vectordiff(a,b):

    return Vector(a.x - b.x, a.y - b.y)    

def constMultiply(constant, vector):

    return Vector(constant * vector.x, constant * vector.y)

def polarVector( magnitude, theta): # create vector using polar

    return Vector( magnitude * math.cos(theta), magnitude * math.sin(theta) )    

def dot(a,b):

    return a.x * b.x + a.y * b.y

if __name__ =="__main__":

    a = Vector(2,2)
    a.componentVector( - 3 * math.pi/4 ).printf()
