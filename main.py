import matplotlib.pyplot as plt
import numpy as np
from calculation import *  # Assuming your calculation functions are imported here


def simulate_velocity_adjustment(current_speed, acc, a):
    # Simulate changes in acceleration over time
    global time_data, speed_data

    time_step = 0.1
    total_time_steps = abs(acc - current_speed) * 10
    print(current_speed)
    t_0 = total_time_steps / 2
    k = 0.2
    if abs(acc - current_speed) > 5:
        k = 0.1

    for t in range(int(total_time_steps) + 1):
        current_time = t * time_step
        acc_adjustment = 0

        if acc > current_speed:
            acc_adjustment =  current_speed + ((acc - current_speed) / (1 + np.exp(-k * (t - t_0))))
            print(1)
            print(acc_adjustment)
        elif acc < current_speed:
            acc_adjustment = current_speed - ((current_speed - acc) / (1 + np.exp(-k * (t - t_0))))
            print(acc_adjustment)

        time_data.append(current_time)
        speed_data.append(acc_adjustment)


# Function to simulate initial acceleration adjustment
def simulate_smooth_velocity_adjustment(current_speed, distance_to_front, front_speed, acc):
    # Simulate changes in acceleration over time
    global time_data, speed_data

    time_step = 0.1
    total_time_steps = abs(acc - current_speed) * 10
    print(current_speed)
    t_0 = total_time_steps / 2
    k = 0.2
    if abs(acc - current_speed) > 5:
        k = 0.1

    for t in range(int(total_time_steps)):
        current_time = t * time_step
        acc_adjustment = current_speed - ((current_speed - acc) / (1 + np.exp(-k * (t - t_0))))
        time_data.append(current_time)
        speed_data.append(acc_adjustment)


def simulate_linear_distance_adjustment(change, current_speed, acceleration, dist_adjustment):
    global secondary_time_data, secondary_speed_data

    # Calculate remaining distance adjustment (using your existing calculation)
    total_adjustment = change + dist_adjustment  # Total distance adjustment
    print(total_adjustment)
    print(acceleration)
    # Time step for simulation (smaller time step for more granularity)
    time_step = 0.1
    total_time_steps = abs(int(calculate_time_to_achieve_adjustment(total_adjustment, current_speed, acceleration)) * 10)
    print(total_time_steps)

    # Calculate acceleration for each time step based on current velocity and distance
    for t in range(total_time_steps):
        current_time = t * time_step
        acc_adjustment = current_speed + acceleration * current_time
        secondary_time_data.append(current_time)
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
    acc = float(input("Enter your desired ACC speed: "))

    # Calculate the following distance
    safe_distance = get_following_distance(current_speed) * 5280
    change = distance_to_front - safe_distance  # Calculate if distance to front car is safe.
                                                # (positive for safe, negative for unsafe)
    acceleration = find_a_or_deceleration(current_speed, distance_to_front, front_speed)

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
        print("Decelerate")
        simulate_smooth_velocity_adjustment(current_speed, distance_to_front, front_speed, acc)
        rem_dist = calculate_remaining_distance(current_speed, front_speed, acceleration)
        print("Remaining distance to adjust again: ", rem_dist)
        if rem_dist != 0:
            current_speed = front_speed

            simulate_linear_distance_adjustment(change, current_speed, acceleration,rem_dist)
    else:
        print("Following distance is safe.")
        simulate_no_adjustment(current_speed)

    # Plotting the data
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))  # Create 2 subplots

    # Plot primary velocity data
    ax[0].plot(time_data, speed_data, label="Primary Velocity")
    ax[0].set_title("Velocity Monitoring")
    ax[0].set_xlabel("Time (s)")
    ax[0].set_ylabel("Velocity (ft/s)")  # Make sure units match your input
    ax[0].legend()

    # Plot secondary velocity data
    ax[1].plot(secondary_time_data, secondary_speed_data, label="Conditional Velocity", color="red")
    ax[1].set_title("Displacement Distance Monitoring")
    ax[1].set_xlabel("Time (s)")
    ax[1].set_ylabel("Velocity (ft/s)")  # Adjust the label according to your data
    ax[1].legend()

    # Show the plots
    plt.show()

if __name__ == "__main__":
    main()  # Call main to populate time_data and speed_data
