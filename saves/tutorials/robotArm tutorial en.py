# this line of code imports the time library. We need to use the sleep() function that's in this library.
# A library is basically a collection of code someone else has written, that we can use in our program by "importing" it.
# This way, we don't need to reinvent the wheel every time we write a new program.
import time

# imports the library that controls the robotarm.
import robotArm

# creates an "instance" of the Arm "class" from the robotArm library. You can think of a class as a Lego set, it contains all the pieces and the instructions to put them together.
# Our instance is our own version of this set. We can build it and then tell it what to do.
# We can name our instance whatever we want, for this example I've chosen the name "arm", but you can change it if you want.
# Just make sure to change it everywhere, or the program will get confused.
arm = robotArm.Arm()

# This line of code sends an instruction to move a part of the robot arm.
# As you can see, it consists of multiple parts.
# The first part of the command just calls our instance of the robot arm.
# The second part calls the specific part of the robot arm that needs to be moved, in this case the shoulder.
# The third part tells the robot arm the direction it needs to move in, up.
# As you can see, this part ends with a set of parentheses. These are important, your program won't work if you remove them.
# To see all the different parts of the robotarm and the way they can move, look under connected devices->robotArm.
arm.shoulder.up()

# Here, we call the sleep function of the time library.
# As you can see, this time we have written something inside of the parentheses.
# Basically, this piece of code tells the program to wait for a number of seconds, or in this case, half a second.
# While the program is waiting, the shoulder of the robot arm will be moving up.
time.sleep(0.5)

# Here, we are telling another piece of the robot arm to move, in this case, the elbow.
# As you can see, there is something written inside the parentheses again.
# This time, we are giving an "argument", a bit of extra information.
# As you can probably tell, this argument tells the robot arm how much power to use.
# This is a percentage, so a number between 0 and 100.
# If we don't tell the robot arm this, it will just use full power.
arm.elbow.down(power=50)

# We're telling the program to wait another half a second. Now, both the shoulder and elbow move at the same time, because we haven't told them to stop.
time.sleep(0.5)

# Here we're telling the shoulder and elbow of the robot arm to stop moving.
arm.shoulder.off()
arm.elbow.off()

# We've reached the end of the file, so our program will now stop.
# If you're writing your own code, always make sure to turn off everything when you're done!
# If you don't, the robot arm will continue moving in the last way you told it to, reach it's movement limit and make a loud clicking noise.
# You will then need to quickly find a way to turn it off again while all of your classmates are looking at you for making so much noise, which will be very embarrassing ;)
