from os import listdir
import argparse
solution = []
def extract_sol(filename, thread, time):
    with open('./result_'+thread +'_'+ time + '/'+ filename, encoding='utf-8') as fp:
        line = fp.readline()
        while line.startswith(' ! Time spent ') == False:
            line = fp.readline()
        time = line.split(': ')[1].split('s')[0]
        while line.startswith('Optimal solution found with objective') == False and line.startswith('Solution found with objective') == False:
            line = fp.readline()
        optimal = 'True'
        objective = 0
        if line.split()[0] == 'Optimal':
            optimal = 'True'
            objective = line.split()[-1].split('.')[0]
        else:
            optimal = 'False'
            objective = line.split()[4].split(',')[0]
        solution.append(' '.join([filename.split('.')[0], time, optimal, objective]) )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("time", help="running time of cplex.", type=str)
    parser.add_argument("thread", help="running threads of cplex.", type=str)
    args = parser.parse_args()
    mypath = './result_'+ args.thread + '_' + args.time +'/'
    files = listdir(mypath)
    files.sort()
    for file in files:
        extract_sol(file, args.thread, args.time)
    with open('./' +args.thread+'_'+args.time+'_optimal', 'w') as fp:
        for i in solution:
            fp.write(i)
            fp.write('\n')
            
