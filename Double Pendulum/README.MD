## Multiple Double Pendulums Simulation

Simulation of several dobule pendulums made with python.
Using the great SDL wrapper pygame ! (more infos at https://www.pygame.org/)

Thanks to https://www.myphysicslab.com/pendulum/double-pendulum-en.html for the calculations of the exact formulas.

# Setup

Run this command in the main directory :
```
pip install -r requirements.txt
```
if it's not working, try :
```
py -m pip install -r requirements.txt
```

# Usage

To run the simulation using default parameters just run the program normally :
```
python main.py
```

Furthermore, you can personalize the values in order to get different values.
You just have to add parameters like this :
```
python main.py m=20 dm=2 a1=pi/2
```

The available parameters are the following :
```
k=integer -> n_pendulums = 512*k
m=float|integer -> starting mass of the pendulum
dm=float|integer -> as it's a mass gradient, the difference of mass between two pendulums is : dm/(k*512)
a1=a*pi/b -> where a and b are two integers|floats, basically the first angle.
a2=a*pi/b -> where a and b are two integers|floats, basically the second angle.
```