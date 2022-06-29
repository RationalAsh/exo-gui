#!/bin/bash

HEIGHT=0
WIDTH=0

SUBFILE="SUBJECTDETAILS.txt"

# Ask user for what option is needed.
exec 3>&1
selection=$(dialog \
  --backtitle "System Information"\
  --title "Menu"\
  --clear\
  --cancel-label "Exit"\
  --menu "Please select:" $HEIGHT $WIDTH 4\
  "1" "Record Experiment"\
  "2" "Tune Parameters"\
  2>&1 1>&3)
exit_status=$?
exec 3>&-

echo "Option ${selection} Selected"

array=(
        '1'
    'Subject 1'
        '1'
    'Subject 1'
        '1'
    'Subject 1'
        '1'
    'Subject 1'
        '1'
    'Subject 1'
        '1'
    'Subject 1'
        '1'
    'Subject 1'
)

function dialog_menu()
{

    arr["$1"]="$(dialog --clear \
            --backtitle "$2" \
            --title "$3" \
            --menu "$4" 10 60 3 \
            "${!5}" --output-fd 1)"

}

dialog_menu disk_selection "Menu" "Menu Test" "This is a test for Menu entry" array[@]