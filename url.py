from os import listdir
import argparse
if __name__ == '__main__':
    mypath = './instances/'
    parser = argparse.ArgumentParser()
    parser.add_argument("time", help="running time of cplex.", type=str)
    parser.add_argument("thread", help="thread number of cplex.", type=str)
    args = parser.parse_args()

    files = listdir(mypath)
    files.sort()
    with open('./html_'+args.thread+'_'+args.time+'.txt', 'w') as fp:
        for file in files:
            url = 'https://cgilab.nctu.edu.tw/~gcobs070796/'+args.thread +'_'+args.time+'_html/' + file + '.html\n'
            fp.write(url)
