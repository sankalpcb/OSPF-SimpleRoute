import socket
import sys
from threading import Thread
from threading import Lock
import argparse
import time 
import random
import numpy as np
import heapq

IP = "127.0.0.1"
START_PORT = 10000
INF = 100000
INFO_DICT = None
NEIGHBOUR_LIST = None
NEIGHBOUR_MATRIX = None
MAX_LEN = 1024
ADJ_MATRIX = None
ROUTING_TABLE = None
LAST_SEEN_SEQNO = None
PREV = None
RT_TIME = 0

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--node_id','-i', type=int,default=0)
    parser.add_argument('--input_file','-f', type=str,default='infile')
    parser.add_argument('--output_file','-o', type=str,default='outfile')
    parser.add_argument('--hello_interval','-t', type=int,default=1)
    parser.add_argument('--lsa_interval','-a', type=int,default=5)
    parser.add_argument('--spf_interval','-s', type=int,default=20)
    args = parser.parse_args()
    return args

def get_neighbours(Dict,id):
    neighbours = []
    for (i,j) in Dict.keys():
        if i == id and j not in neighbours:
            neighbours.append(j)
        if j == id and i not in neighbours:
            neighbours.append(i)
    return neighbours

def get_all_neighbours(no_routers):
    t = np.zeros(shape = (no_routers,no_routers),dtype=int).tolist()
    for (i,j) in INFO_DICT.keys():
        t[i][j] = 1
        t[j][i] = 1
    return t

def get_file_info(lines):
    dict = {}
    for it in range(1,len(lines)):
        C = {}
        line_info = lines[it].split()
        i = int(line_info[0])
        j = int(line_info[1])
        C['min'] = int(line_info[2])
        C['max'] = int(line_info[3])
        dict[(i,j)] = C
        dict[(j,i)] = C
    return dict

def get_seqno(no_routers):
    seq = {i:-1 for i in range(no_routers)}
    return seq

def initialize_RT(no_routers):
    rt = {}
    for i in range(no_routers):
        rt[i] = INF
        
    prev = {}
    for i in range(no_routers):
        prev[i] = None
        
    return rt,prev

def get_hello_pkt(id):
    return 'hello '+str(id)

def get_helloreply_pkt(i,j):
    cost_ij = random.randint(INFO_DICT[(i,j)]['min'],INFO_DICT[(i,j)]['max'])
    return 'helloreply'+' '+str(i)+' '+str(j)+' '+str(cost_ij)

def get_lsa_pkt(node_id,seqno,no_entries):
    s = 'lsa'+' '+str(node_id)+' '+str(seqno)+' '+ str(no_entries)
    for i in range(no_entries):
        s += ' ' + str(i) + ' ' + str(ADJ_MATRIX[node_id][i])
    return s

def get_path(node,path):
    
    if node == node_id or node == -1:
        return path 
    path += '<-' + str(PREV[node])
    return get_path(PREV[node],path)

# def print_path(node,path):
#     if node == node_id or node == -1:
#         return path 
#     print_path(parents[node], parents)
#     print(node, end=" ")

def write_into_outputfile(node_id,outfile):
    fd = open("output/"+outfile+"_"+str(node_id), 'a')
    # fd.write(str(n)+" "+str(l)+"\n")
    fd.write("ROUTING TABLE at time "+str(RT_TIME)+"\n")
    fd.write("Rno"+"\t|\t"+"Cost"+"\t|\t\t"+"Path\t\t\t"+"\n")
    fd.write("----|-----------|-----------------------\n")
    for i in ROUTING_TABLE.keys():
        if i != node_id:
            if ROUTING_TABLE[i] == INF :
                fd.write(str(i)+"\t|\t"+"INF"+"\t\t|\t\t"+"NO PATH"+"\t\t\t\n")
            else :
                fd.write(str(i)+"\t|\t"+str(ROUTING_TABLE[i])+"\t\t|\t\t"+get_path(i,str(i))+"\t\t\t\n")
        # fd.write(str(i)+" "+str(ROUTING_TABLE[i])+"\n")
    fd.write("\n")
    fd.close()

def recieve(node_id):
    global ADJ_MATRIX,LAST_SEEN_SEQNO
    PORT = START_PORT + node_id
    fd.bind((IP,PORT))
    while(1):
        recived_msg = fd.recvfrom(MAX_LEN)
        recived_msg = recived_msg[0].decode()
        # print("recieved",recived_msg)
        # sender_port = recived_msg[1].decode()
        msg_list = recived_msg.split()
        if msg_list[0] == 'hello':
            # send helloreply
            other_router_id = int(msg_list[1])
            pkt = get_helloreply_pkt(node_id,other_router_id)
            # pkt = get_helloreply_pkt(other_router_id,node_id)
            port = START_PORT+other_router_id
            fd.sendto(str.encode(pkt),(IP,port))
        
        elif msg_list[0] == 'helloreply':
            # update ADJ of neighbours
            neighbour_id = int(msg_list[1])
            costij = int(msg_list[3])
            with lock:
                ADJ_MATRIX[neighbour_id][node_id] = costij
                ADJ_MATRIX[node_id][neighbour_id] = costij
        
        elif msg_list[0] == 'lsa':
            # update ADJ matrix
            # print("initial")
            # print(ADJ_MATRIX)
            for i in range(1,4):
                msg_list[i] = int(msg_list[i])
            srcid,seqno,no_entries = msg_list[1:4]
            if seqno > LAST_SEEN_SEQNO[srcid]:
                # store info
                i = 4
                while i < len(msg_list):
                    router_id = int(msg_list[i])
                    cost = int(msg_list[i+1])
                    with lock:
                        ADJ_MATRIX[srcid][router_id] = cost
                        ADJ_MATRIX[router_id][srcid] = cost
                    i = i+2
                with lock :
                    LAST_SEEN_SEQNO[srcid] = seqno
                # print("final")
                # print(ADJ_MATRIX)
                # forward lsa
                for i in NEIGHBOUR_LIST:
                    # if i == sender_port :
                    #     continue
                    port = START_PORT+i
                    fd.sendto(str.encode(recived_msg),(IP,port))
        
        # elif msg_list[0] == 'down'
            

