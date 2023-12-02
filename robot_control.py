from DexArm_API.pydexarm.pydexarm import Dexarm

dexarm = Dexarm(port="/dev/tty.usbmodem308B335D34381")

try:
    print('Go Home')
    dexarm.go_home()
    print('Move to cheese')
    dexarm.move_to(300, 0, 0)
    # print('Pick up cheese')
    # dexarm.air_picker_pick()
    # print('Move to destination')
    # dexarm.move_to(300, 0, 40)
    # dexarm.move_to(250, 100, 40)
    # dexarm.move_to(250, 100, 0)
    # print('Let go')
    # dexarm.air_picker_place()

    # print('Go Home')
    # dexarm.go_home()

finally:
    print('Stop Pump')
    dexarm.air_picker_stop()
    print('Close')
    dexarm.close()
