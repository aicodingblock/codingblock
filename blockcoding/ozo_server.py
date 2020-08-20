# from ozolib import ozolib
import ozolib
import time
import socket

DEBUG = False
def log(s):
    if DEBUG:
        print(s)

HOST='' 
PORT=50123 
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server_socket.bind((HOST,PORT))
except OSError as e:
    print(e)
    exit(1)
log("server started")

while True:
    server_socket.listen(1) 
    client_socket, addr=server_socket.accept()
    log('Connected by {}'.format(addr))
    data=client_socket.recv(1024)
    if data:
        data = data.decode('utf-8').lower()
        com = data.split(' ')
        param_cnt = len(com)
        log("com:{}, count:{}".format(com,param_cnt))
        if com[0]=='maru_oconnect':
            if 'bot1' in locals():  #이미 연결된 로봇이 있으면 연결안함
                if bot1.bisconnected() is True:
                    ret = "Already Connencted"
                else:
                    del bot1
            if 'bot1' not in locals():
                ozo = ozolib.Ozo()
                if param_cnt>=2:
                    robot = ozo.find(com[1])
                else:
                    robot = ozo.find()   

                if robot is False:
                    ret = "None"
                else:
                    devices = ozo.getrobots()
                    log(robot)
                    log("Detected MAC&Names : {}".format(devices))
                    log("Selected MAC and Name : {}".format(robot))
                    bot1 = ozolib.Command(robot)
                    if bot1.bconnect() is False:
                        del bot1
                        ret = False
                    else:
                        ret = True

        elif com[0]=='maru_odisconnect':
            log("Disconnect 1")
            if 'bot1' in locals():  #연결된 로봇이 있는 경우만 disconnect
                log("Disconnect 2")                
                if bot1.isconnected() is True:
                    ret = bot1.bdisconnect()
                    log("bot1.disconnected")
                    del bot1
                else:
                    log("Disconnect 3")                     
                    del bot1
                    ret = True
            else:
                log("Disconnect 4") 
                ret = True

        elif com[0]=='maru_oisconnected':
            if 'bot1' not in locals():
                ret = False
            elif param_cnt==1:
                ret = bot1.bisconnected()
            else:
                ret =  "Incorrect Parameters"  

        elif com[0]=='maru_ostop':
            if 'bot1' not in locals():
                ret = False
            elif param_cnt==1:
                ret = bot1.bstop()
            else:
                ret =  "Incorrect Parameters" 

        elif com[0]=='maru_oreadcolor':
            if 'bot1' not in locals():
                ret = False
            elif param_cnt==1:
                ret = bot1.breadcolor()
            else:
                ret =  "Incorrect Parameters" 

        elif com[0]=='maru_oobstacle':
            ref=40 #about 3cm,  150:about 2cm
            if 'bot1' not in locals():
                ret = False
            elif param_cnt==1:
                ret = bot1.bobstacle(0,ref)                
            elif param_cnt==2:
                ret = bot1.bobstacle(int(com[1]),ref)
            else:
                ret =  "Incorrect Parameters"                 

        elif com[0]=='maru_ostop':
            if 'bot1' not in locals():
                ret = False
            elif param_cnt==1:
                ret = bot1.bstop()
            else:
                ret =  "Incorrect Parameters" 

        elif com[0]=='maru_omove1':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==5:                           
                ret = bot1.bmove1(int(com[1]),int(com[2]),int(com[3]),int(com[4]))                              
            else:
                ret =  "Incorrect Parameters"    

        elif com[0]=='maru_omove2':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==4:                           
                ret = bot1.bmove2(int(com[1]),int(com[2]),int(com[3]))                              
            else:
                ret =  "Incorrect Parameters"                      

        elif com[0]=='maru_omove3':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==2:                           
                ret = bot1.bmove3(int(com[1]))  
            elif param_cnt==3:                           
                ret = bot1.bmove3(int(com[1]),int(com[2]))                              
            else:
                ret =  "Incorrect Parameters"   

        elif com[0]=='maru_orotate1':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==3:                           
                ret = bot1.brotate1(int(com[1]),int(com[2]))                              
            else:
                ret =  "Incorrect Parameters"  

        elif com[0]=='maru_orotate2':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==3:                           
                ret = bot1.brotate2(int(com[1]),int(com[2]))                              
            else:
                ret =  "Incorrect Parameters"  

        elif com[0]=='maru_oturnoff':
            if 'bot1' not in locals():
                ret = False
            elif param_cnt==1:
                ret = bot1.bturnoff()
            else:
                ret =  "Incorrect Parameters" 
                                                
        elif com[0]=='maru_otopled1':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==4:                           
                ret = bot1.btopled1(int(com[1]),int(com[2]),int(com[3]))                              
            else:
                ret =  "Incorrect Parameters"        

        elif com[0]=='maru_otopled2':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==1:                           
                ret = bot1.btopled2()                              
            else:
                ret =  "Incorrect Parameters"   

        elif com[0]=='maru_otopled3':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==1:                           
                ret = bot1.btopled3()                              
            else:
                ret =  "Incorrect Parameters"

        elif com[0]=='maru_otopledoff':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==1:                           
                ret = bot1.btopledoff()                              
            else:
                ret =  "Incorrect Parameters"

        elif com[0]=='maru_ofrontled1':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==5:                           
                ret = bot1.bfrontled1(int(com[1]),int(com[2]),int(com[3]),int(com[4]))                              
            else:
                ret =  "Incorrect Parameters"        

        elif com[0]=='maru_ofrontled2':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==1:                           
                ret = bot1.bfrontled2()                              
            else:
                ret =  "Incorrect Parameters"   

        elif com[0]=='maru_ofrontledoff':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==1:                           
                ret = bot1.bfrontledoff()                              
            else:
                ret =  "Incorrect Parameters"  

        elif com[0]=='maru_oemotion':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==2:                           
                ret = bot1.bemotion(str(com[1]))                              
            else:
                ret =  "Incorrect Parameters"     

        elif com[0]=='maru_odirection':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==2:                           
                ret = bot1.bdirection(str(com[1]))                              
            else:
                ret =  "Incorrect Parameters"     

        elif com[0]=='maru_onumber':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==2:                           
                ret = bot1.bnumber(str(com[1]))                              
            else:
                ret =  "Incorrect Parameters"                                                             

        elif com[0]=='maru_ocolor':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==2:                           
                ret = bot1.bcolor(str(com[1]))                              
            else:
                ret =  "Incorrect Parameters" 

        elif com[0]=='maru_ogentone1':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==3:                           
                ret = bot1.bgentone1(int(com[1]),str(com[2]))                              
            else:
                ret =  "Incorrect Parameters"    

        elif com[0]=='maru_ogentone2':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==4:                           
                ret = bot1.bgentone2(int(com[1]),str(com[2]),float(com[3]))                              
            else:
                ret =  "Incorrect Parameters"  

        elif com[0]=='maru_ostopsound':
            if 'bot1' not in locals():
                ret = False
            elif param_cnt==1:
                ret = bot1.bstopsound()
            else:
                ret =  "Incorrect Parameters"                                             

        elif com[0]=='maru_orestnote':
            if 'bot1' not in locals():
                ret = False
            elif param_cnt==1:
                ret = bot1.brestnote()                
            elif param_cnt==2:
                ret = bot1.brestnote(float(com[1]))
            else:
                ret =  "Incorrect Parameters"  

        elif com[0]=='maru_odance':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==1:                           
                ret = bot1.bdance()                  
            else:
                ret =  "Incorrect Parameters"     

        elif com[0]=='maru_orainbow':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==1:                           
                ret = bot1.brainbow()                  
            else:
                ret =  "Incorrect Parameters"   

        elif com[0]=='maru_oflashrainbow':
            if 'bot1' not in locals():
                ret = "Not Connected"  
            elif param_cnt==1:                           
                ret = bot1.bflashrainbow()                  
            elif param_cnt==2:                           
                 ret = bot1.bflashrainbow(int(com[1]))                  
            else:
                ret =  "Incorrect Parameters"  

        elif com[0]=='maru_ozigzag':
            if 'bot1' not in locals():
                ret = "Not Connected"                  
            elif param_cnt==3:                           
                ret = bot1.bzigzag(int(com[1]),int(com[2])) 
            elif param_cnt==4:
                ret = bot1.bzigzag(int(com[1]),int(com[2]),int(com[3]))                  
            else:
                ret =  "Incorrect Parameters"  


        elif com[0]=='maru_oversion':
            if param_cnt==1:                           
                ret = ozolib.version()  
            else:
                ret =  "Incorrect Parameters"                                          

        elif com[0]=='maru_oquit' or  com[0]=='quit':
            if 'bot1' in locals():
                if bot1.isconnected() is True:
                    ret = bot1.disconnect()
                else:
                    ret = True
            else:
                ret = True
            log("Quit {}".format(ret))
        else:
            ret="Unknown command"

        log("Return:{}".format(ret))            
        client_socket.send(str(ret).encode())

    if data =='quit' or data=='maru_oquit':       
        break
    
client_socket.close()    
server_socket.close()
log("server closed")
exit(0)
