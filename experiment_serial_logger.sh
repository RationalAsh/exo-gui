#!/bin/bash

# Parameters
DSET_NAME="GERI"
PAT_NUM=0
EXP_NUM=0
EXP_PART=0
EXP_DESC="ones two three"
GUI_ON=1
DIALOG=dialog
SUBFILE=SUBJECT_DETAILS.txt
UITITLE="IMU Datalogger UI"
ASCIIMODE=1
LOGDIR=IMUDATA
DESCFILE=EXP_DESC.txt
CALIB_HELP_TEXT="The calibration is about to start. To calibrate the IMU, \
                 30 seconds of data is needed. For the first 10 seconds the \
                 subject has to stand still and move as little as possible. \
                 For the next 10 seconds ask subject to move the right leg and \
                 for tht next 10 seconds ask the subject to move the left leg.
                 \n\nPress OK to start calibration"

# Prompt for patient and experiment identifiers:

# Create new stream
exec 3>&1

# Get Subject information
if [ -x "$(command -v $DIALOG)" ]
then
    # Read defaults
    read -r PAT_NUM EXP_NUM EXP_PART <<<$(cat $SUBFILE)
    VALUE=$($DIALOG --ascii-lines --backtitle "$UITITLE" \
	--keep-tite --title "Enter Subject Details" \
	--ok-label "Start Calibration" \
	--form "\nEnter experiment parameters.\n" 15 50 0 \
	"        Subject Number: " 1 1 "$PAT_NUM"  1 25 15 15 \
	"     Experiment Number: " 2 1 "$EXP_NUM"  2 25 15 15 \
	"Experiment Part Number: " 3 1 "$(($EXP_PART + 1))" 3 25 15 15 2>&1 1>&3)
    rval=$?
    if [ "$rval" -eq "0" ]
    then
	# Read dialog input into variables
	read -r PAT_NUM EXP_NUM EXP_PART <<<$(echo $VALUE)
	# Write output to a file 
	echo $VALUE > $SUBFILE
    else
	echo "Aborting..."
	exit 1
    fi	
fi

# Close the stream
exec 3>&-;

# New stream for interacting with miniterm
exec 

# Generate the time stamp:
TSTAMP=$(date +"%Y%m%d_%H%M%S")

# Generate filename:
PAT_NUM_PAD=$(printf "%02d" $PAT_NUM)
EXP_NUM_PAD=$(printf "%02d" $EXP_NUM)
EXPFNAME="exp_${EXP_PART}.csv"
EXPDIR=$LOGDIR/sub_${PAT_NUM}/session_${EXP_NUM}

# Create experiment directory if it does not exist.
mkdir -p $EXPDIR

resp="1"
while [ $resp -gt 0 ]
do
    # Informative message
    $DIALOG --backtitle "$UITITLE" --title "Starting calibration process..." --keep-tite --ascii-lines \
            --msgbox "$CALIB_HELP_TEXT" 30 80
    
    # Collect 10s of still calibration data
    sudo expect -f calib.exp | $DIALOG --ascii-lines --backtitle "$UITITLE" --title "Collecting still calibration data:" \
                                 --keep-tite --gauge "Collecting calibration data. Ask subject to move as little as possible!" 10 80
    mv -f calib.csv $EXPDIR/calib_still_$EXP_PART.csv
    
    # Collect 10s of right leg calibration data
    # sudo expect -f calib.exp | $DIALOG --ascii-lines --backtitle "$UITITLE" --title "Collecting right leg calibration data:" \
    #                              --keep-tite --gauge "Collecting calibration data. Ask subject to move right leg." 10 80
    # mv -f calib.csv $EXPDIR/calib_right_$EXP_PART.csv
    
    # Collect 10s of left leg calibration data
    # sudo expect -f calib.exp | $DIALOG --ascii-lines --backtitle "$UITITLE" --title "Collecting left leg calibration data:" \
    #                              --keep-tite --gauge "Collecting calibration data. Ask subject to move left leg." 10 80
    # mv -f calib.csv $EXPDIR/calib_left_$EXP_PART.csv
    
    # Tell user that calibration is going on
    $DIALOG --ascii-lines --backtitle "$UITITLE" --title "Calibrating...." \
            --infobox "Calibration parameters are being calculated. Please wait..." 10 80

    # Run script to get calibration params
    # { ./joint_calib_left.py $EXPDIR/calib_left_$EXP_PART.csv; ./joint_calib_right.py  $EXPDIR/calib_right_$EXP_PART.csv; } \
    #  | tee $EXPDIR/calibparams_${EXP_PART}.txt \
    #  | awk '{printf "%d\nXXX\nCalculating: %s\nXXX\n", NR*100/25, $0}'\
    #  | $DIALOG --backtitle "$UITITLE" --title "Calculating calibration parameters" --keep-tite --ascii-lines\
    #             --gauge " " 10 80
    # CPARAMS=$(cat $EXPDIR/calibparams_${EXP_PART}.txt | awk '{ printf "\\Zb %s\\Zn: %+.4f %+.4f %+.4f\\n", $1, $2, $3, $4 }')

    # Display calibration params. If OK go on if not repeat.
    # $DIALOG --ascii-lines --backtitle "$UITITLE" \
    # 	--title "Calibration Params:" --ok-label "Finalize" --colors\
    # 	--keep-tite --cancel-label "Abort" --extra-button --extra-label "Recalibrate"\
    # 	--yesno "$CPARAMS" 40 80

    # Run script to summarize calibration parameters
    ./calib_summary.py $EXPDIR/calib_still_$EXP_PART.csv > CALIB_SUMMARY.txt
    CSUM_TXT=$(cat CALIB_SUMMARY.txt | awk '{printf "%s\\n", $0}')
    
    # Prompt that calibration is complete.
    $DIALOG --ascii-lines --backtitle "$UITITLE" \
	    --title "Calibration Done" --ok-label "Finalize" --colors \
	    --keep-tite --cancel-label "Abort" --extra-button --extra-label "Recalibrate" \
	    --yesno "$CSUM_TXT" 20 80
    
    resp=$?
    if [ "$resp" -eq "1" ]
    then
	echo "Aborting...."
	exit 1
    fi
