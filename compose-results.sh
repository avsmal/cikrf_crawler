#!/bin/bash
for prefix in mo gub
do
	rm -f ${prefix}.csv
	for f in ${prefix}/*.dat
	do 
		DATA=`cut -f1-15 -d, ${f}` 
		echo $DATA >> ${prefix}.csv
	done
done

FIELDS=5

rm -f movsgub.csv
for f in mo/*.dat
do 
	fn=${f#mo/}
	uik=${fn#uik-}
	uik=${uik%.dat} 
	DATAMO=`cut -f1-15 -d, mo/${fn}` 
	DATAGU=`cut -f2-15 -d, gub/${fn}` 
	echo "$DATAMO,$DATAGU" >> movsgub.csv
done

