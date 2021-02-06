from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import os

def scan_code():
    '''
    Scans QR code from the consumer to read all data containing items and their expiry dates
    '''
    if os.path.exists("barcode.csv"):
        os.remove("barcode.csv")

    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
        help="path to output CSV file containing barcodes")
    args = vars(ap.parse_args())

    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()

    time.sleep(2.0)
    csv = open(args["output"], "w")
    found = set()

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width = 1080)
        barcodes = pyzbar.decode(frame)
        
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            if barcodeData not in found:
                csv.write("{}\n".format(barcodeData))
                csv.flush()
                found.add(barcodeData)
                
        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(15) & 0xFF

        # if len(found) > 0:
        #     break
        if key == ord("q"):
            break
        
    print("[INFO] cleaning up...")
    csv.close()
    cv2.destroyAllWindows()
    vs.stop()