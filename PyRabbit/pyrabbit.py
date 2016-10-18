from publisher import publisher
import argparse,json,importlib
from microservices.test_runner import test_runner
from SSHTunnel import SSHTunnel
import logging


class pyrabbit(object):

    
    def __init__(self,args): 
        logging.basicConfig(level=logging.DEBUG)   
        sshTunnel = None
        try:     
                     
            ms_list = args.ms
            environment = args.environment

            ms_list = str(ms_list).split(',')
       
            with open('config.json') as data_file:
                content =  data_file.read()
                data = json.loads(content)
            config = data[environment]
            environments = ['qa','demo','dev']
            if environment in environments:
                sshTunnel = SSHTunnel(ssh_host=config['remote_address'],username=config['remote_user'],key_file='C:\Projects\ezydev-key.pem',local='56772',remote=config['remote_host'])
                sshTunnel.forward()
            publisherObj = publisher(host=config['rabbitmq_host'],username=config['username'],password=config['password'])

            queue_names = data['queue_names']
            test_dir = data['test_location']

        
            for ms in ms_list:
                print (ms)
                publisherObj.connect()
                tr = test_runner(microservice_name=ms,queue_name=queue_names[ms],test_dir=test_dir)
                tr.record_count = int(args.rc)
                tr.execute(publisher=publisherObj)
        except Exception as exp:
            print (repr(exp))
        finally:
            if sshTunnel is not None:
                sshTunnel.terminate()
        
        

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process command line args')
    parser.add_argument('--ms', help='Microservice  help')
    parser.add_argument('--environment', help='Environment help')
    parser.add_argument('--rc', help='Record Count help',default=1)
    args = parser.parse_args()    
    return args

if __name__ == '__main__':
    pyrabbit(parse_arguments())          
        
