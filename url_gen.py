import pyqrcode
import png
import numpy as np
import sys

# arguments
url = str(sys.argv[1]).strip()
scale = sys.argv[2]
name = str(sys.argv[3]).strip()
format = str(sys.argv[4]).strip()

def qrToArray(encodedQr):
    arr = encodedQr.text().split('\n')
    arr.pop()
    return np.vstack(arr)

if url:
    encodedURL = pyqrcode.create(url)
    
    # create qr graphic
    if format.upper() == "SVG":
        encodedURL.svg(f'qrs/{name}.svg', scale=scale)
        print(encodedURL.terminal(quiet_zone=4))
    elif format.upper() == "PNG":
        encodedURL.png(f'qrs/{name}.png', scale=scale)
        print(encodedURL.terminal(quiet_zone=4))
    else:
        print(f'failed to create qr graphic due to invalid format ({format.upper()}) - only supports SVG & PNG')

    qrArray = qrToArray(encodedURL)
    #print(qrArray)

    # write array out to file on C:/
    file = open(f'C:/qrs/{name}.array', 'w')
    for row in qrArray:
        file.write(str(row))
    file.close()    
else:
    print('invalid url: {url}')