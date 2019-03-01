colors = [['R','G','G','R','R'], # The color matrix (pattern) given as input
          ['R','R','G','R','R'],
          ['R','R','G','G','R'],
          ['R','R','R','R','R']]
measurements = ['G','G','G','G','G'] # The measurements that the robot sends back to us
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]] #Y is going downwards and X is going right because of a cathode ray TV [0,0]-stay in place,[0,1]- Move right, [0,-1]-Move left,[1,0]-Move down,[-1,0]- Move up
sensor_right=0.7 # The sensor measurement is right 70 percent of the time
p_move=0.8 # The robot moves 80 percent of the time when given an order to move

width = len(colors[0]) # The width of the input matrix
height = len(colors)   # The height of the input matrix

def show(p): # Function used to display the contents of the probability matrix at end
  for i in range(len(p)): #Goes through full range of probability matrix p
    print p[i] # Prints each value


def localize(colors,measurements,motions,sensor_right,p_move): #Localize function deals with the robot being able to sense and move basically path planning
  sensor_wrong=float(1-sensor_right) #probability of the robot not sensing the right color
  p_stay=float(1-p_move) #probability of the robot staying in position and not moving
  width = len(colors[0]) # The width of the input matrix calculated when the color matrix is sent as a parameter
  height = len(colors)   # The height of the input matrix calculated when the color matrix is sent as a parameter
  
  def sense(p,Z): # The sense function of the robot
    a = [] # List used to store the minilists within and send as a return value to the probability matrix calling
    for H in range(height): # Outer loop goes length wise or height wise through the matrix
      b=[] # List used to make mini lists comprising of the probability matrix after adjustments
      for W in range(width): # Inner loop going width wise through the matrix
        R=(Z==colors[H][W]) # Condition which checks if the color sent is the color currently being checked in the colors matrix, If true R=1,S=0, else R=0,S=1
        S=1-R 
        b.append(p[H][W]*((R*sensor_right)+(S*sensor_wrong))) # New probability is calculated with probability of sensor working and color check factored in and added to list b
      a.append(b) #End of the width wise list b is added to a
      x=[] # initialization of empty list
      
      for b in a: # For loop looking to find the sum of all the list elements within a
        ms=sum(b) # Sums up the elements of the lists within a
        x.append(ms) # adds the sum to a list x
        s=sum(x) # Rolling sum of the lists within a


    for H in range(height): # Outer loop goes through height wise
      for W in range(width): # Inner loop goes through width wise
        a[H][W]=a[H][W]/s # Normalizes the probability values by dividing with total sum of the elements

    return a # Returns the probability matrix to calling function
  

  def move(p, U): # Move function of the robot
    a = [] #  List used to store the minilists within and send as a return value to the probability matrix calling
    for H in range(height):# Outer loop goes length wise or height wise through the matrix
      b = [] # List used to make lists comprising of the probability matrix after adjustments
      for W in range(width): # Inner loop going width wise through the matrix
        s= p_move * p[(H-U[0]%height)][(W-U[1])%width] # value that sums the probability of the robot moving along with it not moving the algorithm also makes sure the robot doesn't go out of bounds of the matrix but infinitely stays inside it
        s=s+p_stay*p[H][W]
        b.append(s) # value is added to list b
      a.append(b) # at the end of outer loop list b is added to matrix a

    return a

  p=[] # list that will become the probability matrix of the robot being in any position
  x=(1.0/(height*width)) # Calculating the probability of the robot being in any position its basically 1/ height of the matrix* width of the matrix for equal distribution in the beginning
  for i in range(height): # Outer loop goes through height wise
    w=[] # List used to store the minilists within and send as a return value to the probability matrix calling
    for j in range(width):# Inner loop going width wise through the matrix
      w.append(x) #value is added to list w
    p.append(w) # list w is added to probability matrix p at the end of inner loop
  
  for C, D in zip(measurements,motions): #for loop used to go through both the measurements and motions lists with the zip function that combines measurements and motions into a single list
    p = move(p, D) # Car moving-probability matrix calling move function and returning the probability matrix after moving
    p = sense(p, C) #Car sense function- probability matrix after calling sense function and returning the probability matrix

  show(p) #Display of the final probabilities of where the robot could be after all motions and sensing
  return p

localize(colors,measurements,motions,sensor_right,p_move) # Calling the localize function to start the program

# References 1) Udacity.com-Artificial Intelligence for Robotics
#            2)https://github.com/bcontins/udacity-cs373/commit/2d6af27755e27eeec1d4abe0d469e7f17f0e9da1