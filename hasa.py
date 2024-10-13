import math

print("")
print("MODIFIED HASA TEST by JKP")
print("ORIGINAL HASA: https://ntrs.nasa.gov/api/citations/19890005736/downloads/19890005736.pdf")
print("Modified HASA: https://s-space.snu.ac.kr/handle/10371/196316")
print("X-37B dimensions are used; if certain dimensions aren't available online,")
print("they are estimated from a fairly accurate CAD model.")
print("")


# Inputs for fuselage length (L_f), ULF, q_max, S_btot, V_tot, and mf in imperial units
L_f = 27.5  # ft (fuselage length) (X-37B)
ULF = 3.75   # ultimate load factor (given in MERS by GATech)
q_max = 300  # lb per ft^2 (psf) (maximum dynamic pressure) (Suitable number for RLVs like X-33, X-37, X-40, etc.)
# source: "High-fidelity real-time trajectory optimization for reusable launch vehicles" by Bollino, Kevin P.
S_btot = 926.66504777 # ft^2 (fuselage wetted surface area) (estimate from CAD model of X-37B)
V_tot = 604.23394760467  # ft^3 (total volume) (estimate from CAD model of X-37B)
mf = 1.12       # mass factor (mass factor of space shuttle)

# Inputs for W_gtot, W_prop, ULF, S_ref, AR, taper_ratio, t/c, sweep_angle, and mf
W_gtot = 11000  # total gross weight in lbs #X-37B: 11000lb 
W_prop = 2865.13   # propellant weight in lbs #arbitrarily set from SNU paper (3306.934lbs)
S_ref = 80   # reference wing area in square feet # estimate from CAD model (59.35220204 for wing interrupted by fuselage)
W_span = 14.92782 #ft 
AR = (W_span**2) / 59.35220204      # aspect ratio (wing_span^2 / wing_area) estimate from CAD model (14.92782**2 / 59.35220204)
taper_ratio = 383/4059  # taper ratio (λ) (length_tip/length_root) estimate from CAD model (383/4059) 
t_c = 154/3426      # thickness to chord ratio (t/c) estimate from CAD model (154/3426)
sweep_angle = 50  # sweep angle (λ_1/2) in degrees (estimate from CAD model)
# ULF = 3.75       # ultimate load factor (same as above)
# mf = 1.12        # mass factor (same as above)

# Inputs for tail weights
# Unsure what to do with a V tail like the X-37B,
# So just guestimated a vertical and horizontal planform area.
# If I have more time, Maybe I'll do a projection to each plane and get the surface area
S_wfh = 25.0  # planform area of horizontal stabilizer in square feet (estimate from CAD model)
S_wfv = 25.0  # planform area of vertical stabilizer in square feet (estimate from CAD model)

# TPS Surface Areas (estimate)
# 100 ft^2 for HRSI (under wing, etc.) estimate from CAD model of X-37B
# 20 ft^2 for RCC (nose and leading edge) estimate from CAD model of X-37B
# 119 ft^2 for FRSI (top part of spacecraft) estimate from CAD model of X-37B
HRSI_area = 100
RCC_area = 20
FRSI_area = 119

## TPS UNIT WEIGHT PER UNIT AREA ARE UNKNOWN, 
# SO WE USE THE AVERAGE OF 3.0 USED FOR THE SPACE SHUTTLE##
W_ins = 3.0

# Inputs for surface control actuators
W_entry = 8800 #lbs (Note that the same is used in Propulsion Analysis)


# Landing Gear Assumption
# Assumes Residual Fuel is 20% (20% fuel is left)
# The 20% residual fuel is arbitrary, 
# so you can change this however you like.
fuel_residual = 0.2

# Inputs for OMS engine weight
T_req_oms = 550.00  # Required OMS thrust in lbs (From Propulsion Analysis)
P_oms_press = 3000  # OMS pressurization pressure in psia (from MERS by GATech)
V_oms_ox = 31.77  # Volume of OMS oxygen in cubic feet (From Propulsion Analysis)
V_oms_fuel = 85.44  # Volume of OMS fuel in cubic feet (From Propulsion Analysis)
V_oms_press = 0.24 * (V_oms_ox + V_oms_fuel)  # OMS pressurization volume (From MERS by GATech)

