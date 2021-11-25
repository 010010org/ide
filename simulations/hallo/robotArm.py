'''
import os
import sys as ss

ss.path.append (os.path.abspath ('../..')) # If you want to store your simulations somewhere else, put SimPyLC in your PYTHONPATH environment variable
'''
import simpylc as sp
import robot as rb
import control as ct
import visualisation as vs


sp.World (ct.Control, rb.Robot, vs.Visualisation)