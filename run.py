from subprocess import STDOUT, check_output
import os
import subprocess


python_file="prubik4x2.py"

m_array=[30,60,90,120,150,180,210,240,270,300,330,360]

solver="RTM4x2"
input_path="./data/instances/"
output_path="./data/solutions/"


for m in m_array:
    for k in range(20):
        file_name=str(m)+"/"+str(k)+".ymal"
        cmd=["python",python_file,"--f",input_path+file_name,"--o",output_path+solver+"/"+file_name]
        try:
            #check_output(cmd,stderr=STDOUT,timeout=300, shell=True).decode('utf-8')
            subprocess.call(cmd,shell=True)
        except subprocess.CalledProcessError as e:
            pass
            #raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

