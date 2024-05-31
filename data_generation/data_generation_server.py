import time
from bs4 import BeautifulSoup
import os
import subprocess
import copy
import concurrent.futures
import random as rand

def open_xml():
    f = open(data_gen_path + 'temp.xml','r')
    bs = BeautifulSoup(f.read(),'xml')
    f.close()
    return bs

def write_xml(bs):
    f = open(data_gen_path + 'temp.xml','w')
    f.write(bs.prettify())
    f.close()

def display_xml():
    bs = open_xml()
    print (bs.find('section',{'name':'Tracks'}))
    print (bs.find('section',{'name':'Drivers'}))

def swap_and_write(currentIdx):
    bs = open_xml()
    current = bs.find('section',{'name':'Drivers'}).find('section',{'name':str(currentIdx)})
    nxt = bs.find('section',{'name':'Drivers'}).find('section',{'name':str(currentIdx+1)})
    
    tmp = copy.deepcopy(current)
    current = copy.deepcopy(nxt)
    nxt = tmp
    
    tmp2 = copy.deepcopy(current['name'])
    current['name'] = copy.deepcopy(nxt['name'])
    nxt['name'] = tmp2
    
    bs.find('section',{'name':'Drivers'}).find('section',{'name':str(currentIdx)}).replaceWith(current)
    bs.find('section',{'name':'Drivers'}).find('section',{'name':str(currentIdx+1)}).replaceWith(nxt)
    
    write_xml(bs)

def randomize_drivers(bs):
    # Find all drivers
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

    # Choose a random other section for swapping
    if other_sections:
        random_section = rand.choice(other_sections)
        
        # Swap the 'module' and 'idx' values
        scr_server_module_tag = scr_server_section.find('attstr', {'name': 'module'})
        scr_server_idx_tag = scr_server_section.find('attnum', {'name': 'idx'})
        random_module_tag = random_section.find('attstr', {'name': 'module'})
        random_idx_tag = random_section.find('attnum', {'name': 'idx'})
        
        # Swap values
        scr_server_module_tag['val'], random_module_tag['val'] = random_module_tag['val'], scr_server_module_tag['val']
        scr_server_idx_tag['val'], random_idx_tag['val'] = random_idx_tag['val'], scr_server_idx_tag['val']

    return bs

def run_subprocess(port):
    # Using Popen instead of call for non-blocking execution
    f = open("..\\torcs_server\\config\\raceman\\" + 'quickrace.xml','r')
    bs = BeautifulSoup(f.read(),'xml')
    f.close()

    # Set correspondig ID for the scr_server port
    driver_section = bs.find('attstr', {'name': 'module', 'val': 'scr_server'}).find_parent('section')
    idx_attr = driver_section.find('attnum', {'name': 'idx'})
    idx_attr['val'] = str(port)  # Set the new idx value here

    randomize_drivers(bs)

    f = open("..\\torcs_server\\config\\raceman\\" + 'quickrace.xml','w')
    f.write(bs.prettify())
    f.close()

    # Start torcs server
    process = subprocess.Popen(['wtorcs.exe', '-r', '.\\temp.xml', '-nodamage', '-nofuel'])
    return process

if __name__ == "__main__":
    server_path = '..\\torcs_server'
    os.chdir(server_path)
    data_gen_path = '..\\data_generation\\'
    # display_xml()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _ in range(1):
            futures.append(executor.submit(run_subprocess(_)))
            time.sleep(2)  # Wait for 2 seconds before starting the next subprocess