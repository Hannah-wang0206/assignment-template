import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Settings page configuration
st.set_page_config(layout="wide", page_title="Rocket Δv Calculator")

# Streamlit
st.title("Rocket Δv Calculator 🚀")

# User input
st.subheader("🚀 Rocket Parameters")
initial_mass = st.slider("Initial mass of the rocket (in kg)", 1000.0, 100000.0, 10000.0, key="initial_mass")
exhaust_velocity = st.slider("Exhaust velocity (in m/s)", 1000.0, 5000.0, 3000.0, key="exhaust_velocity")
burn_time = st.slider("Burn time (in seconds)", 10.0, 3600.0, 600.0, key="burn_time")

# Define the proportion of propellant mass to the initial mass
propellant_mass_fraction = 0.9

# Calculate the final velocity change of the rocket (Δv)
def calculate_deltav(initial_mass, exhaust_velocity, propellant_mass_fraction):
    propellant_mass = initial_mass * propellant_mass_fraction
    initial_mass_without_propellant = initial_mass - propellant_mass
    deltav = exhaust_velocity * np.log(initial_mass / initial_mass_without_propellant)
    return deltav

deltav = calculate_deltav(initial_mass, exhaust_velocity, propellant_mass_fraction)

# Show the results
st.subheader("# Results")
st.write(f"The final velocity change (Δv) of the rocket is: {deltav:.2f} m/s")

# Visualization
st.subheader("🎯 Visualization")
time = np.linspace(0, burn_time, 100)  # Array of time points
velocity = np.zeros_like(time)  # Array of initial velocities

# Simulate the rocket acceleration process
for t in range(1, len(time)):
    propellant_mass_used = propellant_mass_fraction * initial_mass * t / burn_time
    current_mass = initial_mass - propellant_mass_used
    thrust = exhaust_velocity * propellant_mass_used / burn_time
    accel = thrust / current_mass
    velocity[t] = velocity[t-1] + accel * (time[t] - time[t-1])

fig, ax = plt.subplots()
ax.plot(time, velocity)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Velocity (m/s)')
ax.set_title('Rocket Velocity Over Time')
st.pyplot(fig)

# Real-time feedback
if st.button("Recalculate"):
    # Recalculate and update the results
    deltav = calculate_deltav(initial_mass, exhaust_velocity, propellant_mass_fraction)
    st.write(f"Updated final velocity change (Δv): {deltav:.2f} m/s")
    # Resimulate the rocket acceleration process
    for t in range(1, len(time)):
        propellant_mass_used = propellant_mass_fraction * initial_mass * t / burn_time
        current_mass = initial_mass - propellant_mass_used
        thrust = exhaust_velocity * propellant_mass_used / burn_time
        accel = thrust / current_mass
        velocity[t] = velocity[t-1] + accel * (time[t] - time[t-1])
    fig, ax = plt.subplots()
    ax.plot(time, velocity)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Velocity (m/s)')
    ax.set_title('Updated Rocket Velocity Over Time')
    st.pyplot(fig)