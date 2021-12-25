
def getConnectedChannels(slug):
	#getConnectedChannels(slug) = [c1,c2,...]
	#slug: channel slug str
	#[c1,c2,...] where c1,c2,... is linked to the current channel

	GET = f'http://api.are.na/v2/channels/{slug}/connections'
	try:
	    collab_json_list = requests.get(GET).json()['channels']
	except:
	    return []
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

def multi_generateChannelNetwork(startSlug, num_threads):
	def get_connected_channels_from_queue(queue,curr_list):
		while True:
			slug = queue.get()
			slugs = getConnectedChannels(slug)
			curr_list.append(slugs)
			queue.task_done()
	l = []
	q = Queue(startSlug)
	for i in range(num_threads):
		worker = Thread(target=multi_generateChannelNetwork, args=(q,l))
		worker.start()

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
	import scrape_utils
	
	main()
	











