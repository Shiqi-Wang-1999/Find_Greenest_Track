import argparse
from tracknaliser.load import query_tracks
import datetime

def process():
    """"Set the command line arguments"""
    parser= argparse.ArgumentParser(prog='greentrack', description="Find the greenest path")
    parser.add_argument('--start', nargs=2, type=int, default=[0,0], help="this is the start point coordinate of the track")
    parser.add_argument('--end', nargs=2, type=int, default=[299,299], help="this is the end point coordinate of the track")
    parser.add_argument('--verbose', action='store_true', help="to generate detailed description of the searched greenest track")

    arguments= parser.parse_args()

    try:
        tracks = query_tracks(start=(arguments.start[0],arguments.start[1]), end=(arguments.end[0],arguments.end[1]),n_tracks=50,save=False)
    except Exception as error:
        parser.error(error)
    track_greenest =tracks.greenest()

    # generate the attributes to be output
    corners= track_greenest.corners()
    co2 = track_greenest.co2()
    co2_round = round(co2,2)
    # To make the time displayed comply the form on requirement document
    time = datetime.timedelta(seconds=round(track_greenest.time()*3600))

    distance =[]
    direction= []
    toward=[]

    # specify the information to be generated under verbose mode
    for i in  range(1,len(corners)-1):
        direct_distance = abs(corners[i][0]-corners[i-1][0]+corners[i][1]-corners[i-1][1])
        distance.append(direct_distance)
        
        if corners[i][0]==corners[i-1][0] and corners[i][1]< corners[i-1][1]:
            direction.append('south')
            if corners[i][0] > corners[i+1][0] and i!= len(corners)-1:
                toward.append('left')
            elif corners[i][0] < corners[i+1][0] and i!= len(corners)-1:
                toward.append('right')

        elif corners[i][0]==corners[i-1][0] and corners[i][1]> corners[i-1][1]:
            direction.append('north')
            if corners[i][0] > corners[i+1][0] and i!= len(corners)-1:
                toward.append('left')
            elif corners[i][0] < corners[i+1][0] and i!= len(corners)-1:
                toward.append('right')

        elif corners[i][1] ==corners[i-1][1] and corners[i][0]> corners[i-1][0]:
            direction.append('east')
            if corners[i][1] >corners[i+1][1] and i != len(corners)-1:
                toward.append('down')
            elif corners[i][1] <corners[i+1][1] and i != len(corners)-1:
                toward.append('up')
        
        elif corners[i][1] ==corners[i-1][1] and corners[i][0]< corners[i-1][0]:
            direction.append('west')
            if corners[i][1] >corners[i+1][1] and i != len(corners)-1:
                toward.append('down')
            elif corners[i][1] <corners[i+1][1] and i != len(corners)-1:
                toward.append('up')

    
    # print out the result based on the argument "verbose"
    if (arguments.verbose):
        print('Path:\n- Start from'+str(corners[0]))
        for i in range(len(corners)-2):
            print('- Go '+direction[i]+' for '+str(distance[i]) +' km, turn '+ toward[i] +' at '+str(corners[i+1])  )

        print('- Go '+direction[-1]+' for '+str(distance[-1])+' km,'+'\n- reach your destination at '+str(corners[-1])+'\nCO2: '+str(co2_round)+' kg'+'\nTime: '+str(time))
    else:
        print('Path: '+str(corners)[:]+'\nCO2: '+str(co2_round)+' kg'+'\nTime: '+str(time))
        

if __name__ == "__main__":
    process()








