import os
import subprocess
import argparse
import concurrent.futures
import time

from bs4 import BeautifulSoup

tracks = ["aalborg", "alpine-1", "alpine-2", "brondehach", "corkscrew", "eroad", "forza", "g-track-1", "g-track-2", "g-track-3", "ole-road-1","ruudskogen","spring", "street-1","wheel-1", "wheel-2"]
dataPath = '..\\..\\data\\'

def add_track_to_xml(track):
    f = open("..\\..\\..\\torcs_server\\config\\raceman\\" + 'quickrace.xml','r')
    bs = BeautifulSoup(f.read(),'xml')
    f.close()

    trackName = bs.find('section', {'name': 'Tracks'}).find('attstr', {'name': 'name'})
    # trackName = bs.find('section',).find('attstr', {'name': 'name', 'val': 'wheel-1'})
    trackName['val'] = track
 
    f = open("..\\..\\..\\torcs_server\\config\\raceman\\" + 'quickrace.xml','w')
    f.write(bs.prettify())
    f.close()


def run_subprocess(port):
    cmd = ['java', 'ahuraDriver.Client', 'ahuraDriver.DriverControllerE6', 'port:'+str(3001+ int(port)), 
       'host:localhost', 'id:SCR', 'maxEpisodes:1', 'maxSteps:0', 'stage:2', 'trackName:']
    track = tracks[2]
    add_track_to_xml(track)
    full_cmd = list(cmd)
    full_cmd[-1] = full_cmd[-1] + track

    directory_path = dataPath+track

    # Check if the directory exists
    if not os.path.exists(directory_path):
        # If the directory does not exist, create it
        os.makedirs(directory_path)
    
    files = os.listdir(directory_path)
    len(files)
    full_cmd.append(str(len(files)+port))
    # subprocess.call(full_cmd)
    process = subprocess.Popen(full_cmd)
    return process

if __name__ == "__main__":  
     
    os.chdir(r".\\Ahura\\bin")
    # cmd = ['java', 'ahuraDriver.Client', 'ahuraDriver.DriverControllerE6', 'port:'+args.port, 
    #    'host:localhost', 'id:SCR', 'maxEpisodes:1', 'maxSteps:0', 'stage:2', 'trackName:forza']
    # categories = ['road', 'dirt', 'oval']

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _ in range(2):
            futures.append(executor.submit(run_subprocess(_)))
            
            # time.sleep(2)  # Wait for 2 seconds before starting the next subprocess

    # for category in categories:
    #     print ('Category:',category)
    #     tracks = sorted(os.listdir(r'..\\..\\..\\torcs_server\\tracks\\'+category))
    #     if category == 'road':
    #         tracks.remove('e-track-1')
    #         tracks.remove('e-track-2')
    #     for track in tracks:
    #         print ('Track:',track)
    #         # for race_num in range(1,31):
    #         #     print ('Race Number:',race_num)
    #         #     full_cmd = list(cmd)
    #         #     full_cmd[-1] = full_cmd[-1] + track
    #         #     full_cmd.append(str(race_num))
    #         #     subprocess.call(full_cmd)
    #         print ('Race Number:',args.port)
    #         full_cmd = list(cmd)
    #         full_cmd[-1] = full_cmd[-1] + track
    #         full_cmd.append(str(args.port))
    #         subprocess.call(full_cmd)