# Inputs for RCS engine weight
N_pf, N_vf, N_pa, N_va = 14, 2, 24, 4  # Number of primary/vernier thrusters (front/aft) (Space Shuttle quantity)
T_req_qp, T_req_qv = 10.01, 0.58  # Required primary and vernier thrust (lbs) (From Propulsion Analysis)
R_p, R_v = 39.5, 9.4  # Thrust-to-weight ratios for primary/vernier thrusters (from MERS by GATech)
P_rcs_press = 3000  # RCS pressurization pressure in psia (from MERS by GATech)
V_rcs_ox = 2.82 # Volume of RCS oxygen(cubic feet) (From Propulsion Analysis)
V_rcs_fuel = 7.58  # Volume of RCS fuel (cubic feet) (From Propulsion Analysis)
V_rcs_press = 0.24 * (V_rcs_ox + V_rcs_fuel)  # RCS pressurization volume (From MERS by GATech)

# Inputs for tank weight
ullage_lox = 0.06 #LOX 6% value is from X-34 "Transient Analysis of X-34 Pressurization System"
ullage_lh2 = 0.06 #No source for this, but MERS by GATech says typically ~4 to 5% so 6% should be a reasonable value
P_oms_tnk = 195  # Pressure of OMS tank in psia (from MERS by GATech)
V_oms_tnk = (V_oms_ox/(1-0.06) + V_oms_fuel/(1-0.06))  # Volume of OMS tank in cubic feet
P_rcs_tnk = 195  # Pressure of RCS tank in psia (from MERS by GATech)
V_rcs_tnk = (V_rcs_ox/(1-0.06) + V_rcs_fuel/(1-0.06))   # Volume of RCS tank in cubic feet
print(V_oms_tnk)

print(V_rcs_tnk)

# # Additional input for total weight (from propulsion analysis)
# W_prop = 2865.13 #lbs (from Propulsion Analysis)

###########################
# HASA MODEL (INCOMPLETE) #
###########################


# Note that all outputs for functions are in imperial units
# Fuselage weight
def fuselage_weight_func(L_f, ULF, q_max, S_btot, V_tot, mf, eta_vol=0.7):
    # Note that eta_vol is typically 0.7 and the HASA model isn't sensitive to it
    # Equation for body equivalent diameter (D_be)
    D_be = math.sqrt((4 * V_tot) / (math.pi * L_f * eta_vol))
    
    # Equation for sigma (σ) in imperial units
    sigma = abs(((L_f * ULF / D_be) ** 0.15) * (q_max ** 0.16) * (S_btot ** 1.05))
    
    # Equation for fuselage weight (W_f)
    W_f = 0.341 * mf * (sigma ** 1.0)  # Result will be in pounds (lb)
    return W_f

# Main wing weight
def wing_weight_func(W_gtot, W_prop, ULF, S_ref, AR, taper_ratio, t_c, sweep_angle, mf):
    # Calculate empty weight (W_emp)
    W_emp = W_gtot - W_prop

    # Equation for wing weight (W_w)
    term1 = ((W_emp * ULF / 1000) ** 0.52)
    term2 = (S_ref ** 0.7) * (AR ** 0.47)
    term3 = ((1 + taper_ratio) / t_c) ** 0.4
    term4 = (0.3 + (0.7 / math.cos(math.degrees(sweep_angle))))
    
    W_w = 0.2958 * mf * (term1 * term2 * term3 * term4) ** 1.017
    
    return W_w

# Horizontal stabilizer weight
def horizontal_stabilizer_weight_func(W_gtot, S_ref, S_wfh, q_max):
    # Calculate the Λ term
    Lambda = ((W_gtot / S_ref) ** 0.6) * (S_wfh ** 1.2) * (q_max ** 0.8)
    
    # Equation for horizontal stabilizer weight (W_finh)
    W_finh = 0.0035 * Lambda
    
    return W_finh

# Vertical stabilizer weight
def vertical_stabilizer_weight_func(S_wfv):
    # Equation for vertical stabilizer weight (W_finv)
    W_finv = 5.0 * (S_wfv ** 1.09)
    
    return W_finv

#TPS weight
def tps_weight_func(W_ins, HRSI_area, RCC_area, FRSI_area):
    W_tps = W_ins * (HRSI_area + RCC_area + FRSI_area)
    return W_tps

