import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

# Path to the log file generated by the producer
LOG_FILE = "ue_traffic.log"

times = []
bandwidths = []

fig, ax = plt.subplots()
line, = ax.plot_date([], [], linestyle='-', marker='')

def parse_line(line):
    # Parse a line of the form:
    # "YYYY-MM-DD HH:MM:SS, bandwidth"
    # Example: "2024-11-06 14:14:46, 5"
    try:
        timestamp_str, bw_str = line.strip().split(", ")
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        bw = int(bw_str)
        return timestamp, bw
    except:
        return None, None

def update_data():
    global times, bandwidths
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    
    new_times = []
    new_bw = []
    for line in lines:
        ts, bw = parse_line(line)
        if ts is not None and bw is not None:
            new_times.append(ts)
            new_bw.append(bw)
    
    # Replace the old lists with the full dataset
    times = new_times
    bandwidths = new_bw

def animate(frame):
    # Called periodically by FuncAnimation
    update_data()
    
    # Update the line data with all data read so far
    line.set_xdata(times)
    line.set_ydata(bandwidths)

    ax.relim()
    ax.autoscale_view()

    ax.set_title('UE Bandwidth Over Time')
    ax.set_xlabel('Time')
    ax.set_ylabel('Bandwidth (Mbps)')
    
    # Format x-axis date labels
    fig.autofmt_xdate()

    return line,

# Update every 5 seconds
ani = animation.FuncAnimation(fig, animate, interval=5000)

plt.show()
