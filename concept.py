#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 03:52:59 PM HST 2023

by: Charles White
My two main Methodologies are:
DRY code and KISS code:
DRY: Do not Repeat Yourself
KISS: Keep it Short and Simple
"""

from Extras import *

fileName='Concept'
Cre8schAsvg4(fileName, 'Amplifier Concept')
i1 = instruction()
i1.setCircuit(fileName + '.cir')
# Create an HTML page will the circuit information
htmlPage('Circuit data')
head2html('Circuit diagram')
img2html(fileName + '.svg', 500)
netlist2html(fileName + '.cir')
elementData2html(i1.circuit)
params2html(i1.circuit)
specs = csv2specs(specFileName)
specs2circuit(specs, i1)
i1.setSimType("symbolic")
htmlPage("Functional Concept")
i1.setGainType("Gain")
i1.setSource("Vs")
i1.setDetector("V_out")
i1.setDataType("laplace")
result = i1.execute() 
head2html('Functional Specification Requirement')
text2html('From Specifications I need an accurate input impedance and an accurate voltage to current function.')
text2html('My input ports need to be floating and my output ports need to be balanced')
text2html('In the below calculations I have adjusted the gain of an ABCD function to reflect a balanced ABCD function ')
head2html('Gain Result')
I_out, V_in = sp.symbols('I_out, V_in')
V_s = sp.symbols('V_s')
R_ell, I_in= sp.symbols('R_ell,I_in')
gainEq = result.laplace/R_ell
eqn2html(I_out/V_in, gainEq)
i1.setSource("Vs")
i1.setDetector("V_in")
i1.setDataType("laplace")
VinVs = i1.execute().laplace
i1.setDetector("I_Vs")
i1.setDataType("laplace")
IVsVs = i1.execute().laplace
IinVs = -1*IVsVs
ZinEq = VinVs/IinVs #source current is in the opposite direction of input current
head2html('Impedance Result')
eqn2html(V_in/I_in,ZinEq)
head2html('T-1 Parameters')
text2html('For an Input Impedance that is independent of the load resistance I need A=C=0. ')
ZinEq = ZinEq.subs([(sp.symbols('A'), 0),(sp.symbols('C'), 0)])
gainEq=gainEq.subs([(sp.symbols('A'), 0),(sp.symbols('C'), 0)])
Z_i , A_y = sp.symbols('Z_i , A_y')
B, D = sp.symbols('B, D')
eqns = [(gainEq-A_y).as_numer_denom()[0], (ZinEq-Z_i).as_numer_denom()[0]]
A, b = sp.linear_eq_to_matrix(eqns, [B,D])
sol = sp.linsolve((A,b),[B,D])
for x in sol:
  solset=x
eqn2html(B,solset[0])
eqn2html(D,solset[1])
text2html("From the Specifications I want the input impedance to equal the Source Resistance; so I can simplify:")
Bres = solset[0].subs(sp.symbols('R_s'),Z_i)#I want the equations in terms of amp specifications since that's what I'm designing
Dres = solset[1].subs(sp.symbols('R_s'),Z_i)
eqn2html(B,Bres)
eqn2html(D,Dres)
head2html("Noise figure Budget:")
text2html("I can't use the entire noise budget for the feedback network; so instead I want the feedback network to have a fraction of the budget: ")
alpha=3/10;
eqn2html("alpha_NF",alpha)
# Let us add these values to the specifications
specs.append(specItem("B_eq",  description="Typical Voltage -> Current Gain",             typValue=Bres,  units="V/A", specType="optimization"))
specs.append(specItem("D_eq",  description="Typical Current -> Current Gain",             typValue=Dres,  units="A/A", specType="optimization"))
specs.append(specItem("alpha_NF",  description="Fraction of Noise Figure Budget for Feedback Network",             typValue=alpha,  units=1, specType="design"))

head2html("Updated specifications")
specs2html(specs, types = ['functional','performance', 'costs', 'environment', 'design'])
specs2csv(specs, specFileName)

