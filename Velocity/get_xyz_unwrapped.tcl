set dir /data/server5/server4/tbglprojects2/shankla2/Graphene_Defect_REDO_03062015/CFSMD_Polylength_2

set files "
10 x
10 y
10 -y
20 x
20 y
20 -y
30 x
30 y
30 -y
40 x
40 y
40 -y
"

foreach {struc dcd}  $files {

	mol load psf $dir/index/nowat_final_ssDNA_DNA${struc}1_fixed.psf
	mol addfile  $dir/output/unwrapped_${struc}_${dcd}_full.dcd waitfor all
	set nf [molinfo top get numframes]
	set out [open CFSMD_POLYLENGTH_unwrapped_pos_${struc}_${dcd}.txt w]
	puts "This is nf $nf"
	for {set i 0} {$i < $nf} {incr i} {
	        set all [atomselect top all]
	        set sel [atomselect top "nucleic and resid 6 7 8 9 10 11 12 13 14 15"]; $sel frame $i
	        set com [ measure center $sel weight mass   ]
	        set com2 [vectrans [ transaxis z 30  ]  $com]
					set t [expr $i*0.000002*4800]
	        puts $out "$t $com2"
	}
}
exit
