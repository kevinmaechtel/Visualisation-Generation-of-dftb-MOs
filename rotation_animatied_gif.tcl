proc make_rotation_animated_gif {} {
	set frame 0
	for {set i 0} {$i < 360} {incr i 10} {
		set filename snap.[format "%04d" $frame].rgb
		render snapshot $filename
		incr frame
		rotate y by 10
	}
	exec convert -delay 100 -loop 4 snap.*.rgb rotation_y.gif
	set frame 0
	for {set i 0} {$i < 360} {incr i 10} {
		set filename snap.[format "%04d" $frame].rgb
		render snapshot $filename
		incr frame
		rotate x by 10
	}
	exec convert -delay 100 -loop 4 snap.*.rgb rotation_x.gif
	set frame 0
	for {set i 0} {$i < 360} {incr i 10} {
		set filename snap.[format "%04d" $frame].rgb
		render snapshot $filename
		incr frame
		rotate z by 10
	}
	exec convert -delay 100 -loop 4 snap.*.rgb rotation_z.gif
}
