#from controller import Robot, Motor, Lidar, Keyboard, LidarPoint, Camera
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

def plot_with_custom_colors(xy_pairs, highlight_indices, default_color='blue', highlight_color='red'):
    """
    Plots (x, y) pairs with custom colors for specified indices.
    
    Parameters:
    - xy_pairs: List of (x, y) tuples.
    - highlight_indices: List of indices of xy_pairs to highlight.
    - default_color: Color for the default points.
    - highlight_color: Color for the highlighted points.
    """
    # Separate x and y values
    x_values, y_values = zip(*xy_pairs)
    
    # Plot default points
    plt.scatter(x_values, y_values, color=default_color, label='Default Points')
    
    # Plot highlighted points
    for index in highlight_indices:
        if 0 <= index < len(xy_pairs):
            plt.scatter(x_values[index], y_values[index], color=highlight_color, label='Highlighted Points')
    
    # Handle legend (to avoid duplicate labels for highlighted points)
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))  # Removes duplicates
    plt.legend(by_label.values(), by_label.keys())
    
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Custom Colored Points')
    plt.show()

# Example usage
xy_pairs = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
highlight_indices = [1, 3]  # Change the color of the 2nd and 4th points
plot_with_custom_colors(xy_pairs, highlight_indices, default_color='blue', highlight_color='red')