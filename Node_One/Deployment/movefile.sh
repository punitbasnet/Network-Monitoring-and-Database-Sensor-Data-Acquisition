cd ~/readings/normalreadings/current

for f in *.txt; do
 /bin/mv ~/readings/normalreadings/current/$f ~/readings/normalreadings/
done

cd ~/readings/hmacs/current
for g in *.txt; do
 /bin/mv ~/readings/hmacs/current/$g ~/readings/hmacs
done

