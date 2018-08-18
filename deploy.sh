files=""

for file in *; do
    if [[ -f $file ]]; then
        files=$files" "$file
    fi
done

#pi@pi-2502-frc.local
#pi@ritikm-pi
scp $files pi@team2502pi.local:/home/pi/.vision/
echo "Deployed all files (or at least tried to)"

echo "Once the clock changes minute the vision will be ready"
#"python /home/pi/.vision/Vision.py" | ssh pi@team2502pi.local
echo "Complete! (or at least tried to)"




