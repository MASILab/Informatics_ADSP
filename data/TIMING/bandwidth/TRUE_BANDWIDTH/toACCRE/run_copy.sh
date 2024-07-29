for i in {1..100}
do
	echo $i
	(time scp ../1GBfile.bin kimm58@gw346.accre.vanderbilt.edu:/tmp/testbin.bin) 2> logs/${i}.txt
done