done

# Read previous descprition from file
if [ ! -e "$DESCFILE" ] ; then
    touch "$DESCFILE"
fi
PREV_DESC=`cat $DESCFILE`

# Create new stream
exec 4>&1

# Prompt for start of experiment
RESP=$($DIALOG --backtitle "$UITITLE" --ok-label "Start" --cancel-label "Abort" --colors \
    --ascii-lines --keep-tite --title "Starting experiment..." --inputbox "Details:\n \
\Zb   Experiment file name:\Zn ${EXPDIR}/${EXPFNAME}\n \
\Zb         Patient Number:\Zn $PAT_NUM_PAD\n \
\Zb      Experiment Number:\Zn $EXP_NUM_PAD\n \
\Zb        Experiment Part:\Zn $EXP_PART\n \
Enter a short description for the experiment (optional). Description will appear at the top of the csv log file as a comment/header prefixed with a symbol." 20 80 "$PREV_DESC" 2>&1 1>&4)

if [ $? -gt 0 ]
then
    echo "Aborting..."
    exec 4>&-;
    exit 1
fi

# Close the stream
exec 4>&-;

# Save the response to a file
echo $RESP > $DESCFILE

$DIALOG --backtitle "$UITITLE" --yes-label "Fixed Duration" --no-label "Indefinite Duration" \
        --ascii-lines --keep-tite --title "Type of Experiment?" \
        --yesno "Are you running a fixed duration experiment or an indefinite duration experiment?" 10 50
RESP=$?
if [ "$RESP" -eq 0 ] # If experiment is for a fixed duration
then
    # Read previous experiment duration
    read -r DUR <<<$(cat DURATION.txt)
    # Create new stream
    exec 4>&1
    # Ask for how long the experiment should be
    RESP=$($DIALOG --ascii-lines --backtitle "$UITITLE" \
	--keep-tite --title "Enter experiment duration:" \
	--ok-label "Start Experiment" \
	--form " " 15 50 0 \
	"   Experiment Duration: " 1 1 "$PAT_NUM"  1 25 15 15 2>&1 1>&4)
    read -r DUR <<<$(echo $RESP)
    echo $RESP > DURATION.txt
    # Close the stream
    exec 4>&-;
    # Show dialog with progress bar
    # sudo expect -f logdata.exp | $DIALOG
    sudo expect -f logdata.exp $DUR | $DIALOG --backtitle "$UITITLE" --ascii-lines --keep-tite \
                                         --title "Collecting data for $DUR s" \
                                         --gauge " " 20 80
    mv -f data.csv $EXPDIR/$EXPFNAME 
else
    # Show the usual text based interface for logging the data
    clear
    sleep 0.4
    sudo nice --10 miniterm.py /dev/ttyACM0 2000000 | tee $EXPDIR/$EXPFNAME | awk -f imu_format.awk
fi

# Add notes to start of file
DESC=$(cat $DESCFILE)
sed -i "1i#$DESC" $EXPDIR/$EXPFNAME

$DIALOG --clear --backtitle "$UITITLE" --ascii-lines --keep-tite --colors \
        --title "Experiment done." --msgbox "Experiment done. Data saved to \
        \Zb$EXPDIR/$EXPFNAME\Zn." 10 80 
clear

# clear
# echo $VALUES
# echo $(($EXP_PART + 1))
