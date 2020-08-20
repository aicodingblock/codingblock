#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import RPi.GPIO as GPIO
import time, os, signal, glob, subprocess, multiprocessing
from multiprocessing import Process, Queue, Lock
import MicrophoneStream as  MS
from subprocess import check_output

import asyncio
import sys
import http.client as httplib
loop = None

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(31, GPIO.OUT)
buttonStatus = 1

key_path = '/home/pi/blockcoding/kt_ai_makers_kit_block_coding_driver/blockDriver/key/codingPackKey.json'
cmd_arg = []
# turn LED off initially

class btn_exe(object):
    def __init__(self):
        print("__init__ button execution")
    
    def internet_check(self):
        conn = httplib.HTTPConnection("www.google.com", timeout=5)
        try:
            conn.request("HEAD", "/")
            conn.close()
            return True
        except:
            conn.close()
            return False

    def find_file(self, path):
        path =  path + '*'
        list_of_files = glob.glob(path) # * means all if need specific  format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        print(type(latest_file))
        print(latest_file)
        return  latest_file

    def kill_waste_proc(self):     
        proc1 = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
        proc2 = subprocess.Popen(['grep', 'v7'], stdin=proc1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
        out, err = proc2.communicate()
        print('out: {0}'.format(out))
        print('err: {0}'.format(err))
        
        
        for line in out.splitlines():
            line = line.decode()
            if 'v7' in line:
                if 'grep' not in line:
                    pid = line.split(None, 1)[1]
                    pid = int(pid.split(' ', 1)[0])
                    print(pid)
                    os.kill(pid, signal.SIGKILL)
        os.system('ps -ef | grep block')
    def execute_codingpack(self):
        if self.internet_check():
            if os.path.exists(key_path):
                GPIO.output(31, True)
                print ("Start AI Coding Block Button Execution ...")
                MS.play_file("/home/pi/autorun/py_script/data/bc_script.wav")
                print("Block coding mention Finshed...")
                bc_path = '/home/pi/autorun/block/'
                cmd_arg.insert(0, bc_path) 
                result= self.find_file(cmd_arg[0])
                self.kill_waste_proc()
                print("\n\n\n###### Checking Block Coding Process End........######")
                os.system('ps -ef | grep block')
                if not result:
                    print("File Not Found... \n")
                else:
                    print("execute  blocking    code idle....\n")
                    subprocess.call(['./block_autorun.sh', result], cwd='/home/pi/blockcoding/kt_ai_makers_kit_block_coding_driver/blockDriver')
                    print("Block Coding Script Process Finshed...")
                    buttonStatus = -1
                self.kill_waste_proc()
                GPIO.output(31, False)
            else:
                print("No key...")
                MS.play_file("/home/pi/autorun/py_script/data/no_key.wav")
                
        else:
            print ("Network not Connected...")
            MS.play_file("/home/pi/autorun/py_script/data/no_wifi.wav")

    def btn_callback(self, execute_codingpack):
        if loop is None:
            print(":(")
            return       # should not come to this
        
        execute_codingpack()
        # this enqueues a call to message_manager_f() 
        #loop.call_soon_threadsafe(execute_codingpack)

# this is the primary thread mentioned in Part 2
if __name__ == '__main__':
    try:
        # setup the GPIO
        '''
        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN) # adjust the PULL UP/PULL DOWN as applicable
        GPIO.add_event_detect(4, GPIO.RISING, callback=lambda x: self.btn_callback(message_manager_f), bouncetime=500)
        '''
        btn = btn_exe()
        GPIO.output(31, False)
        GPIO.add_event_detect(29, GPIO.RISING, callback=lambda x: btn.btn_callback(btn.execute_codingpack), bouncetime=500)
        # run the event loop
        loop = asyncio.get_event_loop()
        loop.run_forever()
        loop.close()
    except :
        print("Error:", sys.exc_info()[0])

    # cleanup
    GPIO.cleanup()