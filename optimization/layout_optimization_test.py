import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameters
# Parameters for the cylinder
R_cyl = 5  # Radius of the cylinder
H_cyl = 20  # Height of the cylinder
R = 10  # Radius of the large sphere
C = np.array([0, 0, 0])  # Center of the large sphere at origin for simplicity
num_small_boxes = 5  # Number of smaller boxes
dimensions = [
    np.array([1, 1, 1]),  # Dimensions of each box (width, length, height)
    np.array([1, 1, 1]),
    np.array([1, 1, 1]),
    np.array([1.1, 1.1, 1.1]),
    np.array([2, 2, 8])
]
opti = asb.Opti()

# Initialize centers with initial guesses for optimization
centers = [
    opti.variable(init_guess=np.zeros(shape=3)),
    opti.variable(init_guess=np.ones(shape=3)),
    opti.variable(init_guess=np.array([4, 4, 4])),
    opti.variable(init_guess=np.array([5, 4, 5])),
    opti.variable(init_guess=np.array([5, 5, 7]))
]

for i in range(num_small_boxes):
    # Radial distance constraint in the xy-plane, considering the half-widths of the box in x and y directions
    half_width_x = dimensions[i][0] / 2
    half_width_y = dimensions[i][1] / 2
    
    # Calculate the radial distance from the cylinder axis (x^2 + y^2) and ensure the box fits within the cylinder
    dist_to_cylinder_axis_sq = (centers[i][0] ** 2 + centers[i][1] ** 2)
    max_allowed_distance = R_cyl - max(half_width_x, half_width_y)
    opti.subject_to(dist_to_cylinder_axis_sq <= max_allowed_distance ** 2)

    # Height constraint along the z-axis, considering the half-height of the box
    half_height_z = dimensions[i][2] / 2
    opti.subject_to(centers[i][2] >= -H_cyl / 2 + half_height_z)
    opti.subject_to(centers[i][2] <= H_cyl / 2 - half_height_z)


for i in range(num_small_boxes):
    for j in range(i + 1, num_small_boxes):
        # Half-dimensions of each box
        half_dim_i = dimensions[i] / 2
        half_dim_j = dimensions[j] / 2

        # Constraint to prevent overlap along each axis
        for axis in range(3):  # 0 for x, 1 for y, 2 for z
            center_diff = np.fabs(centers[i][axis] - centers[j][axis])
            min_separation = half_dim_i[axis] + half_dim_j[axis]
            opti.subject_to(center_diff >= min_separation)


# Objective function to maximize the distance between small spheres
total_distance = sum(
    np.linalg.norm(centers[i] - centers[j]) for i in range(num_small_boxes) for j in range(i + 1, num_small_boxes)
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

# Updated drawing part for a cylinder boundary
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot convergence of the objective function on the first subplot
ax1.plot(objective_values, marker='o')
ax1.set_xlabel("Iteration")
ax1.set_ylabel("Total Distance Between Box Centers")
ax1.set_title("Convergence of Objective Function")

# 3D Plot of boxes in the second subplot
ax2 = fig.add_subplot(122, projection='3d')

# Function to plot a cylinder boundary
def plot_cylinder(ax, center, radius, height, color='gray', alpha=0.1):
    z = np.linspace(-height / 2, height / 2, 50)
    theta = np.linspace(0, 2 * np.pi, 100)
    theta, z = np.meshgrid(theta, z)
    x = radius * np.cos(theta) + center[0]
    y = radius * np.sin(theta) + center[1]
    ax.plot_surface(x, y, z, color=color, alpha=alpha, rstride=5, cstride=5, edgecolor='none')

# Plot the cylinder boundary
plot_cylinder(ax2, C, R_cyl, H_cyl, color='gray', alpha=0.1)

# Function to plot a box
def plot_box(ax, center, dimensions, color='b', alpha=0.3):
    w, l, h = dimensions
    corners = np.array([
        [center[0] - w / 2, center[1] - l / 2, center[2] - h / 2],
        [center[0] - w / 2, center[1] + l / 2, center[2] - h / 2],
        [center[0] + w / 2, center[1] - l / 2, center[2] - h / 2],
        [center[0] + w / 2, center[1] + l / 2, center[2] - h / 2],
        [center[0] - w / 2, center[1] - l / 2, center[2] + h / 2],
        [center[0] - w / 2, center[1] + l / 2, center[2] + h / 2],
        [center[0] + w / 2, center[1] - l / 2, center[2] + h / 2],
        [center[0] + w / 2, center[1] + l / 2, center[2] + h / 2]
    ])
    ax.plot3D(*zip(*corners[[0, 1, 3, 2, 0]]), color=color)
    ax.plot3D(*zip(*corners[[4, 5, 7, 6, 4]]), color=color)
    for start, end in zip(corners[:4], corners[4:]):
        ax.plot3D(*zip(start, end), color=color)

# Plot each small box at initial positions in red
initial_centers = [np.zeros(3), np.ones(3), np.array([4, 4, 4]), np.array([5, 4, 5]), np.array([5, 5, 7])]
for center, dim in zip(initial_centers, dimensions):
    plot_box(ax2, center, dim, color='red', alpha=0.3)

# Plot each small box at optimized positions in blue
for center, dim in zip(optimized_centers, dimensions):
    plot_box(ax2, center, dim, color='blue', alpha=0.5)

# Set plot limits and labels for the 3D plot
ax2.set_xlim([-R_cyl, R_cyl])
ax2.set_ylim([-R_cyl, R_cyl])
ax2.set_zlim([-H_cyl / 2, H_cyl / 2])
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
ax2.set_zlabel("Z")
ax2.set_title("Initial (Red) and Optimized (Blue) Positions of Small Boxes within Cylinder")

plt.tight_layout()
plt.show()