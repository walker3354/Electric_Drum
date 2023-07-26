#!/usr/bin/python3
# sudo ifconfig can0 txqueuelen 10000
# sudo ip link set can0 up type can bitrate 1000000
from networkx import node_degree_xy
import tomli
import time
import canopen
import socketio
from playsound import playsound
import typing
import pygame
from pydub import AudioSegment
import time
pygame.init()
pygame.mixer.init()
import multiprocessing
beats = 0

def update_tempo(new_tempo):
    # Use the 'global' keyword to update the global variable 'tempo'
    global tempo
    tempo = new_tempo

    def proximity_callback(self, msg):
        node_id = msg.cob_id - 384
    for var in msg:
        if node_degree_xy == 31:
            # Update tempo using update_tempo function
            update_tempo((beats + 1) * 4)

music1 = pygame.mixer.Sound('bassDrum.mp3')
music2 = pygame.mixer.Sound('cymbal.mp3')
music3 = pygame.mixer.Sound('hiHat.mp3')
music4 = pygame.mixer.Sound('snare.mp3')
music5 = pygame.mixer.Sound('tomDrum.mp3')
music6 = pygame.mixer.Sound('tomDrum2.mp3')
music7 = pygame.mixer.Sound('tomDrum3.mp3')

class CsCanOpen:
    def __init__(self, can_interface, config_file):
        self.porx_node_list = []

        self.control_id = 0
        self.pre_control_id = 0
        self.control_id_temp = 0

        self.led_change = False
        self.led_flag = False

        self.send_key = False
        self.start_time = 0
        self.map_control = False
        self.message_key = True

        self.config = self.load_config(config_file)
        self.can_network = self.canopen_init(can_interface)
        self.load_prox_nodes(self.config["proximity"])
        self.prox_dict = {'right': 0, 'left': 0}

    def load_config(self, config_file):
        with open(config_file, "rb") as f:
            toml_dict = tomli.load(f)
            return toml_dict

    def canopen_init(self, can_interface="can0"):
        network = canopen.Network()
        network.connect(channel=can_interface, bustype='socketcan')
        return network

    def load_prox_nodes(self, config):
        print('\nloading prox_nodes\n')
        for node in config["nodes"]:
            print("Wait for prox_node {0:} ready...".format(node["node_id"]))
            can_node = self.can_network.add_node(
                node["node_id"], config["config_file"])
            can_node.tpdo.read()
            can_node.nmt.wait_for_heartbeat()
            self.porx_node_list.append(can_node)
        print("Check all prox nodes completed!")
        for node in self.porx_node_list:
            node.tpdo[1].add_callback(self.proximity_callback)

    def proximity_callback(self, msg):
        node_id = msg.cob_id - 384
        for var in msg:
            if node_id == 31:
                music1.play()
            elif node_id == 33:
                music4.play()
            elif node_id == 32:
                music3.play()
            elif node_id == 34:
                music5.play()
            elif node_id == 35:
                music2.play()
            print(node_id, " : ", var.raw)
            
 

def main():
    cs_canopen = CsCanOpen("can0", "/home/csl/drumelectric/cityscope-canopen-controller/walker_tw_island.toml")
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= 15:
            break

        time.sleep(0.5)
    
    return

if __name__ == "__main__":
    main()


'''
global tempo
tempo = (beats)*4
if 0 < tempo < 76:

    global speed
    speed = ("Slow")

elif 77 < tempo < 120:
    speed = ("Moderately")
                    
elif 121 < tempo < 200:
    speed = ("Fast")   

elif 200 < tempo:
    speed = ("Rapid")
print (tempo)
print (speed)

'''