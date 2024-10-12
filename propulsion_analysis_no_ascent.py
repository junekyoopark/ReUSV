import math

# Constants
g = 32.174  # gravitational constant in ft/s^2

# Define the function to calculate the required thrusts
def thrust_requirements(W_entry, L_f):
    T_req_oms = W_entry / 16
    T_req_qp = 870 * W_entry * L_f / (147141 * 143)
    T_req_qv = 50 * W_entry * L_f / (147141 * 143)
    return T_req_oms, T_req_qp, T_req_qv

# Define the function to calculate the OMS propellant weight for different phases
def oms_propellant_weight(W_entry, deltaV, Isp_oms):
    return W_entry * (math.exp(deltaV / (Isp_oms * g)) - 1)

# Define the function to calculate total OMS propellant weight with a 10% reserve
def total_oms_propellant(W_entry, deltaV_orbit, deltaV_deorbit, Isp_oms):
    W_oms_prop_orbit = oms_propellant_weight(W_entry, deltaV_orbit, Isp_oms)
    W_oms_prop_deorbit = oms_propellant_weight(W_entry, deltaV_deorbit, Isp_oms)
    
    # Add 10% reserve propellant
    W_oms_prop_total = 1.1 * (W_oms_prop_orbit + W_oms_prop_deorbit)
    return W_oms_prop_orbit, W_oms_prop_deorbit, W_oms_prop_total

# Define the function to calculate RCS propellant weight
def rcs_propellant_weight(W_entry, deltaV, Isp_rcs):
    return W_entry * (math.exp(deltaV / (Isp_rcs * g)) - 1)

# Define the function to calculate total RCS propellant weight with a 10% reserve
def total_rcs_propellant(W_entry, deltaV_entry, deltaV_orbit, Isp_rcs):
    W_rcs_prop_entry = rcs_propellant_weight(W_entry, deltaV_entry, Isp_rcs)
    W_rcs_prop_orbit = rcs_propellant_weight(W_entry, deltaV_orbit, Isp_rcs)
    
    # Add 10% reserve propellant
    W_rcs_prop_total = 1.1 * (W_rcs_prop_entry + W_rcs_prop_orbit)
    return W_rcs_prop_entry, W_rcs_prop_orbit, W_rcs_prop_total

# Define the function to calculate the total propellant weights and oxygen/fuel split
def total_propellant_weights(W_oms_prop_total, W_rcs_prop_total):
    W_prop_total = W_oms_prop_total + W_rcs_prop_total
    W_oms_ox = 6/7 * W_oms_prop_total
    W_oms_fuel = 1/7 * W_oms_prop_total
    W_rcs_ox = 4/5 * W_rcs_prop_total
    W_rcs_fuel = 1/5 * W_rcs_prop_total
    W_ox_total = W_oms_ox + W_rcs_ox
    W_fuel_total = W_oms_fuel + W_rcs_fuel
    return W_prop_total, W_ox_total, W_fuel_total

# Inputs
W_entry = 8500  # Entry weight in lbs
L_f = 27.5       # Fuselage length in feet
Isp_oms = 246    # Specific impulse for OMS (in seconds) 246
Isp_rcs = 265    # Specific impulse for RCS (in seconds)
deltaV_oms_orbit = 2177.4934  # Delta V for orbit in fps (paper says 50, calculated by ours for one year is 2177.4934)
deltaV_oms_deorbit = 293.0675853  # Delta V for de-orbit in fps (Calculated by 임태욱-GNC)
deltaV_rcs_entry = 40     # Delta V for RCS entry in fps
deltaV_rcs_orbit = 200    # Delta V for RCS orbit in fps

# Calculate thrust requirements
T_req_oms, T_req_qp, T_req_qv = thrust_requirements(W_entry, L_f)
print(f"Required thrust for OMS: {T_req_oms:.2f} lbs")
print(f"Required thrust for primary RCS: {T_req_qp:.2f} lbs")
print(f"Required thrust for vernier RCS: {T_req_qv:.2f} lbs")

# Calculate OMS propellant weights
W_oms_prop_orbit, W_oms_prop_deorbit, W_oms_prop_total = total_oms_propellant(
    W_entry, deltaV_oms_orbit, deltaV_oms_deorbit, Isp_oms)
print(f"OMS Propellant weight for orbit: {W_oms_prop_orbit:.2f} lbs")
print(f"OMS Propellant weight for de-orbit: {W_oms_prop_deorbit:.2f} lbs")
print(f"Total OMS Propellant weight (with reserve): {W_oms_prop_total:.2f} lbs")

# Calculate RCS propellant weights
W_rcs_prop_entry, W_rcs_prop_orbit, W_rcs_prop_total = total_rcs_propellant(
    W_entry, deltaV_rcs_entry, deltaV_rcs_orbit, Isp_rcs)
print(f"RCS Propellant weight for entry: {W_rcs_prop_entry:.2f} lbs")
print(f"RCS Propellant weight for orbit: {W_rcs_prop_orbit:.2f} lbs")
print(f"Total RCS Propellant weight (with reserve): {W_rcs_prop_total:.2f} lbs")

# Calculate total propellant, oxygen, and fuel weights
W_prop_total, W_ox_total, W_fuel_total = total_propellant_weights(W_oms_prop_total, W_rcs_prop_total)
print(f"Total propellant weight: {W_prop_total:.2f} lbs")
print(f"Total oxygen weight: {W_ox_total:.2f} lbs")
print(f"Total fuel weight: {W_fuel_total:.2f} lbs")