#Landing gear weight
def landing_gear_weight_func(W_gtot, fuel_residual, W_prop):
    W_land = W_gtot - ((1.0-fuel_residual)*W_prop)
    print(W_land)
    W_gear = 0.030 * W_land
    return W_gear

#Total STRUCTURE weight
def structure_weight_func(W_f, W_w, W_hor, W_vert, W_tps, W_gear):
    W_str = W_f+W_w+W_hor+W_vert+W_tps+W_gear
    return W_str



###### INCOMPLETE STUFF ######

####Engine Weight (From MERS by GATech)
# OMS Engine Weight Calculation
def oms_engine_weight_func(T_req_oms, R_oms=22): #R_oms chosen as 22; includes mounts, supports, igniters, etc. (MERS by GATech)
    """Calculates the OMS engine weight."""
    W_oms_eng = T_req_oms / R_oms
    return W_oms_eng

# OMS Pressurization System Weight Calculation
def oms_pressurization_weight_func(P_oms_press, V_oms_press, V_oms_ox, V_oms_fuel, TRF=0.0):
    """Calculates the OMS pressurization system weight."""
    W_oms_press = (0.0143 * P_oms_press * V_oms_press * (1 - TRF) +
                   0.617 * (V_oms_ox + V_oms_fuel))
    return W_oms_press

# OMS Installation Weight Calculation
def oms_installation_weight_func(W_oms_eng):
    """Calculates the OMS installation weight."""
    W_oms_install = 0.74 * W_oms_eng
    return W_oms_install

# Total OMS Weight Calculation
def total_oms_weight_func(W_oms_eng, W_oms_install, W_oms_press):
    """Calculates the total OMS weight."""
    W_oms = W_oms_eng + W_oms_install + W_oms_press
    return W_oms

# RCS Thruster Weight Calculations
def rcs_thruster_weight_func(N, T_req, R):
    """Calculates the weight of RCS thrusters."""
    return N * T_req / R

# RCS Pressurization System Weight Calculation
def rcs_pressurization_weight_func(P_rcs_press, V_rcs_press, V_rcs_ox, V_rcs_fuel, TRF=0.0):
    """Calculates the RCS pressurization system weight."""
    W_rcs_press = (0.0143 * P_rcs_press * V_rcs_press * (1 - TRF) +
                   0.617 * (V_rcs_ox + V_rcs_fuel))
    return W_rcs_press

# RCS Installation Weight Calculation
def rcs_installation_weight_func(W_rcs_thrusters):
    """Calculates the RCS installation weight."""
    W_rcs_install = 0.74 * sum(W_rcs_thrusters)
    return W_rcs_install

# Total RCS Weight Calculation
def total_rcs_weight_func(W_rcs_thrusters, W_rcs_install, W_rcs_press):
    """Calculates the total RCS weight."""
    W_rcs = sum(W_rcs_thrusters) + W_rcs_install + W_rcs_press
    return W_rcs

# Total Engine Weight Calculation
def total_engine_weight_func(W_oms, W_rcs):
    """Calculates the total engine weight."""
    W_eng = W_oms + W_rcs
    return W_eng

# Tank Weight Calculation for OMS and RCS
def tank_weight_func(P_tnk, V_tnk):
    """Calculates the weight of the tank."""
    return 0.01295 * P_tnk * V_tnk

# Total Tank Weight Calculation
def total_tank_weight_func(P_oms_tnk, V_oms_tnk, P_rcs_tnk, V_rcs_tnk):
    """Calculates the total weight of all tanks (OMS + RCS)."""
    W_oms_tnk = tank_weight_func(P_oms_tnk, V_oms_tnk)
    W_rcs_tnk = tank_weight_func(P_rcs_tnk, V_rcs_tnk)
    W_tnk = W_oms_tnk + W_rcs_tnk
    return W_oms_tnk, W_rcs_tnk, W_tnk

# Total Propulsion Weight Calculation
def total_propulsion_weight_func(W_tnk, W_eng):
    """Calculates the total propulsion weight."""
    return W_tnk + W_eng

# # Hydraulics Weight is removed since X-37B uses electromechanical actuators instead.
# def hydraulics_weight_func(S_ref, q_max, L_f, W_span):
#     # Calculate the psi term
#     psi = abs(((S_ref*q_max/1000)**0.334) * (L_f+W_span)**0.5)
    
