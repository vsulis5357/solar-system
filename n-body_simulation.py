import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Gravitational constant
G = 6.67430e-11  # m^3 kg^-1 s^-2

# Masses of the Sun, Earth, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, and Neptune
masses = np.array([1.989e30, 5.972e24, 3.301e23, 4.867e24, 6.417e23, 1.898e27, 5.683e26, 8.681e25, 1.024e26])  # Sun, Earth, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune

# Initial positions and velocities (meters and m/s)
positions = np.array([[0, 0, 0], [147e9, 0, 0], [57.9e9, 0, 0], [108.2e9, 0, 0], [227.9e9, 0, 0], [778.3e9, 0, 0], [1.429e12, 0, 0], [2.871e12, 0, 0], [4.498e12, 0, 0]])  # Adding Neptune
velocities = np.array([[0, 0, 0], [0, 30e3, 0], [0, 47.87e3, 0], [0, 35e3, 0], [0, 24.07e3, 0], [0, 13.07e3, 0], [0, 9.69e3, 0], [0, 6.8e3, 0], [0, 5.43e3, 0]])  # Adding Neptune

# Time parameters
dt = 60 * 60 * 24 * 5  # Time step in seconds (3 days)
total_time = 2 * 365 * 24 * 60 * 60  # 2 years in seconds

# Number of bodies
num_bodies = len(masses)

# Colors and labels for plotting
colors = ['yellow', 'blue', 'red', 'orange', 'brown', 'grey', 'gold', 'cyan', 'blueviolet']  # Adding Neptune color
labels = ['Sun', 'Earth', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']  # Adding Neptune label

# Function to calculate gravitational force between two bodies
def calculate_force(pos1, pos2, mass1, mass2):
    r = pos2 - pos1
    r_magnitude = np.linalg.norm(r)
    force_magnitude = G * (mass1 * mass2) / (r_magnitude ** 2)
    force = force_magnitude * (r / r_magnitude)
    return force

# Function to update positions and velocities using Euler method
def update_positions_and_velocities(positions, velocities, masses, dt, current_time):
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

    return positions, velocities, current_time + dt / (60 * 60 * 24)  # Update time in days

# Animation setup
fig, ax = plt.subplots()
points, = ax.plot([], [], 'o')

# Store the points for each body separately
scatter_points = [ax.plot([], [], 'o', color=colors[i], label=labels[i], markersize=3)[0] for i in range(num_bodies)]

# Time counter initialization
time_counter_text = plt.text(0.05, 0.95, '', transform=plt.gca().transAxes, color='white', fontsize=10)

def init():
    ax.set_xlim(-4.7e12, 4.7e12)
    ax.set_ylim(-4.7e12, 4.7e12)

    for scatter_point in scatter_points:
        scatter_point.set_data([], [])

    ax.legend()
    time_counter_text.set_text('')
    return scatter_points + [time_counter_text]

def update(frame):
    global positions, velocities, total_time
    positions, velocities, current_time = update_positions_and_velocities(positions, velocities, masses, dt, frame)
    
    for i in range(num_bodies):
        scatter_points[i].set_data(positions[i, 0], positions[i, 1])
    
    # Update time counter text
    time_counter_text.set_text(f'Time: {current_time:.2f} days')

    return scatter_points + [time_counter_text]

# Create animation
ani = FuncAnimation(fig, update, frames=int(total_time/dt), init_func=init, blit=True, interval=10)

plt.show()