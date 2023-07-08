"""
Created on Tue Jun 27 06:36:25 PM HST 2023

by: Charles White
My two main Methodologies are:
DRY code and KISS code:
DRY: Do not Repeat Yourself
KISS: Keep it Short and Simple
"""
from Extras import *

fileName = "balancedCCFBnoise"
Cre8schAsvg4(fileName, 'Balanced Cross Coupled Feedback Gain Analysis')
i1 = instruction()
i1.setCircuit(fileName + ".cir")
# import the specifications and define the parameters
specs = csv2specs(specFileName)
specs2circuit(specs, i1)

# Circuit Page
htmlPage("Circuit Data")
head2html("Circuit diagram")
img2html(fileName + ".svg", 600)
netlist2html(fileName + ".cir")
elementData2html(i1.circuit)
params2html(i1.circuit)

i1.setSource(["VsP","VsN"])
i1.setDetector(["V_outP","V_outN"])

i1.setSimType("symbolic")
htmlPage("DM-CM decomposition")
# Define the decomposition
head2html("MNA matrix equation")
i1.setGainType("vi")
i1.setDataType("matrix")
matrices2html(i1.execute())

head2html("DM-CM matrix equation")
i1.setPairExt(['P', 'N'])

i1.setConvType('all') 
matrices2html(i1.execute())

head2html("DM matrix equation")
i1.setConvType('dd') 
matrices2html(i1.execute())

head2html("CM matrix equation")
i1.setConvType('cc') 
matrices2html(i1.execute())
########################
htmlPage("ABCD Parameters")
i1.setConvType('dd')
i1.setGainType('gain')
i1.setDataType('laplace')
i1.setDetector('V_in_D')

V_i = i1.execute().laplace
# Define the detector for determination of the input current
i1.setDetector('I_Vs_D')
result = i1.execute()
# I_i is the transfer from V1 to the current through V1
I_i = -result.laplace

# Define the detector for determination of the output voltage
i1.setDetector('V_out_D')
# V_o is the transfer from V1 to the output voltage
V_o = i1.execute().laplace

# Define the detector for determination of the output current
i1.setDetector('I_Rl_D')
result = i1.execute()
# I_o is the transfer from V1 to the current through R2
I_o = result.laplace

# Calculate the T1 parameters
# Use the same name for the load resistance in all files
R_ell = sp.Symbol('R_ell')
Cocm = sp.Symbol('C_ocm')
A     = sp.simplify(sp.limit(sp.limit(V_i/V_o, R_ell, 'oo'), Cocm, 0))
B     = sp.simplify(sp.limit(V_i/I_o, R_ell, 0))
C     = sp.simplify(sp.limit(sp.limit(I_i/V_o, R_ell, 'oo'), Cocm, 0))
D     = sp.simplify(sp.limit(I_i/I_o, R_ell, 0))

head2html('Test circuit')
img2html(fileName + '.svg', 500)
head2html('T1 matrix of the device under test')
text2html('The T1 matrix of the device under test is found as:')
T1 = sp.Matrix([[A,B], [C,D]])
eqn2html('T_1', T1)
ViIi = sp.Matrix([[sp.Symbol('V_in')], [sp.Symbol('I_in')]])
VoIo = sp.Matrix([[sp.Symbol('V_out')], [sp.Symbol('I_out')]])
# Display the matrix equation without execution of the multiplication
text2html('The matrix equation for the two-port (DUT) is found as:')
text2html('$$' + sp.latex(ViIi) + "=" + sp.latex(T1) + '\\cdot' + sp.latex(VoIo) + '$$')

# Let us add these values to the specifications
specs.append(specItem("B_fb_eq",  description="The B T-1 Parameter for a Balanced Cross Coupled Feedback Circuit ",             typValue=B,  units="V/A", specType="optimization"))
specs.append(specItem("D_fb_eq",  description="The D T-1 Parameter for a Balanced Cross Coupled Feedback Circuit ",             typValue=D,  units="I/I", specType="optimization"))


head2html("Updated specifications")
specs2html(specs, types = ['functional','performance', 'costs', 'environment', 'optimization'])
specs2csv(specs, specFileName)



