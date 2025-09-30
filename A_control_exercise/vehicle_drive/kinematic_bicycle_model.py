import math

def kinematic_bicycle_model(x, y, theta, v, delta, L, dt):
    """
    Kinematic bicycle model update.

    Parameters:
    x, y (float): Current position (m).
    theta (float): Current heading (rad).
    v (float): forward velocity.
    delta (float): Steering angle of front wheel (rad).
    L (float): Wheelbase (m).
    dt (float): Time step (s).

    Returns:
    tuple: Updated (x, y, theta) position and orientation of the vehicle.
    """
    # Update equations
    x_new = x + v * math.cos(theta) * dt
    y_new = y + v * math.sin(theta) * dt
    theta_new = theta + (v / L) * math.tan(delta) * dt

    return x_new, y_new, theta_new