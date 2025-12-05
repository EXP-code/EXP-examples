import matplotlib.pyplot as plt
import numpy as np
import argparse

def plot_orbit(positions, title="Orbital Trajectory", save_path=None):
    """
    Plots two orbital trajectories given a list of 3D positions.

    Parameters:
    positions: A list of 3d particle trajectories (x, y, z) positions for N times, as a list of M ndarrays of shape (N, 3).
    title (str): The title of the plot.
    save_path (str): If provided, the plot will be saved to this path.
    """

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the trajectories
    for n in range(len(positions)):
        ax.plot(positions[n][:, 0], positions[n][:, 1], positions[n][:, 2], '-')
    
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
    
    pos = []
    pos.append(data[:, 1:4])    # First object positions
    pos.append(data[:, 7:10])   # Second object positions
    pos.append(data[:, 13:17])  # Third object positions
    pos.append(data[:, 19:22])  # Fourth object positions
    pos.append(data[:, 25:28])  # Fifth object positions
    
    plot_orbit(pos, title="Selected disk orbits")
