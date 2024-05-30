import os
import subprocess
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port", action="store", type=str, help="Name of the model to be trained")
    args = parser.parse_args()
     
    os.chdir(r".\\Ahura\\bin")
    cmd = ['java', 'ahuraDriver.Client', 'ahuraDriver.DriverControllerE6', 'port:'+args.port, 
       'host:localhost', 'id:SCR', 'maxEpisodes:1', 'maxSteps:0', 'stage:2', 'trackName:forza']
    categories = ['road', 'dirt', 'oval']

    for category in categories:
        print ('Category:',category)
        tracks = sorted(os.listdir(r'..\\..\\..\\torcs_server\\tracks\\'+category))
        if category == 'road':
            tracks.remove('e-track-1')
            tracks.remove('e-track-2')
        for track in tracks:
            print ('Track:',track)
            for race_num in range(1,31):
                print ('Race Number:',race_num)
                full_cmd = list(cmd)
                full_cmd[-1] = full_cmd[-1] + track
                full_cmd.append(str(race_num))
                subprocess.call(full_cmd)
