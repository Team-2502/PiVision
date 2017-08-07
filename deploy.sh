files=""

for file in *; do
    if [[ -f $file ]]; then
        files=$files" "$file
    fi
done

#pi@pi-2502-frc.local
#pi@ritikm-pi
scp $files pi@pi-2502-frc.local.local:/home/pi/.vision/
echo "Deployed all files (or at least tried to)"

echo "Restarting vision . . ."
ssh pi@pi-2502-frc.local
echo "Complete! (or at least tried to)"




