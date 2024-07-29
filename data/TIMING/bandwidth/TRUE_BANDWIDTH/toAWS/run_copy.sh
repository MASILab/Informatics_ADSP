for i in {1..100}
do
	echo $i
	(time scp -i ~/Kim_Test.pem ../1GBfile.bin ubuntu@44.222.225.166:/tmp/testbin.bin) 2> logs/${i}.txt
done