#     # Equation for hydraulics weight (W_hydr)
#     W_hydr = 2.64 * (psi ** 1.0)
    
#     return W_hydr

# Electromechanical Actuators
def surface_control_actuators_weight_func(W_entry):
    W_sca = 0.0048*W_entry
    return W_sca

# Avionics Weight
# This is MODIFIED HASA!!!
# AVIONICS WEIGHT IS REDUCED TO 69% of ORINAL HASA!
# This is due to advanced avionics
def avionics_weight_func(W_gtot):
    W_tavcs = 0.69*66.37*(W_gtot**0.361)
    return W_tavcs


# Electrical System Weight
def electrical_weight_func(W_gtot, L_f):
    phi = abs((W_gtot**0.5) * (L_f**0.25))
    W_eps = 1.167 * (phi**1.0)
    return W_eps


####Total weight without payload (W_no_payload)
def total_weight_without_payload_func(W_str, W_pros, W_sub, W_prop):
    W_gtot_no_payload = W_str + W_pros + W_sub + W_prop
    return W_gtot_no_payload

#################
# RUN THE MODEL #
#################
# Calculate the fuselage weight
fuselage_weight = fuselage_weight_func(L_f, ULF, q_max, S_btot, V_tot, mf)
fuselage_weight_metric = fuselage_weight*0.45359237

# Calculate the wing weight using inputs above
wing_weight = wing_weight_func(W_gtot, W_prop, ULF, S_ref, AR, taper_ratio, t_c, sweep_angle, mf)
wing_weight_metric = wing_weight * 0.45359237

# Calculate the horizontal stabilizer weight
horizontal_weight = horizontal_stabilizer_weight_func(W_gtot, S_ref, S_wfh, q_max)

# Calculate the vertical stabilizer weight
vertical_weight = vertical_stabilizer_weight_func(S_wfv)

# Calculate the total tail wing weight
horizontal_weight_metric = horizontal_weight * 0.45359237  # Convert to kg
vertical_weight_metric = vertical_weight * 0.45359237  # Convert to kg
total_tail_wing_weight_metric = horizontal_weight_metric+vertical_weight_metric

# Calculate the TPS weight
TPS_weight = tps_weight_func(W_ins, HRSI_area, RCC_area, FRSI_area)
TPS_weight_metric = TPS_weight*0.45359237  # Convert to kg

# Calculate the landing gear weight
landing_gear_weight = landing_gear_weight_func(W_gtot, fuel_residual, W_prop)
landing_gear_weight_metric = landing_gear_weight*0.45359237

# Total STRUCTURE weight
structure_weight = structure_weight_func(fuselage_weight, wing_weight, horizontal_weight, vertical_weight, TPS_weight, landing_gear_weight)
structure_weight_metric  = structure_weight*0.45359237
print(f"Fuselage Weight in kg: {fuselage_weight_metric:.2f} kg")
print(f"Wing Weight in kg: {wing_weight_metric:.2f} kg")
print(f"Total Tail Wing Weight in kg: {total_tail_wing_weight_metric:.2f} kg")
print(f"TPS Weight in kg: {TPS_weight_metric:.2f} kg")
print(f"Landing Gear Weight in kg: {landing_gear_weight_metric:.2f} kg")
print("")
print(f"Total Structure Weight in kg: {structure_weight_metric:.2f} kg")
print("")

# hydraulics_weight = hydraulics_weight_func(S_ref, q_max, L_f, W_span)
# hydraulics_weight_metric = hydraulics_weight*0.45359237
surface_actuators_weight = surface_control_actuators_weight_func(W_entry)
surface_actuators_weight_metric = surface_actuators_weight*0.45359237
avionics_weight = avionics_weight_func(W_gtot)
avionics_weight_metric = avionics_weight*0.45359237
electrical_weight = electrical_weight_func(W_gtot,L_f)
electrical_weight_metric = electrical_weight*0.45359237
# Total subsystems weight
W_sub = surface_actuators_weight + avionics_weight + electrical_weight
W_sub_metric = W_sub*0.45359237
print(f"Surface Actuators Weight in kg: {surface_actuators_weight_metric:.2f} kg")
print(f"Avionics Weight in kg: {avionics_weight_metric:.2f} kg")
print(f"Electrical System Weight in kg: {electrical_weight_metric:.2f} kg")
print(f"Total Subsystem Weight in kg: {W_sub_metric:.2f} kg")
print("")

