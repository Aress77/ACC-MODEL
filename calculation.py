import math

# Function to calculate safe following distance
def get_following_distance(current_speed):
    number_of_seconds = 3

    if current_speed < 60:
        number_of_seconds = 2
    elif current_speed >= 80:
        number_of_seconds = 4

    return number_of_seconds * (current_speed/3600)


def deceleration_time_to_change(current_speed, front_distance, front_speed): # time for the ego car to change speed
    dis_per_sec = current_speed/3600 - front_speed/3600        # at most 5 seconds
    if dis_per_sec == 0:
        return 5
    time_to_change = front_distance/dis_per_sec
    if time_to_change > 5:
        time_to_change = 5

    return time_to_change


def calculate_remaining_distance(current_speed, front_speed, deceleration_rate):
    # Calculate time to adjust speed
    time_to_adjust = (front_speed - current_speed) / deceleration_rate

    # Calculate distance covered by rear car
    rear_distance = (current_speed * time_to_adjust) + (0.5 * deceleration_rate * (time_to_adjust ** 2))

    # Calculate distance covered by front car
    front_distance = front_speed * time_to_adjust

    # Calculate remaining distance
    remaining_distance = front_distance - rear_distance

    return remaining_distance


def find_a_or_deceleration(current_speed, distance_to_front, front_speed):
    # find time needed to complete this process
    time = int(deceleration_time_to_change(current_speed, distance_to_front, front_speed))

    if time == 0:
        return 0

    a = (front_speed - current_speed) / time

    return a


def calculate_time_to_achieve_adjustment(total_adjustment, current_speed, a):
    # Using the quadratic formula to solve for time (t)
    discriminant = current_speed ** 2 + 2 * a * total_adjustment
    if discriminant < 0:
        raise ValueError("No real solution: check inputs, particularly the acceleration.")

    t = (-current_speed + math.sqrt(discriminant)) / a
    return t
