#!/bin/bash

HEIGHT=0
WIDTH=0
BACKTITLE="EXO-GUI"
SERIALPORT="/dev/ttyUSB0"
SERIALBAUD="500000"

SUBFILE="SUBJECTDETAILS.txt"

# Ask user for what option is needed.
exec 3>&1
selection=$(dialog \
  --backtitle "$BACKTITLE"\
  --title "Menu"\
  --clear\
  --cancel-label "Exit"\
  --menu "Select an Option:" $HEIGHT $WIDTH 4\
  "1" "Record Experiment"\
  "2" "Tune Parameters"\
  2>&1 1>&3)
exit_status=$?
exec 3>&-

echo "Option ${selection} Selected"

array=(
        '1'
    'Subject 1'
        '2'
    'Subject 2'
        '3'
    'Subject 3'
        '4'
    'Subject 4'
        '5'
    'Subject 5'
        '6'
    'Subject 6'
        '7'
    'Subject 7'
        '8'
    'Subject 8'
        '9'
    'Subject 9'
        '10'
    'Subject 10'
)

function dialog_menu()
{

    arr["$1"]="$(dialog --clear \
            --backtitle "$2" \
            --title "$3" \
            --menu "$4" 0 0 4 \
            "${!5}" --output-fd 1)"
}

dialog_menu disk_selection "EXO-GUI" "Subject Selection" "This is a test for Menu entry" array[@]

echo "${arr[@]}"

# Start logging the data. Set exit character to 27 so that an escape can stop the logging.
python3 -m serial.tools.miniterm "${SERIALPORT}" "${SERIALBAUD}" --exit-char 27