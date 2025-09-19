#!/bin/bash

xyzfile=$1
natom=$(head -1 $xyzfile)
natomQM1=$2
output=$3
natomQM2=$( echo "${natom}-${natomQM1}" | bc )
directory=$PWD


#prepare geometry
natomQM1_2=$( echo "$natomQM1+2" | bc )
echo $natomQM1 > small.geom
echo ' ' >> small.geom
head -n $natomQM1_2 $xyzfile | tail -$natomQM1 >> small.geom

#large DFT
cat > QM2_l.com << EOF
! PBE def2-SVP RI D3
! ENGRAD AUTOSTART
!CHELPG
%scf
maxiter 400
convergence strong
FlipSpin 0 #flipspin on first atom
FinalMs  0.0
end

* xyzfile 0 3 $directory/$xyzfile
EOF

#run
ORCA QM2_l.com

#grep charges 
echo 'point charges from CHELPG' > in.lat
echo $natomQM2 > QM2.charge
tail -n $natomQM2 QM2_l.pc_chelpg | cut -b -5 --complement >> QM2.charge
echo $natomQM2 >> in.lat
awk '{ print $3 "," $4 "," $5 "," $2 ",0" }' QM2_l.pc_chelpg | tail -n $natomQM2 >> in.lat


#molpro CASSCF
cat > QM1_s.com << EOF
memory,1000,m
symmetry,nosym 

angstrom

geometry=small.geom

lattice,in.lat,out.lat

basis=6-31+g*

{hf}

{mcscf;
closed,9;
occ,16;
pspace,1
wf,24,1,0;
state,4;
ORBITAL,2140.2;
save,5100.2;
}
{rs2,mix=4,root=1,shift=0.2;state,4;}
force

EOF

#run molpro
MOLPRO QM1_s.com

#small DFT
cat > QM2_s.com << EOF
! PBE def2-SVP RI D3
! ENGRAD AUTOSTART
!CHELPG
%scf
maxiter 400
convergence strong
FlipSpin 0 #flipspin on first atom
FinalMs  0.0
end
%pointcharges "$directory/QM2.charge"


* xyzfile 0 3 $directory/small.geom
EOF

#run ORCA
ORCA QM2_s.com

#get energies and gradients
energy_QM1=$(grep 'RSPT2 STATE 1.1' QM1_s.com.out | grep 'Energy' | awk '{ print $5 }')
energy_QM2_s=$(grep 'FINAL SINGLE' QM2_s.com.out | awk '{ print $5 }')
energy_QM2_l=$(grep 'FINAL SINGLE' QM2_l.com.out | awk '{ print $5 }')
total_energy=$( echo "${energy_QM1}+(${energy_QM2_l})-(${energy_QM2_s})" | bc )

natomQM1_3=$( echo "$natomQM1+3" | bc )
natom2=$( echo "$natom+2" | bc )
grep 'GRADIENT FOR' -A $natomQM1_3 QM1_s.com.out | tail -n $natomQM1 | cut -b -12 --complement > QM1_s.grad
grep 'CARTESIAN GRADIENT' -A $natom2 QM2_l.com.out | tail -n $natom | cut -b -15 --complement > QM2_l.grad
grep 'CARTESIAN GRADIENT' -A $natomQM1_2  QM2_s.com.out | tail -n $natomQM1 | cut -b -15 --complement > QM2_s.grad
paste QM2_l.grad QM2_s.grad QM1_s.grad | awk '{ printf "%18.12f %18.12f %18.12f\n", $1-$4+$7,$2-$5+$8,$3-$6+$9 }' > QMQM.grad

echo $natom > $output
echo "Properties=species:S:1:pos:R:3:forces:R:3 energy=$total_energy" >> $output
paste <( tail -n $natom $xyzfile ) <( paste QM2_l.grad QM2_s.grad QM1_s.grad | awk '{ printf "%18.12f %18.12f %18.12f\n", -$1+$4-$7,-$2+$5-$8,-$3+$6-$9 }' ) >> $output

rm small.geom out.lat *gbw *uco *vpot *densities 
