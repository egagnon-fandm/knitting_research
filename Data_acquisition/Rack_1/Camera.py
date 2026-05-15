import logging
import os
import subprocess
import sys
import gphoto2 as gp

class Camera:
    def __init__(self, save_folder = '/home/etienne/Documents/Knitted_Fabric/Pictures'):
        self.camera = gp.Camera()
        self.camera.init()
        self.save_folder = save_folder

    def capture_image(self, file_suffix, ref_number):
        file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
        target = os.path.join(self.save_folder, 'scan_'+ file_suffix + '_F_' + str(ref_number)+'.jpg')
        camera_file = self.camera.file_get(
            file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
        camera_file.save(target)
        return 0

    def close(self):
        self.camera.exit
        return 0