
i=0
total=0
cat ACCRE.txt | cut -d '|' -f 2 | cut -d ' ' -f 2 | while IFS= read -r line
do
	i=$(($i+1))
	#echo $i
	IFS=: read -r hours minutes seconds <<< "$line"
	total_mins=$((10#$hours * 60 + 10#$minutes ))
	echo "$total_mins"
	total=$((total + total_mins))
done

#echo $i
#count=$(cat ACCRE.txt | wc -l)
#echo $count
#avg=$(($total / $co))

#echo Average: $avg

