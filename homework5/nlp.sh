#!/bin/bash
START=$(date +%s)

echo "Total requests" >bash_results.txt
wc -l <access.log >>bash_results.txt
echo "Requests by method" >>bash_results.txt
awk '{print $6}' access.log | sort | uniq -c | sort -rn >>bash_results.txt
echo 'Top 10 requests' >>bash_results.txt
awk '{print $7}' access.log | sort | uniq -c | sort -rn | head -10 >>bash_results.txt
echo 'Top 5 4xx requests' >>bash_results.txt
awk '($9 ~ /4../)' access.log | awk '{print $7" "$9" "$10" "$1}' | sort -r -k3 | head -5 >>bash_results.txt
echo 'Top 5 5xx requests' >>bash_results.txt
awk '($9 ~ /5../)' access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -5 >>bash_results.txt

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "It took $DIFF seconds"