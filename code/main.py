import pygame
import random
from vector import *
from settings import *


class Bubble:

    def __init__(self, id):

        self.position = Vector(random.randint(51,949),random.randint(51, 649))
        self.velocity = Vector( float( random.randint(- radius,  radius)) / radius,float( random.randint( - radius, radius)) / radius)
        self.color = random.choice(colors)
        self.id = id
        self.i = 0                # i and j are the indexes of the cell of the grid in which the bubble is in  
        self.j = 0
        

    def draw(self):
          
        pygame.draw.circle(window, self.color, self.position.inttuple(), radius, 0)


    def update(self):
        
        self.position = vectorsum(self.position, self.velocity) 
        
        if self.position.x + radius > corners["topRight"].x: # to handle collisions of bubbles with walls

            self.position.x = corners["topRight"].x - radius
            self.velocity.x = - Cr * self.velocity.x
            

        if self.position.x - radius < corners["topLeft"].x:

            self.position.x = corners["topLeft"].x + radius
            self.velocity.x = - Cr * self.velocity.x
            

        if self.position.y - radius < corners["topLeft"].y:
            
            self.position.y = corners["topLeft"].y + radius
            self.velocity.y = - Cr * self.velocity.y
            

        if self.position.y + radius > corners["bottomLeft"].y:

            self.position.y = corners["bottomLeft"].y - radius
            self.velocity.y = - Cr * self.velocity.y
            

        i = int(self.position.y / (10 * radius))
        j = int(self.position.x / (10 * radius))

        if i != self.i or j != self.j: #  update grid if the bubble leaves the previous cell 

            grid[self.i][self.j].remove(self.id)  
            grid[i][j].append(self.id)
            self.i = i
            self.j = j     
        


def isCollide( bubble1, bubble2): # function to check for collision between 2 bubbles

    if vectordiff(bubble1.position, bubble2.position).magnitudesqr() < (2 * radius) ** 2:

        return True

    else:

        return False    


def resolveCollision( bubble1, bubble2): # function to resolve the collision between 2 bubbles

# when collision between two bubbles is detected, they might have already moved into each other.
# so their motion must be rewinded to the time when they actually collided and their velocities must be updated.
# then the rewinded motion must be forwarded with new the velocities.
   
    deltaPosition =  vectordiff(bubble1.position, bubble2.position)  # difference of the position vectors


    if deltaPosition.magnitudesqr == 0:  # provides slight (magnitude = 1 pixel) offset if the balls are exactly coincident.  

        bubble1.position = vectordiff(bubble1.position, polarVector(2.0 ** 0.5, bubble1.velocity.theta()))
        bubble2.position = vectordiff(bubble2.position, polarVector(2.0 ** 0.5, bubble2.velocity.theta()))
        deltaPosition = vectordiff(bubble1.position, bubble2.position)


    positionOffset = (2 * radius) - deltaPosition.magnitude()  # the extent to which the two balls have moved into each other.
    deltaSpeed = abs(vectordiff( bubble1.velocity, bubble2.velocity ).component(deltaPosition))# speed of approach
    timeFrame1 = (positionOffset / deltaSpeed) # the time elapsed between actual collision and detection


    bubble1.position = vectordiff(bubble1.position, constMultiply( timeFrame1, bubble1.velocity)) # rewinding the motion to the time of collision
    bubble2.position = vectordiff(bubble2.position, constMultiply( timeFrame1, bubble2.velocity))
    

    deltaVelocity = vectordiff( bubble1.velocity, bubble2.velocity ).componentVector(deltaPosition) # velocity of approach
    

    bubble1.velocity = vectordiff(bubble1.velocity, deltaVelocity) # update the velocities
    bubble2.velocity = vectorsum(bubble2.velocity, deltaVelocity)


    bubble1.position = vectorsum(bubble1.position, constMultiply(timeFrame1, bubble1.velocity)) # forwarding the motion to the actual time
    bubble2.position = vectorsum(bubble2.position, constMultiply(timeFrame1, bubble2.velocity))


def collisionCheck():  # checks the grid for collisions

    for i in range(gridi):

        for j in range(gridj):

            for k in range(len(grid[i][j])):
                
                for l in range(k + 1, len(grid[i][j])):

                    if isCollide(listOfBubbles[ grid[i][j][k] ], listOfBubbles[ grid[i][j][l] ]):

                        resolveCollision(listOfBubbles[ grid[i][j][k] ], listOfBubbles[ grid[i][j][l] ])

                if j != gridj - 1:

                    for l in range(len(grid[i][j + 1])):

                        if isCollide(listOfBubbles[ grid[i][j][k] ],listOfBubbles[ grid[i][j + 1][l] ]):

                            resolveCollision(listOfBubbles[ grid[i][j][k]], listOfBubbles[ grid[i][j + 1][l]])

                if i != gridi - 1:

                    for l in range(len(grid[i + 1][j])):

                        if isCollide(listOfBubbles[ grid[i][j][k] ], listOfBubbles[ grid[i + 1][j][l] ]):

                            resolveCollision(listOfBubbles[ grid[i][j][k] ], listOfBubbles[ grid[i + 1][j][l]])

                if i != gridi - 1 and j != gridj - 1:

                    for l in range(len(grid[i + 1][j + 1])):

                        if isCollide(listOfBubbles[ grid[i][j][k] ], listOfBubbles[ grid[i + 1][j + 1][l] ]):

                            resolveCollision(listOfBubbles[ grid[i][j][k] ], listOfBubbles[ grid[i + 1][j + 1][l] ])                       



if __name__ == "__main__":
    
    corners = { "topLeft": Vector(0,0), "bottomLeft": Vector(0,700), "topRight": Vector(1000,0), "bottomRight": Vector(1000,700)}
    pygame.init()
    window = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Bubbles")
    clock = pygame.time.Clock()
    running = True
    random.seed()
    listOfBubbles = []
    grid = []
    gridi = corners["bottomLeft"].y / (10 * radius) + 1
    gridj = corners["topRight"].x / (10 * radius) + 1


    for i in range(gridi):

        temp = []

        for j in range(gridj):

            temp.append([])

        grid.append(temp)    

    count = 0

    for i in range(number):

        bubble = Bubble(count)
        bubble.j = bubble.position.x / (10 * radius)
        bubble.i = bubble.position.y / (10 * radius)
        print gridi, gridj, bubble.i, bubble.j, radius
        listOfBubbles.append(bubble)
        grid[bubble.i][bubble.j].append(count)
        count += 1

                        
    while running:

        clock.tick(100)            
        window.fill((0,0,0))


        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False


        sum = 0

        for bubble in listOfBubbles:
                    
            bubble.update()
                    
        
        collisionCheck()

        for bubble in listOfBubbles:

            bubble.draw()
                    
        pygame.display.flip()        

    pygame.quit()    
