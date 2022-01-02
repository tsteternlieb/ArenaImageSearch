
import networkx
from functools import reduce
import logging
import boto3
from botocore.exceptions import ClientError
import os
from queue import Queue
from threading import Thread 
import pickle
import requests

    

def write(data: dict, bucket_name: str, name: str):
    """function for writing data to s3 buckets st 
    we get bucket_name/name/fringe for example      

    Args:
        data (dict): dict of names to data
        bucket_name (str): url of bucket to write to
        name (str): name of current container process
    """
    s3 = boto3.resource('s3')
    for k,v in data.items():
        object = s3.Object(bucket_name, f'{name}/{k}')
        b = pickle.dumps(data)
        object.put(Body = b)
        
def getConnectedChannels(slug):
	#getConnectedChannels(slug) = [c1,c2,...]
	#slug: channel slug str
	#[c1,c2,...] where c1,c2,... is linked to the current channel

    GET = f'http://api.are.na/v2/channels/{slug}/connections'
    try:
        collab_json_list = requests.get(GET).json()['channels']
    except:
        collab_json_list = []
    slugs = [json['slug'] for json in collab_json_list]

    return slugs
# print(getConnectedChannels('nynets-_sal8iqlt8y'))
def generateChannelNetwork(startSlug,depth):
    '''
    bfs for network generation 
    generateChannelNetwork(startSlug,depth) = network : networkx 
    where nodes represent channels and edges exist if one channels appear in another 
    '''
    q = Queue()
    seen = set([startSlug])
    q.put(startSlug)
    G = nx.Graph()
    
    while depth > 0:
        for i in range(q.qsize()):
            curr_slug = q.get_nowait()
            slugs = getConnectedChannels(curr_slug)
            for slug in slugs:
                if slug not in seen:
                    seen.add(slug)
                    q.put(slug)
                        
                    G.add_edge(curr_slug,slug)
                    
                
        depth -= 1
        
    return G

def multi_generateChannelNetwork(startSlugs, num_threads,dic=False, seen = []):
    def get_connected_channels_from_queue(queue,r):
        while True:
            slug = queue.get()
            slugs = getConnectedChannels(slug)   
            if dic:
                if slug not in seen:
                    r.put((slug,slugs))
            else:
                for slug in slugs:
                    if slug not in seen:
                        r.put(slug)
            queue.task_done()

    res = Queue()
    q = Queue()
    for slug in startSlugs:
        q.put(slug)
    
    for i in range(num_threads):
        worker = Thread(target=get_connected_channels_from_queue, args=(q,res))
        worker.setDaemon(True)
        worker.start()
        
    q.join()
    return list(res.queue)

def bfs_channels(name,
                 bucket_name,
                 fringe, 
                 num_threads, 
                 depth,
                 dic):
    """function for exploring urls in a bfs manner

    Args:
        fringe (list): starting slugs to explore from
        num_threads (int): number of threads to use
        depth (int): depth of exploration
        dic (bool): whether or not to generate adjacency dictionary

    """
    # print(fringe)
    dic_results = None
    seen = []
    if dic:
        dic_results = []
    for itr in range(depth):
        print(itr)
        curr_res = multi_generateChannelNetwork(fringe, num_threads,dic, seen)
        
        if dic:
            dic_results.extend(curr_res)
            
            curr_res_keys_ = list(map(lambda x: x[0], curr_res))
            curr_res_vals_ = list(reduce(lambda x,y: x+y[1],curr_res,[]))
             
            seen.extend(curr_res_keys_)
            fringe = curr_res_vals_
        else:
            fringe = curr_res
    print("1343")
    
    dic = {'seen':seen,'dic_results' : dic_results,'fringe' :fringe}
    # print(dic)
    write(dic,
          bucket_name,
          name)
    
# l = ['nynets-_sal8iqlt8y']
# (bfs_channels("e","arena-urls",l,50,2,True))
            
        


    

# def main():
#     parser = argparse.ArgumentParser(description='startSlug')
#     parser.add_argument('--slug',type=str, required = True)
#     parser.add_argument('--depth', type=int, required = True)
#     args = parser.parse_args()
#     network = bfs_channels()
#     print(network)

# if __name__ == "__main__":
	
# 	import requests
# 	import math
# 	import networkx as nx
# 	from queue import Queue
# 	from threading import Thread
# 	import argparse
# 	print("fart")
	
# 	main()
	











