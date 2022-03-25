#for century in 19 20 19 21 18 17 16 ; do
#for valueName in latitude longitude ; do

centuries="20 19"

for century in $centuries ; do
python3 cheber.py moon 301 $century
python3 cheber.py sun 10 $century
done

for century in $centuries ; do
python3 cheber.py mercury 199 $century
python3 cheber.py venus 299 $century
python3 cheber.py mars 499 $century
done

for century in $centuries ; do
python3 cheber.py jupiter 599 $century
python3 cheber.py saturn 699 $century
done

for century in $centuries ; do
python3 cheber.py uranus 799 $century
python3 cheber.py neptune 899 $century

python3 cheber.py pluto 999 $century

python3 cheber.py chiron Chiron $century
done

for century in $centuries ; do
python3 cheber.py vesta Vesta $century
python3 cheber.py juno "A804 RA" $century
python3 cheber.py ceres Ceres $century
python3 cheber.py pallas Pallas $century
done

for century in $centuries ; do
python3 cheber.py ceres Ceres $century
python3 cheber.py eris Eris $century
python3 cheber.py orcus Orcus $century
python3 cheber.py haumea Haumea $century
python3 cheber.py quaoar Quaoar $century
python3 cheber.py makemake Makemake $century
python3 cheber.py gonggong Gonggong $century
python3 cheber.py sedna Sedna $century
done

for century in $centuries ; do
python3 cheber.py chariklo Chariklo $century
python3 cheber.py sappho Sappho $century
python3 cheber.py eros Eros $century
python3 cheber.py psyche Psyche $century
python3 cheber.py hygiea Hygiea $century
python3 cheber.py davidbowie DavidBowie $century
python3 cheber.py hekate Hekate $century
done


for century in $centuries ; do
python3 cheber.py iris "A847 PA" $century
python3 cheber.py isaac_newton "Isaac Newton" $century
python3 cheber.py asimov Asimov $century
done