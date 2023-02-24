import time
# __version__ = "v1.0.0.20230105"
__version__ = str(time.strftime("v1.0.0.%Y%m%d", time.localtime()))


print(__version__)