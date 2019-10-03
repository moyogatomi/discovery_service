from discovery_service.args import args
import time 
def run_entrypoint():
	if not len(args.typeargs):
		raise Exception('What kind of service you want to use? listener | Telegram | Lighthouse | Info ?')

	if args.typeargs[0]== 'Listener':
	    from discovery_service import listener,logmaster,utils
	    logger = logmaster.logger_obj("UDP listener", level=args.log)
	    logger.info("Initialized sniffer")
	    udp_sniff = listener.UDPBroadcast()
	    udp_sniff.loop_forever()

	    while True:
	        time.sleep(1)

	if args.typeargs[0]== 'Telegram':
	    from discovery_service import utils
	    bclient = utils.UDPTools()
	    if not args.broadcast_address:
	        raise Exception('Add broadcast address --broadcast_address')
	    if not args.m:
	        raise Exception('Add message --m')
	    bclient.broadcast_address = args.broadcast_address
	    bclient.port = args.port
	    bclient.send(args.m)

	if args.typeargs[0]== 'Lighthouse':
	    from discovery_service import service
	    service.cli()

	if args.typeargs[0]== 'Info':
	    from discovery_service import utils
	    b_info = utils.BroadcastAddress.bca_awk()
	    for i in b_info:
	    	print(f"Your ip: {i[0]}, your broadcast addres: {i[1]}")
