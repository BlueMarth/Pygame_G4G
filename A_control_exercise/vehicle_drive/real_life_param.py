"""real_life_param.py

Physical constants and simple environment-model helper functions.

This module provides:
- common constants (gravity, standard sea-level air density/pressure, water density)
- functions to compute how air density, pressure and temperature vary with altitude
- a simple function for water density vs temperature and salinity

The formulas are intentionally simple (standard atmosphere / exponential approximations)
and are suitable for use in educational simulations. They are not replacements for
high-precision meteorological models.

Example:
    from vehicle_drive.real_life_param import rho_air_at_altitude, G
    rho = rho_air_at_altitude(1500)  # air density at 1500 m

"""

import math

# Fundamental constants
G = 9.80665  # m/s^2, standard gravity
R = 287.05  # J/(kg·K), specific gas constant for dry air

# Standard sea-level conditions (ICAO / ISA)
P0 = 101325.0  # Pa
T0 = 288.15    # K (15 °C)
RHO_AIR_0 = 1.225  # kg/m^3 (air density at sea level)

# Water
RHO_WATER_FRESH_20C = 998.2071  # kg/m^3 at 20 °C (fresh water)
RHO_SEA_WATER = 1025.0  # kg/m^3 approximate average seawater


def temperature_at_altitude(h_m, lapse_rate=-0.0065):
    """Return approximate temperature (K) at altitude h_m (meters) using ISA lapse rate.

    Default lapse_rate is -6.5 K/km (troposphere). For altitudes above the
    troposphere this simple model will be inaccurate.
    """
    return T0 + lapse_rate * h_m


def pressure_at_altitude(h_m):
    """Return approximate air pressure (Pa) at altitude h_m using the barometric formula
    assuming a constant lapse rate in the troposphere.
    """
    # limit to troposphere (where the lapse-rate formula is valid) ~ 11 km
    h = max(min(h_m, 11000.0), 0.0)
    T = temperature_at_altitude(h)
    # barometric formula with constant lapse rate
    exponent = -G / (R * -0.0065)
    return P0 * (T / T0) ** exponent


def rho_air_at_altitude(h_m):
    """Return approximate air density (kg/m^3) at altitude h_m.

    Uses ideal gas law rho = p / (R * T) with the simplified ISA pressure/temperature.
    """
    p = pressure_at_altitude(h_m)
    T = temperature_at_altitude(max(min(h_m, 11000.0), 0.0))
    rho = p / (R * T)
    return rho


def speed_of_sound_at_altitude(h_m):
    """Approximate speed of sound (m/s) at altitude using a dry-air relation: sqrt(gamma * R * T).
    gamma (ratio of specific heats) for air ~ 1.4
    """
    gamma = 1.4
    T = temperature_at_altitude(h_m)
    return math.sqrt(gamma * R * T)


def rho_water(temperature_c=20.0, salinity_ppt=0.0):
    """Approximate water density (kg/m^3) as a function of temperature (°C) and salinity (ppt).

    This is a simple empirical approximation good for demonstration. For higher
    accuracy use UNESCO equations (TEOS-10 / EOS-80). Salinity is in parts per thousand.
    """
    # Basic temperature effect (empirical): density decreases with temperature
    # Use a simple quadratic fit around 4 °C (maximum density for fresh water)
    t = temperature_c
    # freshwater density approximation (kg/m^3)
    rho_f = 999.842594 + 6.793952e-2 * t - 9.09529e-3 * t**2 + 1.001685e-4 * t**3 - 1.120083e-6 * t**4 + 6.536332e-9 * t**5
    # salinity correction (rough linear scaling)
    rho = rho_f + 0.824493 * salinity_ppt
    return rho


if __name__ == "__main__":
    # quick sanity checks / demo values
    for alt in (0, 1000, 5000, 10000):
        print(f"alt={alt:5d} m: rho={rho_air_at_altitude(alt):.3f} kg/m^3, p={pressure_at_altitude(alt):.0f} Pa, T={temperature_at_altitude(alt):.1f} K")
    print("water @20C fresh:", rho_water(20.0, 0.0))
