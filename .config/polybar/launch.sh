killall -q polybar

# while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done
# if type "xrandr"; then
# 	for m in $(xrandr --query | grep " connected" | cut -d" " -f1); do
# 	       	MONITOR=$m polybar --reload example &
#        	done
# else
#        	polybar --reload example &
# fi

polybar --reload main &
polybar --reload left &
polybar --reload right &
#MONITOR=DVI-I-1 polybar example &
#MONITOR=HDMI-3 polybar example &
#MONITOR=DP-1 polybar example &
echo "Bars launched, nigga"
