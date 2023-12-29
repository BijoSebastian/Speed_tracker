from kld7 import KLD7
from kld7 import RadarParamProxy

tmpvar = 1
detectionCount = 0
with KLD7("/dev/serial0") as radar:
    tmpvar = 1
    file1 = open("MyFile1.txt","w")
    for target_info in radar.stream_TDAT():
       # print(type(target_info))

        if target_info != None:
            if tmpvar == 1:
                print("Detection number: " + str(detectionCount))
                detectionCount += 1
                file1.write("Detection number: " + str(detectionCount) + "\n")
            if tmpvar > 0:
                tmpvar += 1
            if tmpvar >= 1 and tmpvar <= 5:               #capture 4 readings after a new detection
                print(target_info.distance)
                file1.write("distance: " + str(target_info.distance) + "      speed: " + str(target_info.speed) + "          angle: " + str(target_info.angle) + "           magnitude:  " + str(target_info.magnitude) + "\n")
        else:
            tmpvar=1
    file1.close()
