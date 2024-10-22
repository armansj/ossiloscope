import socket
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(1)
print("Waiting for connection...")
client_socket, addr = server_socket.accept()
print("Connected by", addr)

data = []
time_data = []
sample_count = 0

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_xlim(0, 100)
ax.set_ylim(0, 3.3)
ax.set_xlabel('Sample')
ax.set_ylabel('Voltage (V)')
ax.set_title('Real-time Voltage Plot')


def update(frame):
    global data, time_data, sample_count
    try:
        raw_data = client_socket.recv(1024).decode().strip()
        if raw_data:
            adc_values = raw_data.splitlines()
            for value in adc_values:
                try:
                    adc_value = int(value)
                    if adc_value < 0 or adc_value > 65535:
                        print(f"Received ADC value out of range: {adc_value}")
                        continue

                    voltage = adc_value / 65535 * 3.3
                    data.append(voltage)
                    time_data.append(sample_count)

                    sample_count += 1

                    if len(data) > 100:
                        data.pop(0)
                        time_data.pop(0)

                    line.set_data(time_data, data)

                    ax.set_xlim(time_data[0], time_data[-1])

                except ValueError:
                    print("Error converting ADC value:", value)

    except Exception as e:
        print("Error in update function:", e)

    return line,


ani = FuncAnimation(fig, update, interval=50)

# Show the plot
plt.show()