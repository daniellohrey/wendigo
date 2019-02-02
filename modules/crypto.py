#uses nightminer by ricmoo to mine crypto currencies
#need to copy nightminer.py file into modules directory to import
#mines forever, and takes the following options (all mandatory)
#url - crypto server
#usr - username for server
#pwd - password for server

import nightminer

def run(config, **args):
	try:
		miner = nightminer.Miner(args["url"], args["usr"], args["pwd"])
		miner.serve_forever()
	except:
		return None, None
