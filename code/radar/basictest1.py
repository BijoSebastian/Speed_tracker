from kld7 import KLD7
with KLD7("/dev/serial0") as radar:
    radar.set_param('RSPI', 2)
    radar.set_param('RRAI', 3)
    #radar.set_param('MISP', 16)
    for target_info in radar.stream_TDAT():
        print(target_info)
