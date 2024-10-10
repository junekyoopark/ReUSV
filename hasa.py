import math

print("")
print("MODIFIED HASA TEST by JKP")
print("ORIGINAL HASA: https://ntrs.nasa.gov/api/citations/19890005736/downloads/19890005736.pdf")
print("Modified HASA: https://s-space.snu.ac.kr/handle/10371/196316")
print("X-37B dimensions are used; if certain dimensions aren't available online,")
print("they are estimated from a fairly accurate CAD model.")
print("")

# Calculate fuselage weight in imperial units
def fuselage_weight_func(L_f, ULF, q_max, S_btot, V_tot, mf, eta_vol=0.7):
    # Equation for body equivalent diameter (D_be)
    D_be = math.sqrt((4 * V_tot) / (math.pi * L_f * eta_vol))
    
    # Equation for sigma (σ) in imperial units
    sigma = abs(((L_f * ULF / D_be) ** 0.15) * (q_max ** 0.16) * (S_btot ** 1.05))
    
    # Equation for fuselage weight (W_f)
    W_f = 0.341 * mf * (sigma ** 1.0)  # Result will be in pounds (lb)
    return W_f

# Inputs for fuselage length (L_f), ULF, q_max, S_btot, V_tot, and mf in imperial units
L_f = 27.5  # ft (fuselage length) (X-37B)
ULF = 3.75   # ultimate load factor (given in MERS by GATech)
q_max = 120  # lb per ft^2 (psf) (maximum dynamic pressure) (X-37B)
S_btot = 926.66504777 # ft^2 (fuselage wetted surface area) (X-37B)
V_tot = 604.23394760467  # ft^3 (total volume) (X-37B)
mf = 1.12       # mass factor (mass factor of space shuttle)

# Calculate the fuselage weight using inputs above

fuselage_weight = fuselage_weight_func(L_f, ULF, q_max, S_btot, V_tot, mf)
fuselage_weight_metric = fuselage_weight*0.453592

# print(f"Fuselage Weight: {fuselage_weight:.2f} lbs")
print(f"Fuselage Weight in kg: {fuselage_weight_metric:.2f} kg")
############################

# Calculate wing weight in imperial units
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

# Inputs for W_gtot, W_prop, ULF, S_ref, AR, taper_ratio, t/c, sweep_angle, and mf
W_gtot = 11000  # total gross weight in lbs #11000
W_prop = 3306.934   # propellant weight in lbs #3306.934
S_ref = 80   # reference wing area in square feet #59.35220204 for wing interrupted by fuselage)
W_span = 14.92782 #ft
AR = (W_span**2) / 59.35220204      # aspect ratio (wing_span^2 / wing_area) (14.92782**2 / 59.35220204)
taper_ratio = 383/4059  # taper ratio (λ) (length_tip/length_root) (383/4059)
t_c = 154/3426      # thickness to chord ratio (t/c) (154/3426)
sweep_angle = 50  # sweep angle (λ_1/2) in degrees
# ULF = 3.75       # ultimate load factor
# mf = 1.12        # mass factor (adjust as per specific data)

# Calculate the wing weight using inputs above
wing_weight = wing_weight_func(W_gtot, W_prop, ULF, S_ref, AR, taper_ratio, t_c, sweep_angle, mf)
wing_weight_metric = wing_weight * 0.453592

# print(f"Wing Weight: {wing_weight:.2f} lbs")
print(f"Wing Weight in kg: {wing_weight_metric:.2f} kg")
###############

# Define a function to calculate horizontal stabilizer (tail) weight
def horizontal_stabilizer_weight_func(W_gtot, S_ref, S_wfh, q_max):
    # Calculate the Λ term
    Lambda = ((W_gtot / S_ref) ** 0.6) * (S_wfh ** 1.2) * (q_max ** 0.8)
    
    # Equation for horizontal stabilizer weight (W_finh)
    W_finh = 0.0035 * Lambda
    
    return W_finh

# Define a function to calculate vertical stabilizer (tail) weight
def vertical_stabilizer_weight_func(S_wfv):
    # Equation for vertical stabilizer weight (W_finv)
    W_finv = 5.0 * (S_wfv ** 1.09)
    
    return W_finv

# Inputs for tail weights
S_wfh = 25.0  # planform area of horizontal stabilizer in square feet (estimate)
S_wfv = 25.0  # planform area of vertical stabilizer in square feet (estimate)

