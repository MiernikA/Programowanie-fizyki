
# Programowanie-fizyki  

This project demonstrates 2D physics simulations.

The goal is to build a clear, modular, and stylistically consistent codebase — using `pygame.Vector2`.

<br>

## Description
- `settings.py` – global constants (window size, gravity, stiffness, etc.)


- `SoftBodyCollision.py`, `VerletCloth.py`, `TikTokBallCollision.py` – simulation scripts


- Uses `pygame` and `pygame.Vector2` for consistent 2D vector math

-------------------------------------
## Physics Calculations
### *Soft Body Simulation*  
<br>

![Soft Body Demo](./demo/softbody.gif)

<br>

![Soft Body Equation](./equations/softbody_math.png)

<br>
<br>

### *Bouncing Balls in a Circular Arena* 
<br>

![Balls Demo](./demo/balls.gif)

<br>

![Balls Equation](./equations/bounce_math.png)

<br>
<br>

### *Cloth Simulation* 

<br>

![Cloth Demo](./demo/cloth.gif)

<br>

![Cloth Equation](./equations/cloth_math.png)
-------------------------------------

<br>
<br>

## How to Run
1. Clone the repository:

   `git clone https://github.com/MiernikA/Programowanie-fizyki.git`


2. Install requirements:

   `pip install pygame`


3. Run a simulation:
   python SoftBodyCollision.py


4. Adjust parameters in settings.py (e.g. GRAVITY, SPRING_CONSTANT).

