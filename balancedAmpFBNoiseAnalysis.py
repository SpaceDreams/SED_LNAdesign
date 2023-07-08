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
Cre8schAsvg4(fileName, 'Balanced Cross Coupled Noisy Feedback Analysis')
i1 = instruction()
i1.setCircuit(fileName + ".cir")
# import the specifications and define the parameters
specs = csv2specs(specFileName)
specs2circuit(specs, i1)
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
####### Noise Page
i1.setConvType('dd')
i1.setGainType('vi')
i1.setDataType('noise')
i1.setDetector('I_Rl_D')
# Define the frequency range
f_min = sp.Symbol('f_min')
f_max = sp.Symbol('f_max')
noiseResult = i1.execute()
# Create an HTML page with the results of the noise analysis
htmlPage('Symbolic noise analysis')
noise2html(noiseResult)
# Calculate the squared RMS noise at the detector
var_inoise     = rmsNoise(noiseResult, 'inoise', f_min, f_max)**2
# Calculate the contribution of the source to the squared RMS detector noise
var_inoise_src = 2*rmsNoise(noiseResult, 'inoise', f_min, f_max, noiseResult.source)**2#<---- This is bad, right? How does this work with differential mode, do I multiply by 2?
# Calculated the noise figure
NFeq=var_inoise/var_inoise_src
F_o = 10*sp.log(NFeq,10)


head2html('Noise figure')
text2html('The noise figure is obtained as:')
eqn2html('F', F_o, units='dB')

specs.append(specItem("NF_fb_eq",  description="The Noise Figure for a Balanced Cross Coupled Noisy Feedback Circuit ",             typValue=NFeq,  units="1", specType="optimization"))
head2html("Updated specifications")
specs2html(specs, types = ['functional','performance', 'costs', 'environment', 'optimization'])
specs2csv(specs, specFileName)



