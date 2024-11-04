import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameters
R = 10  # Radius of the large sphere
C = np.array([0, 0, 0])  # Center of the large sphere at origin for simplicity
num_small_spheres = 5  # Number of smaller spheres
radii = [1, 1, 1, 1.1, 3]  # Radii of each small sphere
opti = asb.Opti()

# Initialize centers with initial guesses for optimization
centers = [
    opti.variable(init_guess=np.zeros(shape=3)),
    opti.variable(init_guess=np.ones(shape=3)),
    opti.variable(init_guess=np.array([4, 4, 4])),
    opti.variable(init_guess=np.array([5, 4, 5])),
    opti.variable(init_guess=np.array([5, 5, 7]))
]

# Constraints
for i in range(num_small_spheres):
    dist_to_large_sphere_center_sq = sum((centers[i][k] - C[k]) ** 2 for k in range(3))
    opti.subject_to(dist_to_large_sphere_center_sq <= (R - radii[i]) ** 2)

for i in range(num_small_spheres):
    for j in range(i + 1, num_small_spheres):
        dist_between_spheres = np.linalg.norm(centers[i] - centers[j])
        opti.subject_to(dist_between_spheres - (radii[i] + radii[j]) >= 0)

# Objective function to maximize the distance between small spheres
total_distance = sum(
    np.linalg.norm(centers[i] - centers[j]) for i in range(num_small_spheres) for j in range(i + 1, num_small_spheres)
)
opti.minimize(total_distance)

# Lists to store positions and objective values at each iteration
centers_iter = []
objective_values = []

def log_values(iteration_number):
    print(f"Logging optimizer state at iteration {iteration_number}...")
    centers_iter.append([opti.debug.value(center) for center in centers])  # Log each center individually
    objective_values.append(opti.debug.value(total_distance))  # Log the objective value

# Solve the problem with logging
sol = opti.solve(callback=log_values)
optimized_centers = [sol.value(center) for center in centers]

###############################################
###############################################
###############################################
###############################################

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot convergence of the objective function on the first subplot
ax1.plot(objective_values, marker='o')
ax1.set_xlabel("Iteration")
ax1.set_ylabel("Total Distance Between Sphere Centers")
ax1.set_title("Convergence of Objective Function")

# 3D Plot of spheres in the second subplot
ax2 = fig.add_subplot(122, projection='3d')

# Function to plot a sphere
def plot_sphere(ax, center, radius, color='b', alpha=0.3):
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 50)
    x = center[0] + radius * np.outer(np.cos(u), np.sin(v))
    y = center[1] + radius * np.outer(np.sin(u), np.sin(v))
    z = center[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color=color, alpha=alpha)

# Plot the large sphere
plot_sphere(ax2, C, R, color='gray', alpha=0.1)

# Plot each small sphere at initial positions in red
initial_centers = [np.zeros(3), np.ones(3), np.array([4, 4, 4]), np.array([5, 4, 5]), np.array([5, 5, 7])]
for center, radius in zip(initial_centers, radii):
    plot_sphere(ax2, center, radius, color='red', alpha=0.3)

# Plot each small sphere at optimized positions in blue
for center, radius in zip(optimized_centers, radii):
    plot_sphere(ax2, center, radius, color='blue', alpha=0.5)

# Set plot limits and labels for the 3D plot
ax2.set_xlim([-R, R])
ax2.set_ylim([-R, R])
ax2.set_zlim([-R, R])
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
ax2.set_zlabel("Z")
ax2.set_title("Initial (Red) and Optimized (Blue) Positions of Small Spheres within Large Sphere")

plt.tight_layout()
plt.show()

# Print the optimized centers
for i, center in enumerate(optimized_centers):
    print(f"Optimized Center {i}:", center)
