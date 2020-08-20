#!/usr/bin/env python
# -*- coding: utf-8	-*-
from __future__	import print_function

import RPi.GPIO	as GPIO
import time, os, signal, glob, subprocess, multiprocessing
from multiprocessing import Process, Queue, Lock
import MicrophoneStream	as	MS
from subprocess import check_output

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(29, GPIO.IN,	pull_up_down=GPIO.PUD_UP)
GPIO.setup(31, GPIO.OUT)
buttonStatus = 1

# set up an	empty list for the key presses
presses	= []
cmd_arg	= []

# turn LED off initially
GPIO.output(31,	False)

def	button_trigger():
	global	buttonStatus
	buttonStatus =	-1
	while True:
		#	wait	for	input to go	'low'
		input_value =	GPIO.input(29)
		if	not	input_value:
			#	log	start time	and	light the LED
			start_time =	time.time()
			GPIO.output(31, True)
			#	wait for input	to go high again
			while	not	input_value:
				input_value	= GPIO.input(29)
			else:
				# log the time the button is	un-pressed,	and	extinguish	LED
				end_time	= time.time()
				GPIO.output(31,	False)
				# store	the	press times	in the list,	as	a dictionary	object
				presses.append({'start':start_time,	'end':end_time})
				pressed_time	= end_time	- start_time
				print(pressed_time)

				if pressed_time	>= 4:
					buttonStatus =	3
				elif	pressed_time >=	1.5:
					MS.play_file("/home/pi/autorun/py_script/data/sample_sound.wav")
					buttonStatus =	2  
				elif	pressed_time >=	0.15:	
					buttonStatus =	1
					
				if(buttonStatus	== 2):
					print("Long	Pressed...\n")
			
			
		if buttonStatus == 2:
			MS.play_file("/home/pi/autorun/py_script/data/py_script.wav")
			py_path = '/home/pi/autorun/py_script/python3/'
			cmd_arg.insert(0, py_path)
			print("#########	Python Scrpit Execution	###########")
			result= find_file(cmd_arg[0])
			print("Result of	Exec Py	Script = " + result)
			
			if not result:
				print("File	Not	Found... \n")
			else:
				#result='/home/pi/ai-makers-kit/python3/ex1_kwstest.py'
				cmd_arg[0] = cmd_arg[0]	+ result
				print('Py Total	cm = ' + cmd_arg[0])
				print("execute	python scrpit....\n")
				print("Result of Exec Py Script	= "	+ result)
				subprocess.call(['python', result], cwd='/home/pi/autorun/py_script/python3')
				print("Python Script Process Finshed..." )
			buttonStatus	=	-1
			
		elif buttonStatus	== 1:
			proc1 = Process(target = say_ment)
			proc2 = Process(target = exec_bc)
			
			proc1.start()
			proc2.start()
			proc1.join()
			proc2.join()
			buttonStatus	=	-1

			print("Back to the Button Sencing Loop...")
			
			

def	kill_waste_proc(proc_name):		
	proc1 = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
	proc2 = subprocess.Popen(['grep', 'blockcoding'], stdin=proc1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
	out, err = proc2.communicate()
	print('out: {0}'.format(out))
	print('err: {0}'.format(err))
	
	
	for line in out.splitlines():
		if 'blockcoding' in	line:
			if 'grep' not in line:
				pid = line.split(None, 1)[1]
				pid = int(pid.split(' ', 1)[0])
				print(pid)
				os.kill(pid, signal.SIGKILL)
	
	os.system('ps -ef | grep block')


def get_pid(name):
    return map(int, check_output(["pidof",name]).split())

def	find_file(path):
	path =	path + '*'
	list_of_files = glob.glob(path) # * means all if need specific	format then	*.csv
	latest_file = max(list_of_files, key=os.path.getctime)
	print(type(latest_file))
	print(latest_file)
	return	latest_file


def say_ment():
	MS.play_file("/home/pi/autorun/py_script/data/bc_script.wav")
	print("Block coding mention Finshed...")

def exec_bc():
	global buttonStatus
	bc_path = '/home/pi/autorun/block/'
	cmd_arg.insert(0, bc_path) 
	print("########### Block	Coding Scprit Execution	#########")
	result= find_file(cmd_arg[0])
	print("Result of	Exec Block Coding Script = " + result)
	#Kill the waste Process....
	print("###### Kill the waste Process.... #####")
	kill_waste_proc('blockcoding')
	##### check all block coding processes died.....
	print("\n\n\n###### Checking Block Coding Process End........######")
	os.system('ps -ef | grep block')
	#######################
	if not result:
		print("File	Not	Found... \n")
	else:
		print("execute	blocking	code idle....\n")
		subprocess.call(['./block_autorun.sh', result], cwd='/home/pi/blockcoding/kt_ai_makers_kit_block_coding_driver/blockDriver')
		print("Block Coding	Script Process Finshed...")
		buttonStatus	=	-1	
	

def	main():
	button_trigger()

if __name__	== '__main__':
	main()