import esptool
import sys

if __name__ == "__main__":
    command = "esptool write_flash"
    sys.argv = command.split()
    esptool.main()
