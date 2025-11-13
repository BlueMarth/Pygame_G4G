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
    def __init__(self, x, y, z, angle, params):
        super().__init__(x, y, z, angle)
        self.z = z
        self.angle = angle
        self.mass = params.get('mass', 1.0)
        self.drag_coeff = params.get('drag_coeff', 0.3)
        self.lift_force = params.get('lift_force', 0.5)
        self.roll_force = params.get('roll_force', 0.15)
        self.pitch_force = params.get('pitch_force', 0.2)
        self.yaw_force = params.get('yaw_force', 0.1)
        self.vx, self.vy, self.vz = 0.0, 0.0, 0.0
        self.ang_vel = 0.0

        # self.max_velocity = params.get('max_velocity', 8)
        # self.acceleration = params.get('acceleration', 0.2)
        # self.drag = params.get('drag', 0.98)  # replaces friction
        # self.vertical_velocity = 0.0
        # self.altitude = params.get('z', 0.0)
        # self.lift = params.get('lift', 0.2)  # replaces vertical_acceleration
        # self.max_altitude = params.get('max_altitude', 1000)
        # self.ground_effect_strength = params.get('ground_effect_strength', 1.5)  # multiplier near ground
        # self.lift_decay_rate = params.get('lift_decay_rate', 2.0)  # exponential decay rate

    def update(self, control, dt):
        # get control inputs
        lift = control.get('lift', 0)
        pitch = control.get('pitch', 0)
        roll = control.get('roll', 0)
        yaw = control.get('yaw', 0)
        # compute drag
        self.hor_speed = math.sqrt(self.vx**2 + self.vy**2)
        self.hor_drag = 0.5 * self.drag_coeff * self.hor_speed**2 / self.mass
        self.ver_drag = 0.5 * self.drag_coeff * self.vz**2 / self.mass
        # compute lift force
        self.lift_force = self.lift_force

        # compute acceleration
        # self.rol_acc = (self.roll_force - self.hor_drag) / self.mass
        # self.pit_acc = (self.pitch_force - self.hor_drag) / self.mass
        # self.yaw_acc = (self.yaw_force - self.hor_drag) / self.mass
        # self.ver_acc = (self.lift_force - self.ver_drag) / self.mass
        self.rol_acc = 0.1
        self.pit_acc = 0.1
        self.yaw_acc = 0.1
        self.ver_acc = 0.1
        # # compute max velocities
        # self.max_rol_vel = math.sqrt((2 * self.roll_force) / self.drag_coeff)
        # self.max_pit_vel = math.sqrt((2 * self.pitch_force) / self.drag_coeff)
        # self.max_yaw_vel = math.sqrt((2 * self.yaw_force) / self.drag_coeff)
        # self.max_ver_vel = math.sqrt((2 * self.lift_force) / self.drag_coeff)
        
        ''' foreaft velocity '''
        if pitch > 0: # move forward
            self.vx += self.pit_acc * dt
        elif pitch < 0: # move backward
            self.vx -= self.pit_acc * dt
        else:
            self.vx *= self.hor_drag
            if abs(self.vx) < 1e-4:
                self.vx = 0
        '''sideways velocity'''
        if roll > 0: # move right
            self.vy += self.rol_acc * dt
        elif roll < 0: # move left
            self.vy -= self.rol_acc * dt
        else:
            self.vy *= self.hor_drag
            if abs(self.vy) < 1e-4:
                self.vy = 0
        ''' turning velocity'''
        if yaw > 0: # turn right
            self.ang_vel += self.yaw_acc * dt
        elif yaw < 0: # turn left
            self.ang_vel -= self.yaw_acc * dt
        else:
            self.ang_vel *= self.hor_drag
            if abs(self.ang_vel) < 1e-4:
                self.ang_vel = 0
        ''' vertical velocity '''
        if lift > 0: # up
            self.vz += self.ver_acc * dt
        elif lift < 0: # down
            self.vz -= self.ver_acc * dt
        ''' position and heading update'''
        self.x += self.vx * math.cos(self.angle) * dt - self.vy * math.sin(self.angle) * dt
        self.y += self.vx * math.sin(self.angle) * dt + self.vy * math.cos(self.angle) * dt
        self.z += self.vz * dt
        self.angle += self.ang_vel * dt

    
    def handle_input(self, keys):
        control = {'lift': 0, 'pitch': 0, 'roll': 0, 'yaw': 0}
        if keys.get('space'):
            control['lift'] = 1         # go up
        if keys.get('Lshift'):
            control['lift'] = -1        # go down
        if keys.get('w'):
            control['pitch'] = 1        # forward
        if keys.get('s'):
            control['pitch'] = -1       # backward
        if keys.get('d'):
            control['roll'] = 1         # slide right
        if keys.get('a'):
            control['roll'] = -1        # slide left
        if keys.get('e'):
            control['yaw'] = 1          # turn right
        if keys.get('q'):
            control['yaw'] = -1         # turn left
        return control

    def draw(self, surface):
        # Placeholder: implement drawing logic in your main script
        pass
