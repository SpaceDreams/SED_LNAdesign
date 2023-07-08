#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python test bench for determination of the T1 parameters
- Use source identifier 'V1'
- Use load resistor value 'R_ell'
- Use the same file name for the .asc, .cir, .PNG, and .SVG
  files associated with a circuit.
"""
from Extras import *

# import the specifications and define the parameters
specs = csv2specs(specFileName)
specsDict=specList2dict(specs)
ini.htmlIndex = 'index.html'
htmlPage('Feedback Resistor Design')
NF_fb=sp.Symbol('NF')*sp.Symbol('alpha_NF')
head2html('Resistor Design using specifications:')
R_c=sp.Symbol("R_c")
R_b=sp.Symbol("R_b")
R_a=sp.Symbol("R_a")

# List of equations
D=sp.sympify(specsDict["D_eq"].typValue)
Dfb=sp.sympify(specsDict["D_fb_eq"].typValue)
eqn2html(D,Dfb)
B=sp.sympify(specsDict["B_eq"].typValue)
Bfb=sp.sympify(specsDict["B_fb_eq"].typValue)
eqn2html(B,Bfb)
NFeq=specsDict["NF_fb_eq"].typValue
eqn2html(NFeq,10**(NF_fb/10))

#Solving the equations
RcpRb=sp.solve(Dfb-D,R_c+R_b)[0]
Rb=sp.solve((Bfb.subs(R_c+R_b,RcpRb))-B,R_b)[0]
Rc=sp.simplify(RcpRb-Rb)
NFeq= NFeq.subs([(R_c,Rc),(R_b,Rb),(sp.symbols("R_s,Z_i"))])
Rares = sp.solve((10**(NF_fb/10)-NFeq),R_a)
Ra= Rares[1]
Rc=Rc.subs(R_a,Ra)
head2html('Resistor Solutions: ')

eqn2html(R_a,Ra)
eqn2html(R_b,Rb)
eqn2html(R_c,Rc)

head2html('Numerical Resistor Solutions: ')
Ranum = fullSubsRev(Ra,specsDict)
eqn2html(R_a,Ranum)
Rbnum = fullSubsRev(Rb,specsDict)
eqn2html(R_b,Rbnum)
Rcnum = fullSubsRev(Rc,specsDict)
eqn2html(R_c,Rcnum)

specs.append(specItem("R_a",  description="Feedback Resistor $R_a$",             maxValue=Ranum,  units="Omega", specType="design"))
specs.append(specItem("R_b",  description="Feedback Resistor $R_b$",             typValue=Rbnum,  units="Omega", specType="design"))
specs.append(specItem("R_c",  description="Feedback Resistor $R_c$",             maxValue=Rcnum,  units="Omega", specType="design"))

head2html("Updated specifications")
specs2html(specs, types = ['functional','performance', 'costs', 'environment', 'design'])
specs2csv(specs, specFileName)