# Calculate the horizontal stabilizer weight
horizontal_weight = horizontal_stabilizer_weight_func(W_gtot, S_ref, S_wfh, q_max)

# Calculate the vertical stabilizer weight
vertical_weight = vertical_stabilizer_weight_func(S_wfv)

horizontal_weight_metric = horizontal_weight * 0.453592  # Convert to kg
vertical_weight_metric = vertical_weight * 0.453592  # Convert to kg

total_tail_wing_weight_metric = horizontal_weight_metric+vertical_weight_metric

# print(f"Horizontal Stabilizer Weight: {horizontal_weight:.2f} lbs")
# print(f"Horizontal Stabilizer Weight in kg: {horizontal_weight_metric:.2f} kg")

# print(f"Vertical Stabilizer Weight: {vertical_weight:.2f} lbs")
# print(f"Vertical Stabilizer Weight in kg: {vertical_weight_metric:.2f} kg")

print(f"Total Tail Wing Weight in kg: {total_tail_wing_weight_metric:.2f} kg")
####################

# TPS Surface Areas (estimate)
# 100 ft^2 for HRSI (under wing, etc.)
# 20 ft^2 for RCC (nose and leading edge)
# 119 ft^2 for FRSI (top part of spacecraft)

HRSI_area = 100
RCC_area = 20
FRSI_area = 119

## TPS UNIT WEIGHT PER UNIT AREA ARE UNKNOWN, 
# SO WE USE THE AVERAGE USED BY THE SPACE SHUTTLE##
W_ins = 3.0

TPS_weight = W_ins * (HRSI_area + RCC_area + FRSI_area)
TPS_weight_metric = TPS_weight*0.453592  # Convert to kg
# print(f"TPS Weight: {TPS_weight:.2f} lbs")
print(f"TPS Weight in kg: {TPS_weight_metric:.2f} kg")
###################
# Landing Gear Weight
# Assuming Residual Fuel is 20% (20% fuel is left)
# The 20% residual fuel is arbitrary, 
# so you can change this however you like.
fuel_residual = 0.2
W_land = W_gtot - ((1.0-fuel_residual)*W_prop)

landing_gear_weight = 0.030 * W_land
landing_gear_weight_metric = landing_gear_weight*0.453592
print(f"Landing Gear Weight in kg: {landing_gear_weight_metric:.2f} kg")

####Total Structure Weight
structure_weight = fuselage_weight + wing_weight + horizontal_weight + vertical_weight + TPS_weight + landing_gear_weight
structure_weight_metric  = structure_weight*0.453592

print("")
print(f"Total Structure Weight in kg: {structure_weight_metric:.2f} kg")
print("")







####Engine Weight
####Tank Weight
####Total propulsion weight









# Hydraulics Weight
def hydraulics_weight_func(S_ref, q_max, L_f, W_span):
    # Calculate the psi term
    psi = abs(((S_ref*q_max/1000)**0.334) * (L_f+W_span)**0.5)
    
    # Equation for hydraulics weight (W_hydr)
    W_hydr = 2.64 * (psi ** 1.0)
    
    return W_hydr


hydraulics_weight = hydraulics_weight_func(S_ref, q_max, L_f, W_span)
hydraulics_weight_metric = hydraulics_weight*0.453592

print(f"Hydraulics Weight in kg: {hydraulics_weight_metric:.2f} kg")

# Avionics Weight
# This is MODIFIED HASA!!!
# AVIONICS WEIGHT IS REDUCED TO 69% of ORINAL HASA!
# This is due to advanced avionics
avionics_weight = 0.69*66.37*(W_gtot**0.361)
avionics_weight_metric = avionics_weight*0.453592

print(f"Avionics Weight in kg: {avionics_weight_metric:.2f} kg")

# Electrical System Weight
def electrical_weight_func(W_gtot, L_f):
    phi = abs((W_gtot**0.5) * (L_f**0.25))
    W_eps = 1.167 * (phi**1.0)
    return W_eps

electrical_weight = electrical_weight_func(W_gtot,L_f)
electrical_weight_metric = electrical_weight*0.453592

print(f"Electrical System Weight in kg: {electrical_weight_metric:.2f} kg")





####Total weight without payload (W_no_payload)
####Allowable payload weight = W_gtot - W_no_payload