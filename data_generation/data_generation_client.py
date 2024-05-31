import os
import random
import subprocess
import argparse
import concurrent.futures
import time

from bs4 import BeautifulSoup

tracks = ["aalborg", "alpine-1", "alpine-2", "brondehach", "corkscrew", "eroad", "forza", "g-track-1"]
          #"g-track-2", "g-track-3", "ole-road-1","ruudskogen","spring", "street-1","wheel-1", "wheel-2"]
dataPath = '..\\..\\data\\'

def add_track_to_xml(track):
    f = open("..\\..\\..\\torcs_server\\config\\raceman\\" + 'quickrace.xml','r')
    bs = BeautifulSoup(f.read(),'xml')
    f.close()

    trackName = bs.find('section',).find('attstr', {'name': 'name'})
    trackName['val'] = track

    bs = switch_drivers(bs)
 
    f = open("..\\..\\..\\torcs_server\\config\\raceman\\" + 'quickrace.xml','w')
    f.write(bs.prettify())
    f.close()

def switch_drivers(bs):
    trackName = bs.find('section', {'name': 'Drivers'})
    driver_sections = trackName.find_all('section', recursive=False)

    # Identify the scr_server section
    scr_server_section = None
    other_sections = []

    for section in driver_sections:
        module_tag = section.find('attstr', {'name': 'module'})
        if module_tag and module_tag['val'] == 'scr_server':
            scr_server_section = section
        else:
            other_sections.append(section)

    # Choose a random other section
    if other_sections:
        random_section = random.choice(other_sections)
        
        # Swap the 'module' values
        scr_server_module_tag = scr_server_section.find('attstr', {'name': 'module'})
        random_module_tag = random_section.find('attstr', {'name': 'module'})
        
        scr_server_module_tag['val'], random_module_tag['val'] = random_module_tag['val'], scr_server_module_tag['val']
    
    return bs


def run_subprocess(port):
    cmd = ['java', 'ahuraDriver.Client', 'ahuraDriver.DriverControllerE6', 'port:'+str(3001+ int(port)), 
       'host:localhost', 'id:SCR', 'maxEpisodes:1', 'maxSteps:0', 'stage:2', 'trackName:']
    track = tracks[7]
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
        for _ in range(1):
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