# Calculations for OMS
W_oms_eng = oms_engine_weight_func(T_req_oms)
W_oms_press = oms_pressurization_weight_func(P_oms_press, V_oms_press, V_oms_ox, V_oms_fuel)
W_oms_install = oms_installation_weight_func(W_oms_eng)
W_oms = total_oms_weight_func(W_oms_eng, W_oms_install, W_oms_press)
W_oms_eng_metric = W_oms_eng*0.45359237
W_oms_press_metric = W_oms_press*0.45359237
W_oms_install_metric = W_oms_install*0.45359237
W_oms_metric = W_oms*0.45359237
print(f"OMS Engine Weight in kg: {W_oms_eng_metric:.2f} kg")
print(f"OMS Pressurization Weight in kg: {W_oms_press_metric:.2f} kg")
print(f"OMS Installation Weight in kg: {W_oms_install_metric:.2f} kg")
print(f"Total OMS Weight in kg: {W_oms_metric:.2f} kg")
print("")

# Calculations for RCS
W_rcs_pf = rcs_thruster_weight_func(N_pf, T_req_qp, R_p)
W_rcs_vf = rcs_thruster_weight_func(N_vf, T_req_qv, R_v)
W_rcs_pa = rcs_thruster_weight_func(N_pa, T_req_qp, R_p)
W_rcs_va = rcs_thruster_weight_func(N_va, T_req_qv, R_v)
W_rcs_thrusters = [W_rcs_pf, W_rcs_vf, W_rcs_pa, W_rcs_va]
W_rcs_press = rcs_pressurization_weight_func(P_rcs_press, V_rcs_press, V_rcs_ox, V_rcs_fuel)
W_rcs_install = rcs_installation_weight_func(W_rcs_thrusters)
W_rcs = total_rcs_weight_func(W_rcs_thrusters, W_rcs_install, W_rcs_press)
# print(f"RCS Thruster Weights: {W_rcs_thrusters}")

W_rcs_press_metric = W_rcs_press*0.45359237
W_rcs_install_metric = W_rcs_install*0.45359237
W_rcs_metric = W_rcs*0.45359237

print(f"RCS Pressurization Weight in kg: {W_rcs_press_metric:.2f} kg")
print(f"RCS Installation Weight in kg: {W_rcs_install_metric:.2f} kg")
print(f"Total RCS Weight in kg: {W_rcs_metric:.2f} kg")
print("")

# Total Engine Weight
W_eng = total_engine_weight_func(W_oms, W_rcs)
W_eng_metric = W_eng*0.45359237
print(f"Total Engine Weight in kg: {W_eng_metric:.2f} kg")
print("")

# Calculate Tank Weights
W_oms_tnk, W_rcs_tnk, W_tnk = total_tank_weight_func(P_oms_tnk, V_oms_tnk, P_rcs_tnk, V_rcs_tnk)
W_oms_tnk_metric = W_oms_tnk*0.45359237
W_rcs_tnk_metric = W_rcs_tnk*0.45359237
W_tnk_metric = W_tnk*0.45359237

print(f"OMS Tank Weight in kg: {W_oms_tnk_metric:.2f} kg")
print(f"RCS Tank Weight in kg: {W_rcs_tnk_metric:.2f} kg")
print(f"Total Tank Weight in kg: {W_tnk_metric:.2f} kg")
print("")

# Calculate Total Propulsion Weight
W_pros = total_propulsion_weight_func(W_tnk, W_eng)
W_pros_metric = W_pros*0.45359237
print(f"Total Propulsion Weight in kg: {W_pros_metric:.2f} kg")
print("")

# Calculate total weight WITHOUT payload
W_gtot_without_payload = total_weight_without_payload_func(structure_weight, W_pros, W_sub, W_prop)
W_gtot_without_payload_metric = W_gtot_without_payload*0.45359237
####Total weight without payload (W_no_payload)
print(f"Total Weight WITHOUT Payload in kg: {W_gtot_without_payload_metric:.2f} kg")

# Calculate allowable payload weight
W_allow_payload = W_gtot - W_gtot_without_payload
W_allow_payload_metric = W_allow_payload*0.45359237
print(f"Allowable Payload in kg: {W_allow_payload_metric:.2f} kg")