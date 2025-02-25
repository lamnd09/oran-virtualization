import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import random

# Configuration parameters
threshold = 0.3      # 30% threshold for sensitive requests
k = 0.5              # Linear reduction factor for the DRL adjustment

# Lists to hold our timestamp and ratio data
timestamp_data = []
ratio_data = []
adjusted_ratio_data = []

# Set up the figure and axes
fig, ax = plt.subplots()
line1, = ax.plot_date([], [], 'o-', label='Original Ratio', linestyle='-')
line2, = ax.plot_date([], [], 'x--', label='DRL Adjusted Ratio', linestyle='--')
ax.axhline(y=threshold, color='red', linestyle=':', linewidth=2,
           label=f'Threshold ({threshold*100:.0f}%)')
ax.set_xlabel('Timestamp')
ax.set_ylabel('Ratio (Sensitive / Total Requests)')
ax.set_title('Real-time UE Sensitive Request Ratio with DRL Adjustment')
ax.legend()
ax.grid(True)
ax.set_ylim(0, 1)

# Format the x-axis to show datetime strings
date_formatter = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(date_formatter)
fig.autofmt_xdate()

def init():
    # Set initial limits for x-axis to the last 60 seconds
    now = datetime.now()
    ax.set_xlim(now - timedelta(seconds=60), now)
    return line1, line2

def update(frame):
    # Use current real time as timestamp
    current_time = datetime.now()
    
    # Simulate a new ratio value (e.g., from actual UE data)
    new_ratio = np.random.uniform(0, 0.6)
    
    # Compute the DRL adjusted ratio using a simple linear reduction if above threshold
    if new_ratio > threshold:
        new_adjusted = new_ratio - k * (new_ratio - threshold)
    else:
        new_adjusted = new_ratio
    
    # Append new data
    timestamp_data.append(current_time)
    ratio_data.append(new_ratio)
    adjusted_ratio_data.append(new_adjusted)
    
    # Dynamically update the x-axis to show only the last 60 seconds of data
    ax.set_xlim(current_time - timedelta(seconds=60), current_time)
    
    # Update the plot data
    line1.set_data(timestamp_data, ratio_data)
    line2.set_data(timestamp_data, adjusted_ratio_data)
    
    # Adjust the animation interval for the next update randomly between 10-20 seconds (in ms)
    new_interval = random.uniform(20, 30) * 1000
    ani.event_source.interval = new_interval

    return line1, line2

# Create the animation object with an initial interval of 15 seconds (15000 ms)
ani = FuncAnimation(fig, update, init_func=init, interval=15000, blit=True)

plt.tight_layout()
plt.show()
