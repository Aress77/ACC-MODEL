import matplotlib.pyplot as plt
import numpy as np
from calculation import *
from scipy.integrate import quad


def simulate_velocity_adjustment(current_speed, acc, front_speed):
    # Simulate changes in acceleration over time
    global time_data, speed_data

    time_step = 0.1
    if current_speed == acc and front_speed < current_speed:
        total_time_steps = abs(acc - front_speed) * 10
    else:
        total_time_steps = abs(acc - current_speed) * 10
    #print(current_speed)
    t_0 = total_time_steps / 2
    k = 0.1
    if abs(acc - current_speed) > 5:
        k = 0.05

    for t in range(int(total_time_steps) + 1):
        current_time = t * time_step
        acc_adjustment = 0

        if acc > current_speed:
            acc_adjustment =  current_speed + ((acc - current_speed) / (1 + np.exp(-k * (t - t_0))))
            #print(acc_adjustment)
        elif acc < current_speed:
            acc_adjustment = current_speed - ((current_speed - acc) / (1 + np.exp(-k * (t - t_0))))
            #print(acc_adjustment)
        elif current_speed == acc and front_speed < current_speed:
            acc_adjustment = current_speed - ((current_speed - front_speed) / (1 + np.exp(-k * (t - t_0))))
            #print(acc_adjustment)
            #print("???")

        time_data.append(current_time)
        speed_data.append(acc_adjustment)


# Function to simulate initial acceleration adjustment
def simulate_smooth_velocity_adjustment(current_speed, acc):
    # Simulate changes in acceleration over time
    global time_data, speed_data

    time_step = 0.1
    total_time_steps = abs(acc - current_speed) * 10
    #print(current_speed)
    t_0 = total_time_steps / 2
    k = 0.1
    if abs(acc - current_speed) > 5:
        k = 0.05

    for t in range(int(total_time_steps)):
        current_time = t * time_step
        acc_adjustment = current_speed - ((current_speed - acc) / (1 + np.exp(-k * (t - t_0))))
        time_data.append(current_time)
        speed_data.append(acc_adjustment)


def simulate_distance_traveled(current_speed, k, t_0, dist_adjustment, distance_to_front):
    total_dist = dist_adjustment + distance_to_front  # Initial total distance in feet
    current_speed_s = current_speed * 5280 / 3600  # Convert speed to ft/s
    time_step = 0.1  # Time step granularity in seconds
    cp = current_speed_s - 0.1 * (5280 / 3600)  # Target speed in ft/s
    total_time = 0  # Total simulation time in seconds

    # Sigmoid velocity function
    def velocity_function(t):
        return current_speed_s - (current_speed_s - cp) / (1 + np.exp(-k * (t - t_0)))

    if total_dist >= get_following_distance(current_speed) * 5280:
        print("Current following distance is safe no additional changes needed.")

    while total_dist < get_following_distance(current_speed)*5280:
        # Recalculate the following distance based on the current speed after each iteration
        following_distance = get_following_distance(current_speed)*5280
        print(f"Current speed: {current_speed_s:.2f} ft/s, Following distance: {following_distance:.2f} ft")

        # Calculate the distance traveled during the current time step
        distance_traveled, _ = quad(velocity_function, total_time, total_time + time_step)
        total_dist += distance_traveled  # Update total distance in feet
        total_time += time_step  # Increment simulation time in seconds

        # Decrease speed for the next step (update in ft/s)
        current_speed_s -= 0.1 * (5280 / 3600)  # Reduce by 0.1 mph in ft/s
        cp = current_speed_s - 0.1 * (5280 / 3600)  # Update target speed
        current_speed -= 0.1
        # Debug information
        print(
            f"Time: {total_time:.1f}s, Total Distance: {total_dist:.2f} ft, Current Speed: {current_speed_s:.2f} ft/s")

        # Safety check to avoid infinite loop
        if total_time > 100:
            print("Simulation time exceeded limit!")
            break

        secondary_time_data.append(total_time)
        secondary_speed_data.append(current_speed_s * 3600 / 5280)
        distance_time_data.append(total_time)
        distance_data.append(total_dist)

    final_speed = current_speed_s * 3600 / 5280
    print(f"Final speed: {final_speed:.1f} mph")

    return total_dist


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
distance_data = []
distance_time_data = []


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
    acceleration = find_a_or_deceleration(current_speed, distance_to_front, front_speed)
    rem_dist = 0

    # Determine if adjustments are needed based on following distance and ACC speed
    if change > 0:  # Safe following distance
        if acc > current_speed:  # Accelerate
            print("Accelerate")
            simulate_velocity_adjustment(current_speed, acc, front_speed)
        elif acc < current_speed:  # Decelerate
            print("Decelerate")
            simulate_velocity_adjustment(current_speed, acc, front_speed)
        else:
            print("No adjustment needed.")
            simulate_no_adjustment(current_speed)
    elif change < 0:  # Unsafe following distance
        if current_speed < acc < front_speed: # when acc speed is smaller than current speed
                                                    # and also smaller than front speed
            print("Current speed smaller than front speed and ACC speed.")
            print("Increase speed to " + str(acc) + "mph")
            simulate_velocity_adjustment(current_speed, acc, front_speed)
        else:
            print("Decelerate to {}")
            simulate_velocity_adjustment(current_speed, acc, front_speed)
            rem_dist = calculate_remaining_distance(current_speed, front_speed, acceleration)
            # print("Remaining distance to adjust again: ", rem_dist)
            if rem_dist != 0:
                current_speed = front_speed
                simulate_distance_traveled(current_speed, 0.05, 0, rem_dist, distance_to_front)

                # Plot 1: Velocity Monitoring
                plt.figure(figsize=(8, 6))  # Create a new figure
                plt.plot(time_data, speed_data, label="Velocity", color="blue")  # Plot velocity data
                plt.title("Velocity Monitoring")
                plt.xlabel("Time (s)")
                plt.ylabel("Velocity (mph)")  # Correct unit label
                plt.legend()
                plt.grid(True)

                # Plot 2: Safe Distance Monitoring
                plt.figure(figsize=(8, 6))  # Create another new figure
                plt.plot(distance_time_data, distance_data, label="Following Distance",
                         color="green")  # Plot distance data
                plt.title("Safe Distance Monitoring")
                plt.xlabel("Time (s)")
                plt.ylabel("Following Distance (ft)")  # Ensure units match your data
                plt.legend()
                plt.grid(True)

    else:
        print("Following distance is safe.")
        simulate_no_adjustment(current_speed)

    if rem_dist == 0:
        # Plotting the data
        plt.figure(figsize=(8, 6))  # Single plot with specified size
        # Plot primary velocity data
        plt.plot(time_data, speed_data, label="Velocity", color="blue")
        plt.title("Velocity Monitoring")
        plt.xlabel("Time (s)")
        plt.ylabel("Velocity (mph/s)")  # Ensure units match your input
        plt.legend()
        plt.grid(True)  # Optional: Add grid for better readability

    plt.show()


if __name__ == "__main__":
    main()  # Call main to populate time_data and speed_data
