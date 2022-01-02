def main():
    parser = argparse.ArgumentParser(description='startSlug')
    parser.add_argument('--slug',type=str, required = True)
    parser.add_argument('--num_threads', type=int, required = True)
    parser.add_argument('--depth', type=int, required = True)
    parser.add_argument('--dic', type=bool, required=True)
    args = parser.parse_args()
    bfs_channels('tests','arena-urls',[args.slug],args.num_threads, args.depth, args.dic)
    

if __name__ == "__main__":

    import requests
    import math
    import networkx as nx
    from queue import Queue
    from threading import Thread
    from scrape_utils import bfs_channels
    import argparse
    main()