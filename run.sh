#!/bin/bash
## usage ./run.sh timelimit threads times
cpo='/mnt/nfs/work/gcobs070796/cplex_solver/cpoptimizer/bin/x86-64_linux/cpoptimizer'
shopt -s extglob
cd data_list/
for file in *;
do
    echo "read /mnt/nfs/work/gcobs070796/experiments/cpo/${file%%*(.dat)}.cpo
set TimeLimit $1
set FailLimit 9007199254740991
set worker $2
optimize
display solution
quit" > ../cmd/${file%%*(.dat)}.mps
done
cd ..
mkdir thread_$2
cd thread_$2
for num in $(seq 1 $3);
do
  mkdir test_$num
  mkdir test_$num/result_$2_$1
  pwd
  cd /mnt/nfs/work/gcobs070796/experiments/cmd/
  for file in *;
  do
      ${cpo} < ${file} > ../thread_$2/test_$num/result_$2_$1/${file%%*(.mps)}.log
  done
  cd /mnt/nfs/work/gcobs070796/experiments/thread_$2/
done
