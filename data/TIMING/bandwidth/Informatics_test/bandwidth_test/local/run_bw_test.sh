for i in {1..100}; do echo $i; bash scripts/${i}.sh 2> logs/${i}.sh; done
