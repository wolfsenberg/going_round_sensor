import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import time

# === SETTINGS ===
PORT = 'COM4'
BAUD = 9600

# === INIT ===
ser = serial.Serial(PORT, BAUD)
time.sleep(2)

angles = []
distances = []
current_angle = 0

fig, ax = plt.subplots()
line, = ax.plot([], [], 'ro-', lw=2)
distance_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=12, color='white')

def pol2cart(r, theta_deg):
    theta = math.radians(theta_deg)
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y

def update(frame):
    global current_angle

    while ser.in_waiting:
        raw = ser.readline().decode('utf-8', errors='ignore').strip()
        if raw.startswith("distance="):
            try:
                dist = int(raw.split('=')[1])
                if dist > 0 and dist < 1200:  # avoid outliers
                    # Simulate angle as manual hand movement
                    if len(distances) > 0 and abs(dist - distances[-1]) > 80:
                        # Detected a corner? Add extra angle shift
                        current_angle += 15
                    else:
                        current_angle += 2  # normal step
                    
                    distances.append(dist)
                    angles.append(current_angle)

                    # Convert polar to Cartesian
                    xs, ys = zip(*[pol2cart(d, a) for d, a in zip(distances, angles)])
                    line.set_data(xs, ys)
                    distance_text.set_text(f'Distance: {dist} cm')
                    
                    ax.relim()
                    ax.autoscale_view()
            except:
                pass

    return line, distance_text

# === PLOT STYLING ===
ax.set_facecolor('black')
ax.set_title("Manual LiDAR Shape Scanner", color='white')
ax.tick_params(colors='white')
ax.grid(True, color='gray')

ani = animation.FuncAnimation(fig, update, interval=100)
plt.show()
