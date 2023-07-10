"""
Created on Tue Jun 27 06:36:25 PM HST 2023

by: Charles White
My two main Methodologies are:
DRY code and KISS code:
DRY: Do not Repeat Yourself
KISS: Keep it Short and Simple
"""
from Extras import *

fileName = "balancedCCFBnoiseControl"
Cre8schAsvg4(fileName, 'Balanced Cross Coupled Noisy Nullor Analysis')
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
####### Noise Page
i1.setConvType('dd')
i1.setGainType('vi')
i1.setDataType('noise')
i1.setDetector('I_Rl_D')
# Define the frequency range
f_min = sp.Symbol('f_min')
f_max = sp.Symbol('f_max')
gm,k,T,n,Gamma,fl,f,fT,alpha = sp.symbols("g_m,k,T,n,Gamma,f_l,f,f_T,alpha",real=True, positive=True)
noiseResult = i1.execute()
# Create an HTML page with the results of the noise analysis
htmlPage('Symbolic noise analysis')
noise2html(noiseResult)
# Create HTML page for Mosfets as the controller
htmlPage('MOSFet noise analysis')
head2html("Noise from a MOSFet")
text2html("The spectral density of the total noise current associated with the channel current of a mosfet is:")
Sidmos=gm*4*k*T*n*Gamma*(1+fl/f)
eqn2html("S_idtot",Sidmos)
text2html("The T-1 Parameters of a MOSFet are: ")
Bmos=-1/gm
Dmos=-sp.Symbol("s")/(2*sp.pi*fT)
eqn2html("B_mos",Bmos)
eqn2html("D_mos",Dmos)
text2html("Now I can re-write the input referred noise of a Mosfet as:")
Svmos=Sidmos*(Bmos)**2
Simos=sp.expand(Sidmos*(Dmos.subs(sp.Symbol("s"),2*sp.pi*f))**2)
eqn2html("S_i",Simos)
eqn2html("S_v",Svmos)
text2html("Here I will substitute $f_l=\\alpha f_T$:")
Svmos=Svmos.subs(fl,alpha*fT)
Simos=Simos.subs(fl,alpha*fT)
eqn2html("S_i",Simos)
eqn2html("S_v",Svmos)
# Calculate the contribution of the source to the squared RMS detector noise
var_inoise_src = 2*rmsNoise(noiseResult, 'inoise', f_min, f_max, noiseResult.source)**2#<---- This is bad, right? How does this work with differential mode, do I multiply by 2?
noiseMos=noiseResult.inoise.subs([(sp.Symbol('S_i'),Simos),(sp.Symbol('S_v'),Svmos),(sp.symbols("R_s,Z_i"))])
# Calculate the squared RMS noise at the detector
dndgm     = sp.integrate(sp.diff(noiseMos,gm), (f,f_min, f_max))
gmopt = sp.solve(dndgm,gm)[1]
dndfT     = sp.simplify( sp.integrate(sp.diff(noiseMos,fT), (f,f_min, f_max))).subs(gm,gmopt)
eqn2html("g_mopt",fullSubs(gmopt,i1.parDefs))
fTopt = sp.solve(dndfT,fT)[0]
eqn2html("f_Topt",fullSubs(fTopt,i1.parDefs))

head2html("Troubleshooting:")
text2html("Here I would like to instead analyze a simpler circuit; I want the minimum RMS for a resistive voltage source; the text covers minimizing the noise but doesn't include a changing transit frequency. .... Question: What condition makes the transit frequency constant as gm changes?")
Rs = sp.Symbol("R_s",real=True, positive=True)
SvnRs = 4*k*T*Rs
Svin = SvnRs+Svmos+Rs**2*Simos
eqn2html("S_vin",Svin)
dndgm     = sp.integrate(sp.diff(Svin,gm), (f,f_min, f_max))
gmopt = sp.solve(dndgm,gm)[1]
dndfT     = sp.simplify( sp.integrate(sp.diff(Svin,fT), (f,f_min, f_max))).subs(gm,gmopt)
eqn2html("g_mopt",gmopt)
fTopt = sp.simplify(sp.solve(dndfT,fT)[0])
eqn2html("f_Topt",fTopt)
eqn2html("f_Topt",fullSubs(fTopt,i1.parDefs))
"""
specs.append(specItem("NF_Nul_eq",  description="The Noise Figure for a Noisy Nullor Balanced Cross Coupled Feedback Circuit ",             typValue=,  units="1", specType="optimization"))
head2html("Updated specifications")
specs2html(specs, types = ['functional','performance', 'costs', 'environment', 'optimization'])
specs2csv(specs, specFileName)
"""