def send_hello(id,hello_interval):
    pkt = get_hello_pkt(id)
    while(1):
        for i in NEIGHBOUR_LIST:
            port = START_PORT + i
            fd.sendto(str.encode(pkt),(IP,port))
        time.sleep(float(hello_interval))

def send_lsa(id,no_routers,lsa_interval):
    seqno = 0
    while(1):
        for i in NEIGHBOUR_LIST:
            port = START_PORT + i
            pkt  = get_lsa_pkt(id,seqno,no_routers)
            fd.sendto(str.encode(pkt),(IP,port))
        time.sleep(float(lsa_interval))
        
def update_RT(node_id,spf_interval,outfile):
    global ROUTING_TABLE,PREV,RT_TIME
    while(1):
        
        # for i in ADJ_MATRIX:
        #     print(i)
        # print(node_id)
        # print(ADJ_MATRIX)
        
        shortest_path = {}
        previous = {i:-1 for i in range(len(ROUTING_TABLE))}
        unvisited = [i for i in range(len(ROUTING_TABLE))]
        
        for node in unvisited:
            shortest_path[node] = INF 
        
        shortest_path[node_id] = 0
        
        while unvisited :
            current_min_node = None 
            for node in unvisited :
                if current_min_node == None :
                    current_min_node = node
                elif shortest_path[node] < shortest_path[current_min_node]:
                    current_min_node = node  
            
            for neighbour in range(len(NEIGHBOUR_MATRIX[current_min_node])):
                if NEIGHBOUR_MATRIX[current_min_node][neighbour] != 1:
                    continue
                val = shortest_path[current_min_node] + ADJ_MATRIX[current_min_node][neighbour]
                if val <= shortest_path[neighbour]:
                    shortest_path[neighbour] = val
                    previous[neighbour] = current_min_node
            unvisited.remove(current_min_node)
        
        # lock here
        with lock :
            PREV = previous
            ROUTING_TABLE = shortest_path
        # print(PREV)
        write_into_outputfile(node_id,outfile)   
        RT_TIME += spf_interval
        time.sleep(float(spf_interval))
        
    

if __name__ == "__main__":
    args = parse()
    node_id = args.node_id
    input_file = args.input_file
    output_file = args.output_file
    hello_interval = args.hello_interval
    lsa_interval = args.lsa_interval
    spf_interval = args.spf_interval
    
    fd = open(input_file)
    lines = fd.readlines()
    fd.close()
    '''
        INFO_DICT contains the file info (i,j) -> {'min' : _ , 'max' : _ }
        NEIGHBOURS_LIST contains list of neighbours to node_id
        NEIGHBOURS_MATRIX of (i,j) is 1 if they have a link between them else zero
        ADJ_MATRIX (i,j) cost of link between i and j
        ROUTING TABLE i - > distance if this node from node i
        LAST_SEEN_SEQNO i -> last seen max seqno of the lsa form node i
    '''
    PORT = 10000 + node_id
    fd = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # fd.bind((IP,PORT))
    
    no_routers = int(lines[0].split()[0])
    no_links = int(lines[0].split()[1])
    INFO_DICT = get_file_info(lines)
    NEIGHBOUR_LIST = get_neighbours(INFO_DICT,node_id)
    NEIGHBOUR_MATRIX = get_all_neighbours(no_routers)
    ADJ_MATRIX = INF * np.ones(shape = (no_routers,no_routers),dtype=int)
    np.fill_diagonal(ADJ_MATRIX,0)
    ADJ_MATRIX = ADJ_MATRIX.tolist()
    LAST_SEEN_SEQNO = get_seqno(no_routers)
    ROUTING_TABLE,PREV = initialize_RT(no_routers)
    
    # print(NEIGHBOUR_LIST)
    # print(NEIGHBOUR_MATRIX)
    # print(ADJ_MATRIX)
    # print(LAST_SEEN_SEQNO)
    lock = Lock()
    T = [None]*4
    T[0] = Thread(target=recieve,args=[node_id])
    T[1] = Thread(target=send_hello,args=(node_id,hello_interval))
    T[2] = Thread(target=send_lsa,args=(node_id,no_routers,lsa_interval))
    T[3] = Thread(target=update_RT,args=(node_id,spf_interval,output_file))
    for i in range(3):
        T[i].daemon = True
    for i in range(4):
        T[i].start()
    
    sys.exit()
    
    for i in range(4):
        T[i].join()
    
    
    
    
    
      