#!/usr/bin/python3
# sudo ifconfig can0 txqueuelen 10000
# sudo ip link set can0 up type can bitrate 1000000
import tomli
import time
import canopen
import socketio

import typing

sio = socketio.Client()


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
            print(node_id, " : ", var.raw)

   


def main():
    cs_canopen = CsCanOpen("can0", "/home/csl/drumelectric/cityscope-canopen-controller/walker_tw_island.toml")
    while True:
        time.sleep(0.5)
    return


if __name__ == "__main__":
    main()
