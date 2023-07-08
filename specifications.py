#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 04:21:31 PM HST 2023

by: Charles White
My two main Methodologies are:
DRY code and KISS code:
DRY: Do not Repeat Yourself
KISS: Keep it Short and Simple
"""

# Requirement specifications of the LNA
from Extras import *

## Source Characteristics:
SoPortConfig = "Floating" # Sources Output Port Configuration
Zsdm = 300     # Sources Differential Output impedance in Ohms
Zscm = 0.5e-12 # Sources Common Mode Output impedance in Farads
fmin  = 1e6    # Small-signal transfer -3dB high-pass cut-off frequency
fmax  = 250e6  # Small-signal transfer -3dB low-pass cut-off frequency

## Load Characteristics:
LiPortConfig = "Floating" # Loads Input Port Configuration ... Question: The spec says this is a balanced mixer; can it be grounded too? 
Ildmmax = 500e-6 # Loads Maximum Peak differential mode Input Current
Zldm = 100       # Loads input differential mode impedance in Ohms
Zlcm = 1e-12     # Loads input common mode impedance in Farads
Vcmmin = 0.8     # Loads minimum Common Mode input Voltage
Vcmmax = 1       # Loads maximum Common Mode input Voltage

## LNA Specifications:
Zisd = 4/100    # LNA's Input impedance standard deviation
Rdlmin = 10e3   # Minimum differential load resistance
NFmax = 2.5     # Noise Figure
Gainmn = 40e-3  # Mean Trans-Admittance Gain
Gainsd = 10/100 # Trans-Admittance Gain Standard Deviation
IM3max = -66    #3rd mode intermodulation distortion

## Power Supply Constraints:
VP = 1.8      # Power Supply Voltage
IPmax = 20e-3 # Maximum current the power supply can provide

## Environmental Conditions:
minTemp = 0  # Minimum Operating Temperature in Celsius
maxTemp = 70 # Maximum Operating Temperature in Celsius

# Add all this data to a table with specifications

specs = []

specs.append(
    specItem(
        "Z_i",
        description = "LNA input impedance",
        typValue    = Zsdm,
        units       = "Omega",
        specType    = "performance",
    )
)
specs.append(
    specItem(
        "Delta_Z_i",
        description = "LNA input impedance Standard Deviation",
        typValue    = Zisd,
        units       = "Omega",
        specType    = "performance",
    )
)
specs.append(
    specItem(
        "Z_scm",
        description = "Sources Common Mode output impedance",
        typValue    = Zscm,
        units       = "F",
        specType    = "functional", 
    )
)
specs.append(
    specItem(
        "f_min",
        description = "Small-signal -3dB high-pass cut-off frequency",
        maxValue    = fmin,
        units       = "Hz",
        specType    = "performance",
    )
)
 
specs.append(
    specItem(
        "f_max",
        description = "Small-signal -3dB low-pass cut-off frequency",
        minValue    = fmax,
        units       = "Hz",
        specType    = "performance",
    )
)
specs.append(
    specItem(
        "R_ell",
        description = "LNA differential load resistance",
        minValue    = Rdlmin,
        units       = "Omega",
        specType    = "performance",
    )
)
specs.append(
    specItem(
        "NF",
        description = "Maximum LNA Noise Figure",
        maxValue    = NFmax,
        units       = "dB",
        specType    = "performance",
    )
)
specs.append(
    specItem(
        "A_y",
        description = "LNA Gain",
        typValue    = Gainmn,
        units       = "S",
        specType    = "functional",
    )
)
specs.append(
    specItem(
        "Delta_A_y",
        description = "LNA Gain Standard Deviation",
        typValue    = Gainsd,
        units       = "S",
        specType    = "functional",
    )
)
specs.append(
    specItem(
        "IM3",
        description = "LNA 3rd Order Intermodulation Distortion",
        typValue    = IM3max,
        units       = "dB",
        specType    = "performance",
    )
)
specs.append(
    specItem(
        "I_omin",
        description = "LNA maximum peak output current",
        typValue    = Ildmmax,
        units       = "A",
        specType    = "performance",
    )
)
specs.append(
    specItem(
        "V_P",
        description = "Power supply voltage",
        minValue    = VP,
        units       = "V",
        specType    = "Power Supply",
    )
)
specs.append(
    specItem(
        "I_pmax",
        description = "Maximum Power supply current",
        minValue    = IPmax,
        units       = "A",
        specType    = "Power Supply",
    )
)
    
    
# Save the specifications
specs2csv(specs, specFileName)

# display the date on an html page

htmlPage("Specifications")
text2html("The Load and Source are both floating. ")
specs2html(specs)
