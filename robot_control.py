from DexArm_API.pydexarm.pydexarm import Dexarm

dexarm = Dexarm(port="/dev/tty.usbmodem308B335D34381")

dexarm.go_home()
