
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

def multithread_generateChannelNetwork(startSlugs, num_threads):
    def get_connected_channels_from_queue(queue,r):
        while True:
            slug = queue.get()
            slugs = getConnectedChannels(slug)            
            for slug in slugs:
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


    

def main():
	parser = argparse.ArgumentParser(description='startSlug')
	parser.add_argument('--slug',type=str, required = True)
	parser.add_argument('--depth', type=int, required = True)
	args = parser.parse_args()
	network = generateChannelNetwork(args.slug,args.depth)


if __name__ == "__main__":
	
	import requests
	import math
	import networkx as nx
	from queue import Queue
	from threading import Thread
	import argparse
	print("fart")
	
	# main()
	











