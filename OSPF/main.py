

from multiprocessing import Process
import os
import argparse
import socket
import sys

# IP = "127.0.0.1"
# PORT = 20000
# MAX_LEN = 1024

def parse():
    parser = argparse.ArgumentParser()
    # parser.add_argument('--no_nodes','-n', type=int,default=3)
    parser.add_argument('--input_file','-f', type=str,default='infile')
    parser.add_argument('--output_file','-o', type=str,default='outfile')
    parser.add_argument('--hello_interval','-t', type=int,default=1)
    parser.add_argument('--lsa_interval','-a', type=int,default=5)
    parser.add_argument('--spf_interval','-s', type=int,default=20)
    args = parser.parse_args()
    return args

def run_routers(node_id):
    command = "python3 router.py -i "+str(node_id)+" -f "+input_file+" -o "+output_file+" -t "+str(hello_interval)+" -a "+str(lsa_interval)+" -s "+str(spf_interval)
    os.system(command)

# def terminator():
#     fd = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
#     fd.bind((IP,PORT))
#     recived_msg = fd.recvfrom(MAX_LEN)
#     recived_msg = recived_msg[0].decode()
#     print("Terminating !")
#     return

if __name__ == '__main__':
    args = parse()
    # no_nodes = args.no_nodes
    input_file = args.input_file
    output_file = args.output_file
    hello_interval = args.hello_interval
    lsa_interval = args.lsa_interval
    spf_interval = args.spf_interval
    
    fd = open(input_file)
    lines = fd.readlines()
    fd.close()
    
    no_nodes = int(lines[0].split()[0])
    no_links = int(lines[0].split()[1])
    
    P = []
    for i in range(no_nodes):
        p = Process(target=run_routers, args=[i])
        p.daemon = True
        P.append(p)
    
    # P.append(Process(target=terminator, args=()))    
        
    for p in P:
        p.start()
        
    # sys.exit()
    for p in P:
        p.join()
    
