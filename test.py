import numpy as np 
from Particle import *

part = Particle( np.array([.0,.0,.0]), np.array([.1,.1,.1]), np.array([.1,.1,.1]), 0.1, 0.01)

const = Constants( 9.81, 0.04, 0.02, np.array( [.5, .5, .5]))


tmp = np.array([
    [0.1,0.0,0.0],
    [0.2,0.1,0.0],
    [0.1,0.0,0.1],
    [-0.1,-0.1,-0.1]
     ])
    
print( tmp)

print( np.dot( tmp[0], tmp[1]))
print( np.add( tmp[0], tmp[1]))
print( np.subtract( tmp[0], tmp[1]))

print( part.get_time_of_hit(  tmp, 1))

print(  part.vel * 2)

for i in range( 100):
    part.update_velocity( const, 0.01)
    print( part.vel)
