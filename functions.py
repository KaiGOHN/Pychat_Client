#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import os.path
import pickle
import socket
import re
import time
from threading import Thread
from tkinter.messagebox import *


def set_icon(window):
    window.wm_iconbitmap("pychat_icon.ico")


def readcfg(list):
    config = configparser.ConfigParser()
    config.read('client_config.ini')
    for item in list:
        config = config[item]
    return str(config)


def connect(host, port):
    try:
        connexion_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion_server.connect((host, int(port)))
        return connexion_server
    except:
        return "err1"


def send(message, connexion_server):
    connexion_server.send(pickle.dumps(message))


def recv(connexion_server):
    received_message = connexion_server.recv(1024)
    return pickle.loads(received_message)


def disconnect(connexion_server):
    connexion_server.shutdown(1)
    connexion_server.close()


def login(username, password):
    connexion_server = connect(readcfg(['SOCKET', 'host']), readcfg(['SOCKET', 'port']))
    if connexion_server == "err1":
        showwarning('ERR1', 'SERVEUR INACESSIBLE')
    else:
        message = ["login", username, password]
        send(message, connexion_server)
        received_message = recv(connexion_server)
        disconnect(connexion_server)
        if received_message is True:
            return True
        if received_message is False:
            return False
        elif received_message == "err3":
            showwarning('ERR3', 'BASE DE DONNÉE INACESSIBLE')


def sendmsg(username, channel, password, msg):
    connexion_server = connect(readcfg(['SOCKET', 'host']), readcfg(['SOCKET', 'port']))
    if connexion_server == "err1":
        showwarning('ERR1', 'SERVEUR INACESSIBLE')
    else:
        message = ["sendmsg", username, channel, password, msg]
        send(message, connexion_server)
        received_message = recv(connexion_server)
        disconnect(connexion_server)
        if received_message is True:
            return True
        elif received_message == "err3":
            showwarning('ERR3', 'BASE DE DONNÉE INACESSIBLE')


def connexion_channel(channel, password):
    connexion_server = connect(readcfg(['SOCKET', 'host']), readcfg(['SOCKET', 'port']))
    if connexion_server == "err1":
        showwarning('ERR1', 'SERVEUR INACESSIBLE')
    else:
        message = ["connexion_channel", channel, password]
        send(message, connexion_server)
        received_message = recv(connexion_server)
        if received_message == "err3":
            showwarning('ERR3', 'BASE DE DONNÉE INACESSIBLE')
        disconnect(connexion_server)
        return received_message


def used_channel(channel, password):
    connexion_server = connect(readcfg(['SOCKET', 'host']), readcfg(['SOCKET', 'port']))
    if connexion_server == "err1":
        showwarning('ERR1', 'SERVEUR INACESSIBLE')
    else:
        message = ["used_channel", channel, password]
        send(message, connexion_server)
        received_message = recv(connexion_server)
        if received_message == "err3":
            showwarning('ERR3', 'BASE DE DONNÉE INACESSIBLE')
        disconnect(connexion_server)
        return received_message


def new_channel(user, channel, password):
    connexion_server = connect(readcfg(['SOCKET', 'host']), readcfg(['SOCKET', 'port']))
    if connexion_server == "err1":
        showwarning('ERR1', 'SERVEUR INACESSIBLE')
    else:
        message = ["new_channel", user, channel, password]
        send(message, connexion_server)
        received_message = recv(connexion_server)
        if received_message == "err3":
            showwarning('ERR3', 'BASE DE DONNÉE INACESSIBLE')
        disconnect(connexion_server)
        return received_message


def chan_delete(username, userpassword, channel, password):
    connexion_server = connect(readcfg(['SOCKET', 'host']), readcfg(['SOCKET', 'port']))
    if connexion_server == "err1":
        showwarning('ERR1', 'SERVEUR INACESSIBLE')
    else:
        message = ["del_channel", username, userpassword, channel, password]
        send(message, connexion_server)
        received_message = recv(connexion_server)
        if received_message == "err3":
            showwarning('ERR3', 'BASE DE DONNÉE INACESSIBLE')
        disconnect(connexion_server)
        return received_message


def loadidslist(channel, password):
    connexion_server = connect(readcfg(['SOCKET', 'host']), readcfg(['SOCKET', 'port']))
    if connexion_server == "err1":
        print('ERR1', 'SERVEUR INACESSIBLE')
    message = ["loadidslist", channel, password]
    send(message, connexion_server)
    received_message = recv(connexion_server)
    if received_message == "err3":
        print('ERR3', 'BASE DE DONNÉE INACESSIBLE')
    disconnect(connexion_server)
    return received_message


def get_msg(id, channel, password):
    connexion_server = connect(readcfg(['SOCKET', 'host']), readcfg(['SOCKET', 'port']))
    if connexion_server == "err1":
        print('ERR1', 'SERVEUR INACESSIBLE')
    message = ["get_msg", id, channel, password]
    send(message, connexion_server)
    received_message = recv(connexion_server)
    if received_message == "err3":
        print('ERR3', 'BASE DE DONNÉE INACESSIBLE')
    disconnect(connexion_server)
    return received_message


def get_chan_name(channel):
    connexion_server = connect(readcfg(['SOCKET', 'host']), readcfg(['SOCKET', 'port']))
    if connexion_server == "err1":
        print('ERR1', 'SERVEUR INACESSIBLE')
    message = ["get_chan_name", channel]
    send(message, connexion_server)
    received_message = recv(connexion_server)
    if received_message == "err3":
        print('ERR3', 'BASE DE DONNÉE INACESSIBLE')
    disconnect(connexion_server)
    return received_message


def register(username, password, first_name, last_name, email):
    connexion_server = connect(readcfg(['SOCKET', 'host']), readcfg(['SOCKET', 'port']))
    if connexion_server == "err1":
        showwarning('ERR1', 'SERVEUR INACESSIBLE')
    else:
        message = ["register", username, password, first_name, last_name, email]
        send(message, connexion_server)
        received_message = recv(connexion_server)
        disconnect(connexion_server)
        if received_message == "err3":
            showwarning('ERR3', 'BASE DE DONNÉE INACESSIBLE')
        if received_message is True:
            return True
        elif received_message is False:
            return False


def check_cfg():
    if os.path.exists("client_config.ini") is False:
        config = configparser.ConfigParser()
        config.read('client_config.ini')
        config['SOCKET'] = {'host': 'localhost',
                            'port': '1111'}
        with open('client_config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        config = configparser.ConfigParser()
        config.read('client_config.ini')
        if ('SOCKET' in config) is False:
            os.remove("client_config.ini")
            config['SOCKET'] = {'host': 'localhost',
                                'port': '1111'}
            with open('client_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('host' in config['SOCKET']) is False:
            config['SOCKET']['host'] = 'localhost'
            with open('client_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('port' in config['SOCKET']) is False:
            config['SOCKET']['port'] = '1111'
            with open('client_config.ini', 'w') as configfile:
                config.write(configfile)
