import matplotlib.pyplot as plt
from calculation import *  # Assuming your calculation functions are imported here
from numpy.f2py.auxfuncs import throw_error
import numpy as np

def simulate_velocity_adjustment(current_speed, acc, a):
    # Simulate changes in acceleration over time
    global time_data, speed_data

    time_step = 1
    total_time_steps = abs(acc - current_speed)/1.5
    print(current_speed)

    for t in range(int(total_time_steps) + 1):
        current_time = t * time_step
        acc_adjustment = current_speed + a * 1.5 * current_time
        print(acc_adjustment)
        time_data.append(current_time)
        speed_data.append(acc_adjustment)


# Function to simulate initial acceleration adjustment
def simulate_linear_velocity_adjustment(current_speed, distance_to_front, front_speed, a_deceleration):
    # Simulate changes in acceleration over time
    global time_data, speed_data

    time_step = 1
    total_time_steps = int(deceleration_time_to_change(current_speed, distance_to_front, front_speed)) + 1
    print(int(deceleration_time_to_change(current_speed, distance_to_front, front_speed)))
    print("111111111111111")
    print(total_time_steps)

    for t in range(int(total_time_steps)):
        current_time = t * time_step
        acc_adjustment = current_speed + a_deceleration * current_time
        time_data.append(current_time)
        speed_data.append(acc_adjustment)


def simulate_linear_distance_adjustment(current_speed, acceleration, dist_adjustment, distance_to_front):
    global secondary_time_data, secondary_speed_data

    # Calculate remaining distance adjustment (using your existing calculation)
    total_dist = dist_adjustment + distance_to_front  # Total distance adjustment
    time_step = 0.1  # Granularity for simulation
    total_time_steps = 0

    follow = get_following_distance(current_speed) * 5280  # Following distance in feet

    while total_dist < follow:
        total_dist += current_speed * time_step + 0.5 * time_step ** 2
        follow = get_following_distance(current_speed) * 5280
        current_speed -= 0.1  # Simulate deceleration
        total_time_steps += time_step
        if total_time_steps > 100:  # Safety check to avoid infinite loop
            print("Simulation time exceeded limit!")
            break

    # Populate data for graph
    for t in np.arange(0, total_time_steps, time_step):
        acc_adjustment = current_speed - t
        secondary_time_data.append(t)
        secondary_speed_data.append(acc_adjustment)


def simulate_no_adjustment(current_speed):
    global time_data, speed_data

    time_step = 1
    total_time_steps = 5

    for t in range(int(total_time_steps)):
        current_time = t * time_step
        acc_adjustment = current_speed
        time_data.append(current_time)
        speed_data.append(acc_adjustment)


# Initialize global variables for plotting
time_data = []
speed_data = []
secondary_time_data = []
secondary_speed_data = []


def main():
    # Get user inputs
    current_speed = int(input("Get current speed: "))
    front_speed = int(input("Get front speed: "))

    distance_to_front = float(input("Get distance to front car (ft): "))
    acc = int(input("Enter your desired ACC speed: "))

    # Calculate the following distance
    safe_distance = get_following_distance(current_speed) * 5280
    change = distance_to_front - safe_distance  # Calculate if distance to front car is safe.
                                                # (positive for safe, negative for unsafe)
    deceleration = find_deceleration(current_speed, distance_to_front, front_speed)
    rem_dist = 0

    # Determine if adjustments are needed based on following distance and ACC speed
    if change > 0:  # Safe following distance
        if acc > current_speed:  # Accelerate
            print("Accelerate")
            simulate_velocity_adjustment(current_speed, acc, 1)
        elif acc < current_speed:  # Decelerate
            print("Decelerate")
            simulate_velocity_adjustment(current_speed, acc, -1)
        else:
            print("No adjustment needed.")
            simulate_no_adjustment(current_speed)
    elif change < 0:  # Unsafe following distance (Decelerate)
        if current_speed < acc < front_speed: # when acc speed is smaller than current speed
                                                    # and also smaller than front speed
            print("Accelerate")
            simulate_velocity_adjustment(current_speed, acc, 1)
        print("Decelerate")
        simulate_linear_velocity_adjustment(current_speed, distance_to_front, front_speed, deceleration)
        rem_dist = calculate_remaining_distance(current_speed, front_speed, deceleration)
        print("Remaining distance to adjust again: ", rem_dist)
        if rem_dist != 0:
            current_speed = front_speed
            simulate_linear_distance_adjustment(current_speed, deceleration, rem_dist, distance_to_front)

            #Plot1: Velocity Monitoring
            plt.figure(figsize=(8, 6))  # Create a new figure
            plt.plot(time_data, speed_data, label="Velocity", color="blue")  # Plot velocity data
            plt.title("Velocity Monitoring")
            plt.xlabel("Time (s)")
            plt.ylabel("Velocity (mph)")  # Correct unit label
            plt.legend()
            plt.grid(True)

            # Plot 2: Safe Distance Monitoring
            plt.figure(figsize=(8, 6))  # Create another new figure
            plt.plot(secondary_time_data, secondary_speed_data, label="Velocity",
                     color="green")  # Plot distance data
            plt.title("Displacement Distance Velocity Monitoring")
            plt.xlabel("Time (s)")
            plt.ylabel("Velocity (mph)")  # Ensure units match your data
            plt.legend()
            plt.grid(True)

        # Show the plots
        plt.show()
    else:
        print("Following distance is safe.")
        simulate_no_adjustment(current_speed)

    if rem_dist == 0:
        # Plotting the data
        plt.figure(figsize=(8, 6))  # Single plot with specified size
        # Plot primary velocity data
        plt.plot(time_data, speed_data, label=" Velocity", color="blue")
        plt.title("Velocity Monitoring")
        plt.xlabel("Time (s)")
        plt.ylabel("Velocity (mph)")  # Ensure units match your input
        plt.legend()
        plt.grid(True)  # Optional: Add grid for better readability

        # Show the plot
        plt.show()

if __name__ == "__main__":
    main()  # Call main to populate time_data and speed_data
