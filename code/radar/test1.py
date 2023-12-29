from kld7 import KLD7
from kld7 import RadarParamProxy

tmpvar = 1
with KLD7("/dev/serial0") as radar:
    tmpvar = 1
    for target_info in radar.stream_TDAT():
        #print("loop")

        if target_info != None:
            print("new target")
            if tmpvar > 0:
                tmpvar += 1
            if tmpvar >= 1 and tmpvar <= 5:               #capture 4 readings after a new detection
                print(target_info)
        else:
            tmpvar = 1

        #print("also")
        #tmp1, tmp2 =_read_packet(radar)
        #print(tmp2)
        #print(radar._param_proxy.THOF)
        #print(radar._param_dict['RSPI'])
        
        radar.set_param('MISP', 10)
       	
        #radar.set_param('MASP',80)
        #print(radar.read_RFFT())
