#while true ; do
  for I in `ls -d results/*/ | sed 's:.*/\(.*\)/.*:\1:'` ; do 
    echo "$I" 
    for v in longitude latitude ; do
      python3 weftize.py "$I" $v 2> /tmp/errweft 
    done
  done 
  echo 
  ls -Slh results/*.20*.weft results/*.19*.weft
#  sleep 600 
#done
