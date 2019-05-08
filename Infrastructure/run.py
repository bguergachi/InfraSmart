import os, sys
sys.path.append('C:/Users/agsof/Documents/GitHub/InfraSmart/Infrastructure')

for i in ['zone_1', 'zone_2', 'zone_3', 'zone_4']:
    os.system("python main.py "+i)
