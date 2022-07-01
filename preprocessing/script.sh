#!/bin/bash
if [ $# != 2 ];then
    echo "usage: script.sh 'instances directory' 'xxx.mod'"
    exit
fi
oplrun='/mnt/nfs/work/gcobs070796/cplex_solver/opl/bin/x86-64_linux/oplrun'
directory=$1
cd $1
for file in *;
do  
    shopt -s extglob
    echo "${file%%*(.dat)}"
    ${oplrun} -d /mnt/nfs/work/gcobs070796/experiments/cpo/${file%%*(.dat)}.cpo ../preprocessing/$2 ${file}
done
