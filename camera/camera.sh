INTERVAL=15            # Time between captures, in seconds
WIDTH=1280             # Image width in pixels
HEIGHT=720             # Image height in pixels
QUALITY=51             # JPEG image quality (0-100)
DEST=./pics            # Destination directory (MUST NOT CONTAIN NUMBERS)
PREFIX=img             # Image prefix (MUST NOT CONTAIN NUMBERS)
HALT=21                # Halt button GPIO pin (other end to GND)
LED=17                 # Status LED pin (v2 Pi cam lacks built-in LED)
prevtime=0             # Time of last capture (0 = do 1st image immediately)

gpio -g mode $HALT up  # Initialize GPIO states
gpio -g mode $LED  out
mkdir -p $DEST         # Create destination directory (if not present)

# Find index of last image (if any) in directory, start at this + 1

FRAME=$(($(find $DEST -name "*.jpg" -printf %f\\n | sed 's/^[^1-9]*//g' | sort -rn | head -1 | sed 's/[^0-9]//g') + 1))
OUTFILE=`printf "$DEST/$PREFIX%05d.jpg" $FRAME`
echo $OUTFILE
gpio -g write $LED 1
# raspistill -n -w $WIDTH -h $HEIGHT -q $QUALITY -th none -t 250 -o $OUTFILE
raspistill -n -w $WIDTH -h $HEIGHT -q $QUALITY -th none -t 250 -o ./img.jpg
touch $OUTFILE
gpio -g write $LED 0
FRAME=$(($FRAME + 1)) # Increment image counter
prevtime=$currenttime # Save image cap time
