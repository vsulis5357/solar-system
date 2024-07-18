import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Gravitational constant in m^3 kg^-1 s^-2
G = 6.67430e-11  

# Masses of the Sun, Earth, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, and Neptune
masses = np.array([1.989e30, 5.972e24, 3.301e23, 4.867e24, 6.417e23, 1.898e27, 5.683e26, 8.681e25, 1.024e26])  

# Initial positions and velocities (meters and m/s)
positions = np.array([[0, 0, 0], [147e9, 0, 0], [57.9e9, 0, 0], [108.2e9, 0, 0], [227.9e9, 0, 0], [778.3e9, 0, 0], [1.429e12, 0, 0], [2.871e12, 0, 0], [4.498e12, 0, 0]])  
velocities = np.array([[0, 0, 0], [0, 30e3, 0], [0, 47.87e3, 0], [0, 35e3, 0], [0, 24.07e3, 0], [0, 13.07e3, 0], [0, 9.69e3, 0], [0, 6.8e3, 0], [0, 5.43e3, 0]])  

# Time parameters
dt = 1.2*60 * 60 * 24  # Time step in seconds (1.2 days)
total_time = 165 * 365 * 24 * 60 * 60  # 165 years in seconds (165 is Neptune's orbital period)


# Number of bodies
num_bodies = len(masses)

# Colors and labels for plotting
colors = ['gold', 'blue', 'red', 'orange', 'brown', 'grey', 'green', 'cyan', 'blueviolet']  
labels = ['Sun', 'Earth', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']  


def calculate_force(pos1, pos2, mass1, mass2):
    '''
    A simple function to calculate the gravitational force vector exerted on the first body by the second body 
    using Newton's law of gravitation

    Args:
        pos1 : numpy array - the position of the first body at a given moment
        pos2 : numpy array - the position of the second body at a given moment
        pos1 : float - the mass of the first body at a given moment
        pos2 : float - the mass of the second body at a given moment
    '''
    r = pos2 - pos1
    r_magnitude = np.linalg.norm(r)
    force_magnitude = G * (mass1 * mass2) / (r_magnitude ** 2)
    force = force_magnitude * (r / r_magnitude)
    return force


def update_positions_and_velocities(positions, velocities, masses, dt):
    '''
    A simple function that uses Eulers integration to update the bodies positions and velocities over time
    
    Args:
        positions : numpy array - the position vectors for each body
        velocities : numpy array - the velocity vectors for each body
        masses : numpy array  - the masses of each body
        dt : float - the integration time step
    '''
    num_bodies = len(masses)
    forces = np.zeros_like(positions)

    for i in range(num_bodies):
        for j in range(num_bodies):
            if i != j:
                force = calculate_force(positions[i], positions[j], masses[i], masses[j])
                forces[i] += force

    for i in range(num_bodies):
        acceleration = forces[i] / masses[i]
        velocities[i] += acceleration * dt
        positions[i] += velocities[i] * dt

    return positions, velocities

# Plot and animation setup
fig, ax = plt.subplots()
points, = ax.plot([], [], 'o')

# Store the points for each body separately, set color and labels for each planet
scatter_points = [ax.plot([], [], 'o', color=colors[i], label=labels[i], markersize=3)[0] for i in range(num_bodies)]

# Time counter 
time_counter_text = plt.text(0.05, 0.94, '', transform=plt.gca().transAxes, color='black', fontsize=10)

def init():
    '''
    The animation initialization, returns the scatter points for the animation
    '''
    #the size of the displayed x and y axis
    ax.set_xlim(-5e12, 5e12)
    ax.set_ylim(-5e12, 5e12)

    for scatter_point in scatter_points:
        scatter_point.set_data([], [])

    ax.legend()
    time_counter_text.set_text('')
    return scatter_points + [time_counter_text]

def update(frame):
    """
    A simple function to update the positions of the bodies for each frame of the animation. Returns updated scatter points plot

    Args:
        frame (int): the current frame number.

    """
    global positions, velocities
    positions, velocities = update_positions_and_velocities(positions, velocities, masses, dt)
    
    for i in range(num_bodies):
        scatter_points[i].set_data(positions[i, 0], positions[i, 1])
    
    # Update time counter 
    current_time_years = frame * dt / (60 * 60 * 24 * 365)
    time_counter_text.set_text(f'Time: {current_time_years:.2f} years')

    return scatter_points + [time_counter_text]


# Create animation
ani = FuncAnimation(fig, update, frames=int(total_time/dt), init_func=init, blit=True, interval=10)

plt.show()