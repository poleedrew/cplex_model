#include <iostream>
#include <fstream>
#include <string>
#include <dirent.h>
#include <stdio.h>
#include <sstream>
using namespace std;
int main(int argc, char* argv[]){
    string path = "./instances/";
    DIR *dir;
    struct dirent *ent;
    if ((dir = opendir (path.c_str())) != NULL) {
    /* print all the files and directories within directory */
    while ((ent = readdir (dir)) != NULL) {
        printf ("%s\n", ent->d_name);
        std::string file_name(ent->d_name);
        std::string file = path + file_name;

        cout << file << endl;
        fstream fp(file.c_str());
        string buf;
        getline(fp, buf);
        int job;
        int machine;
        while(buf[0]=='#'){
            getline(fp, buf);
        }
        stringstream ss(buf);
        ss >> job >> machine;
        file_name = "./data_list/" + file_name + ".dat";
        fstream fp_2(file_name.c_str(), ios::out);
        if (fp_2.is_open()){
            fp_2 << "nbJobs = "<< job  << ";" << endl;
            fp_2 << "nbMchs = "<< machine << ";" << endl;
            fp_2 << "Ops = [" << endl;
            for( int i=0; i < job; i++){
                getline(fp, buf);
                stringstream ss(buf);
                fp_2 << "[";
                for (int i=0;i < machine; i++){
                    int m_id, process_time;
                    ss >> m_id >> process_time;
                    fp_2 << " <" << m_id << "," << process_time << "> ";
                    if(i != machine-1)fp_2 << ",";
                    else break;
                }
                fp_2 << "]";
                if(i != job-1) fp_2 << "," << endl;
                else fp_2 << endl;
            }
            fp_2 << "];" << endl;
        }
        fp_2.close();
    }
    closedir (dir);
    } else {
    /* could not open directory */
    perror ("");
    return EXIT_FAILURE;
    }
    return 0;
}
