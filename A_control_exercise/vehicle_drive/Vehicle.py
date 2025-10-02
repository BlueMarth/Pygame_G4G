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
        self.rear_bumper_offset = params.get('rear_bumper_offset', 10)  # distance from rear axle to rear bumper
        self._check_geometry()

    def _check_geometry(self):
        if self.wheelbase + self.rear_bumper_offset > self.length:
            raise ValueError(f"Invalid car geometry: wheelbase + rear_bumper_offset ({self.wheelbase} + {self.rear_bumper_offset}) exceeds car length ({self.length})")

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

        # --- Tail-driven kinematics ---
        # The stern (tail) is the point being moved by the velocity vector
        # The boat rotates about a point near the bow (front)
        L = self.length
        # Calculate stern (tail) position based on current center and angle
        stern_x = self.x - (L/2) * math.cos(self.angle)
        stern_y = self.y - (L/2) * math.sin(self.angle)
        # Move stern forward
        stern_x += self.velocity * math.cos(self.angle) * dt
        stern_y += self.velocity * math.sin(self.angle) * dt
        # Update heading: rotate about a point near the bow
        # The turn center is at the bow, so the angular velocity is proportional to steering and velocity
        # The 0.01 factor is a tunable parameter for rudder effectiveness
        bow_turn_factor = 0.01
        self.angle += self.steering_angle * self.velocity * bow_turn_factor * dt
        # Recompute center position from new stern position and heading
        self.x = stern_x + (L/2) * math.cos(self.angle)
        self.y = stern_y + (L/2) * math.sin(self.angle)

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
        self.drag = params.get('drag', 0.98)  # replaces friction
        self.vertical_velocity = 0.0
        self.altitude = params.get('altitude', 0.0)
        self.lift = params.get('lift', 0.2)  # replaces vertical_acceleration
        self.max_altitude = params.get('max_altitude', 1000)
        self.ground_effect_strength = params.get('ground_effect_strength', 1.5)  # multiplier near ground
        self.lift_decay_rate = params.get('lift_decay_rate', 2.0)  # exponential decay rate

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
            self.velocity *= self.drag
            if abs(self.velocity) < 1e-4:
                self.velocity = 0
        # Yaw (turn)
        self.angle += steer * 0.04 * dt
        self.x += self.velocity * math.cos(self.angle) * dt
        self.y += self.velocity * math.sin(self.angle) * dt
        # --- Vertical motion with lift, drag, and ground effect ---
        # Ground effect: stronger lift near ground, decays concavely (slow at first, fast near max altitude)
        # Effective lift = base_lift * (1 + ground_effect_strength * exp(-((1 - (altitude/max_altitude)) ** lift_decay_rate)))
        if self.max_altitude > 0:
            norm_alt = min(max(self.altitude / self.max_altitude, 0), 1)
        else:
            norm_alt = 0
        ground_effect = self.ground_effect_strength * math.exp(-((1 - norm_alt) ** self.lift_decay_rate))
        effective_lift = self.lift * (1 + ground_effect)
        # Up/down controls
        if up:
            self.vertical_velocity += effective_lift * dt
        if down:
            self.vertical_velocity -= effective_lift * dt
        self.altitude += self.vertical_velocity * dt
        # Simulate vertical drag
        self.vertical_velocity *= self.drag
        if self.altitude < 0:
            self.altitude = 0
            self.vertical_velocity = 0
        if self.altitude > self.max_altitude:
            self.altitude = self.max_altitude
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
            control['throttle'] = -1
        # Double-tap and hold space for descend
        if keys.get('descend'):
            control['down'] = 1
        return control

    def draw(self, surface):
        # Placeholder: implement drawing logic in your main script
        pass
