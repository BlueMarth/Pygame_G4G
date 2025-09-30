import math

class Vehicle:
    def __init__(self, x, y, angle=0.0, velocity=0.0):
        self.x = x
        self.y = y
        self.angle = angle  # radians
        self.velocity = velocity
        self.steering_angle = 0.0

    def update(self, control, dt):
        raise NotImplementedError("Update method must be implemented by subclasses.")

    def handle_input(self, keys):
        raise NotImplementedError("handle_input must be implemented by subclasses.")

    def draw(self, surface):
        raise NotImplementedError("draw must be implemented by subclasses.")

class Car(Vehicle):
    def __init__(self, x, y, params):
        super().__init__(x, y)
        self.length = params.get('length', 100)
        self.width = params.get('width', 40)
        self.max_velocity = params.get('max_velocity', 6)
        self.reverse_max_velocity = params.get('reverse_max_velocity', -2)
        self.acceleration = params.get('acceleration', 0.2)
        self.friction = params.get('friction', 0.99)
        self.reverse_friction = params.get('reverse_friction', 0.97)
        self.handbrake_strength = params.get('handbrake_strength', 0.9)
        self.max_steering = math.radians(params.get('max_steering_deg', 35))
        self.steering_speed = math.radians(params.get('steering_speed_deg', 2.5))
        self.wheelbase = params.get('wheelbase', 80)

    def update(self, control, dt):
        # Simple kinematic bicycle model
        throttle = control.get('throttle', 0)
        brake = control.get('brake', 0)
        steer = control.get('steer', 0)
        handbrake = control.get('handbrake', False)

        # Acceleration and braking
        if throttle:
            self.velocity += self.acceleration * dt
            if self.velocity > self.max_velocity:
                self.velocity = self.max_velocity
        elif brake:
            self.velocity -= self.acceleration * dt
            if self.velocity < self.reverse_max_velocity:
                self.velocity = self.reverse_max_velocity
        elif handbrake:
            self.velocity *= self.handbrake_strength
            if abs(self.velocity) < 1e-4:
                self.velocity = 0
        else:
            if self.velocity < 0:
                self.velocity *= self.reverse_friction
            else:
                self.velocity *= self.friction
            if abs(self.velocity) < 1e-4:
                self.velocity = 0

        # Steering
        self.steering_angle += steer * self.steering_speed * dt
        self.steering_angle = max(-self.max_steering, min(self.steering_angle, self.max_steering))
        if not steer:
            # Auto-centering
            if self.steering_angle > 0:
                self.steering_angle -= self.steering_speed * dt
                if self.steering_angle < 0:
                    self.steering_angle = 0
            elif self.steering_angle < 0:
                self.steering_angle += self.steering_speed * dt
                if self.steering_angle > 0:
                    self.steering_angle = 0

        # Kinematic update
        if abs(self.steering_angle) > 1e-4:
            turning_radius = self.wheelbase / math.tan(self.steering_angle)
            angular_velocity = self.velocity / turning_radius
        else:
            angular_velocity = 0
        self.angle += angular_velocity * dt
        self.x += self.velocity * math.cos(self.angle) * dt
        self.y += self.velocity * math.sin(self.angle) * dt

    def handle_input(self, keys):
        # Returns a control dict
        control = {'throttle': 0, 'brake': 0, 'steer': 0, 'handbrake': False}
        if keys.get('w') or keys.get('up'):
            control['throttle'] = 1
        if keys.get('s') or keys.get('down'):
            control['brake'] = 1
        if keys.get('a') or keys.get('left'):
            control['steer'] = -1
        if keys.get('d') or keys.get('right'):
            control['steer'] = 1
        if keys.get('space'):
            control['handbrake'] = True
        return control

    def draw(self, surface):
        # Placeholder: implement drawing logic in your main script
        pass

class Boat(Vehicle):
    def __init__(self, x, y, params):
        super().__init__(x, y)
        self.length = params.get('length', 120)
        self.width = params.get('width', 50)
        self.max_velocity = params.get('max_velocity', 4)
        self.acceleration = params.get('acceleration', 0.1)
        self.friction = params.get('friction', 0.995)
        self.steering_speed = math.radians(params.get('steering_speed_deg', 1.5))
        self.max_steering = math.radians(params.get('max_steering_deg', 25))

    def update(self, control, dt):
        throttle = control.get('throttle', 0)
        steer = control.get('steer', 0)
        # Boat can't reverse, only slow to stop
        if throttle:
            self.velocity += self.acceleration * dt
            if self.velocity > self.max_velocity:
                self.velocity = self.max_velocity
        else:
            self.velocity *= self.friction
            if abs(self.velocity) < 1e-4:
                self.velocity = 0
        # Steering (rudder)
        self.steering_angle += steer * self.steering_speed * dt
        self.steering_angle = max(-self.max_steering, min(self.steering_angle, self.max_steering))
        # Simple boat kinematics: heading changes with steering, but with some lag
        self.angle += self.steering_angle * self.velocity * 0.01 * dt
        self.x += self.velocity * math.cos(self.angle) * dt
        self.y += self.velocity * math.sin(self.angle) * dt

    def handle_input(self, keys):
        control = {'throttle': 0, 'steer': 0}
        if keys.get('w') or keys.get('up'):
            control['throttle'] = 1
        if keys.get('a') or keys.get('left'):
            control['steer'] = -1
        if keys.get('d') or keys.get('right'):
            control['steer'] = 1
        return control

    def draw(self, surface):
        # Placeholder: implement drawing logic in your main script
        pass

class Helicopter(Vehicle):
    def __init__(self, x, y, params):
        super().__init__(x, y)
        self.max_velocity = params.get('max_velocity', 8)
        self.acceleration = params.get('acceleration', 0.2)
        self.friction = params.get('friction', 0.98)
        self.vertical_velocity = 0.0
        self.altitude = params.get('altitude', 0.0)

    def update(self, control, dt):
        throttle = control.get('throttle', 0)
        steer = control.get('steer', 0)
        up = control.get('up', 0)
        down = control.get('down', 0)
        # Forward/backward
        if throttle:
            self.velocity += self.acceleration * dt
            if self.velocity > self.max_velocity:
                self.velocity = self.max_velocity
        else:
            self.velocity *= self.friction
            if abs(self.velocity) < 1e-4:
                self.velocity = 0
        # Yaw (turn)
        self.angle += steer * 0.04 * dt
        self.x += self.velocity * math.cos(self.angle) * dt
        self.y += self.velocity * math.sin(self.angle) * dt
        # Altitude
        if up:
            self.vertical_velocity += self.acceleration * dt
        if down:
            self.vertical_velocity -= self.acceleration * dt
        self.altitude += self.vertical_velocity * dt
        # Simulate drag
        self.vertical_velocity *= 0.98
        if self.altitude < 0:
            self.altitude = 0
            self.vertical_velocity = 0

    def handle_input(self, keys):
        control = {'throttle': 0, 'steer': 0, 'up': 0, 'down': 0}
        if keys.get('w') or keys.get('up'):
            control['throttle'] = 1
        if keys.get('a') or keys.get('left'):
            control['steer'] = -1
        if keys.get('d') or keys.get('right'):
            control['steer'] = 1
        if keys.get('space'):
            control['up'] = 1
        if keys.get('s'):
            control['down'] = 1
        return control

    def draw(self, surface):
        # Placeholder: implement drawing logic in your main script
        pass
