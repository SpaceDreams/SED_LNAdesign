v 20211219 2
C -12100 22700 1 90 0 R.sym
{
T -13750 22850 5 8 0 0 90 0 1
device=R-slicap
T -12900 23225 5 8 1 1 90 0 1
refdes=Rs
T -12775 23225 5 8 1 0 90 0 1
value={R_s}
T -12625 23225 5 8 1 0 90 0 1
dcvar=0
T -12475 23225 5 8 1 0 90 0 1
noisetemp=0
T -12325 23225 5 8 1 0 90 0 1
noiseflow=0
}
C -10500 22100 1 0 0 R.sym
{
T -10350 23750 5 8 0 0 0 0 1
device=R-slicap
T -9975 22900 5 8 1 1 0 0 1
refdes=Rl
T -9975 22775 5 8 1 0 0 0 1
value={R_ell}
T -9975 22625 5 8 1 0 0 0 1
dcvar=0
T -9975 22475 5 8 1 0 0 0 1
noisetemp=0
T -9975 22325 5 8 1 0 0 0 1
noiseflow=0
}
C -13700 22200 1 0 0 V.sym
{
T -13700 23450 5 6 0 0 0 0 1
device=V-slicap
T -13200 22750 5 8 1 0 0 0 1
value={V_s}
T -13200 22900 5 8 1 1 0 0 1
refdes=Vs
T -13200 22600 5 8 1 0 0 0 1
dc=0
T -13205 22450 5 8 1 0 0 0 1
dcvar=0
T -13205 22300 5 8 1 0 0 0 1
noise=0
}
C -12100 22000 1 0 0 ABCD.sym
{
T -12700 24300 5 6 0 0 0 0 1
device=twoPort-slicap
T -11750 23900 5 8 1 1 0 0 1
refdes=XP
T -11350 23900 5 8 1 0 0 0 1
A={A}
T -11350 23700 5 8 1 0 0 0 1
B={B}
T -11350 23500 5 8 1 0 0 0 1
C={C}
T -11350 23300 5 8 1 0 0 0 1
D={D}
}
N -10500 22200 -10200 22200 4
N -10200 23000 -10500 23000 4
{
T -10300 23050 5 10 1 1 0 6 1
netname=out
}
C -13700 21900 1 0 0 0.sym
{
T -13300 22450 5 6 0 0 0 0 1
device=0-slicap
}
N -12200 23000 -12100 23000 4
{
T -12100 23050 5 10 1 1 0 0 1
netname=in
}
C -10400 21900 1 0 0 0.sym
{
T -10000 22450 5 6 0 0 0 0 1
device=0-slicap
}
N -13000 23000 -13500 23000 4
N -12100 22200 -13500 22200 4
