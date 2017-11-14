set dir /data/server5/server4/tbglprojects2/shankla2/Graphene_Defect_REDO_03062015/CFSMD_Polylength_2

set files "
10 y b
20 y b
30 y b
40 y b
10 y c
20 y c
30 y c
40 y c
"

foreach {struc dcd trial}  $files {
	mol load psf $dir/index/nowat_final_ssDNA_DNA${struc}1_fixed.psf
	mol addfile  $dir/output/unwrapped_${struc}_${dcd}_full.dcd waitfor all
	set nf [molinfo top get numframes]
	set out [open CFSMD_POLYLENGTH_unwrapped_pos_${struc}_${dcd}.txt w]
	puts "This is nf $nf"
	for {set i 0} {$i < $nf} {incr i} {
	        set all [atomselect top all]
	        set sel [atomselect top "nucleic "]; $sel frame $i
	        set com [ measure center $sel weight mass   ]
	        set com2 [vectrans [ transaxis z 30  ]  $com]
					set t [expr $i*0.000002*4800]
	        puts $out "$t $com2"
	}
}
exit
