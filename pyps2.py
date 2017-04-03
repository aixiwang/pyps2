#---------------------------------------------------------------------------------------------
# pyps2
# BSD license is applied to this code
#
# Copyright by Aixi Wang (aixi.wang@hotmail.com)
#
#---------------------------------------------------------------------------------------------
import serial
import sys,time



#-------------------------
# encode_ps2_key_pkg
#------------------------- 
def encode_ps2_key_pkg(make_break_flag,key_data):
    # make_break_flag 0: make, 1: break
    if make_break_flag == 1:
        s1 = '\xeb\x90\x02\x00\x00'
    else:
        s1 = '\xeb\x90\x01\x00\x00'
    d5 = 0
    for d in key_data:
        d5 += ord(d)
    d5 = (d5) % 256
    s1 += key_data + chr(d5)
    print 's1:', s1.encode('hex'), len(s1)
    return s1
    
#-------------------------
# encode_ps2_mouse_pkg
#------------------------- 
def encode_ps2_mouse_pkg(left_btn,right_btn,move_x,move_y):
   
    s1 = '\xeb\x90\x04\x01\x00'
    d1 = 8
    if left_btn == 1:
        d1 += 1
    if right_btn == 1:
        d1 += 2
    if move_x < 0:
        d1 += 16
        
    if move_y < 0:
        d1 += 32

    if move_x < 0:
        d2 = 256 + move_x
    else:
        d2 = move_x
        
    if move_y < 0:
        d3 = 256 + move_y
    else:
        d3 = move_y

    d4 = 0
    
    d5 = (d1 + d2 + d3 + d4) % 256
    s1 += chr(d1) + chr(d2) + chr(d3) + chr(d4) + chr(d5)
    
    print 's1:', s1.encode('hex'), len(s1)
    return s1
    

    
#-------------------------
# main
#-------------------------
if __name__ == '__main__':

    #try:
    if 1:
        serialport_path = sys.argv[1]
        print 'COM port:', serialport_path
        s = serial.Serial(serialport_path,9600,parity=serial.PARITY_NONE,timeout=0.1)
        #print s
        time.sleep(5)
        print 'start to run'
        d = 20
        while d > 0:
            # send char '9' make
            s1 = encode_ps2_key_pkg(0,'\x46')
            s.write(s1)
            # send char '9' break
            s1 = encode_ps2_key_pkg(1,'\xf0\x46')
            s.write(s1)
            time.sleep(1)
            
            # move mouse
            s1 = encode_ps2_mouse_pkg(0,0,-50,50)
            s.write(s1)
            time.sleep(1)
            d -= 1
            
    #except:
        #print 'init serial error!'
        #sys.exit(-1)
        
    
