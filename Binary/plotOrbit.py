import matplotlib.pyplot as plt
import numpy as np
import argparse

def plot_orbit(positions, title="Orbital Trajectory", save_path=None):
    """
    Plots two orbital trajectories given a list of 3D positions.

    Parameters:
    positions: The x, y, z positions for N times both trajectories as an ndarray of shape (N, 6).
    title (str): The title of the plot.
    save_path (str): If provided, the plot will be saved to this path.
    """

    # Extract x, y, z coordinates
    x1 = positions[:, 0]
    y1 = positions[:, 1]
    z1 = positions[:, 2]
    x2 = positions[:, 3]
    y2 = positions[:, 4]
    z2 = positions[:, 5]
    
    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the trajectory
    ax.plot(x1, y1, z1, '-')
    ax.plot(x2, y2, z2, '-')
    
    # Set labels and title
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_zlabel('Z Position')
    ax.set_title(title)
    
    # Show grid
    ax.grid(True)
    
    # Save or show the plot
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot orbital trajectory from 3D positions.")
    parser.add_argument('--input', type=str,
                        default='ORBTRACE.run0',
                        help="Path to the input file containing 3D positions (one per line as x,y,z).")

    args = parser.parse_args()

    data = np.loadtxt(args.input)
    
    plot_orbit(data[:, [1,2,3,11,12,13]], title="Binary orbit")
