import numpy as np
import cv2
from skimage.measure import compare_ssim
from skimage.measure import compare_psnr
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
 
class UpdateDist(object):
    def __init__(self, line, source_cap, target_cap, type):
        self.frame_array = []
        self.result_array= []
        self.source_cap=cv2.VideoCapture(source_cap)
        self.target_cap=cv2.VideoCapture(target_cap)
        self.line=line
        self.type=type
        self.threshold=400

    def __del__(self):
        self.source_cap.release()
        self.target_cap.release()

    def __call__(self, frame):
        self.frame_array.append(frame)
        self.line.set_data(self.frame_array, self.result_array)
        return self.line,

    def init(self):
        self.line.set_data([],[])
        return self.line,

    def gen_ssim(self):
        frame_index=0
        while (self.source_cap.isOpened() and
            self.target_cap.isOpened() and
            frame_index < self.threshold):
            source_ret,source_frame=self.source_cap.read()
            target_ret,target_frame=self.target_cap.read()
        
            if source_ret and target_ret:
                result = 0
                if self.type is "ssim":
                    result=compare_ssim(cv2.cvtColor(source_frame, cv2.COLOR_BGR2GRAY),
                        cv2.cvtColor(target_frame, cv2.COLOR_BGR2GRAY));
                elif self.type is "psnr":
                    result=compare_psnr(source_frame,target_frame);
                self.result_array.append(result)
                yield frame_index
                frame_index += 1
            else:
                break
        return

if __name__ == "__main__":
    fig = plt.figure()
    ax1 = fig.add_subplot(221)
    line1, = ax1.plot([],[],'r-')
    ax1.set_xlim(0,400)
    ax1.set_ylim(0,1)
    ax1.grid(True)
    ax1.axvline(0.5, linestyle='--',color='black')
    
    ax2 = fig.add_subplot(222)
    line2, = ax2.plot([],[],'r-')
    ax2.set_xlim(0,400)
    ax2.set_ylim(0,50)
    ax2.grid(True)
    ax2.axvline(0.5, linestyle='--',color='black')
    
    source_cap = './test_video/dump.h264'
    target_cap = './test_video/live.h264'
#    source_cap = './test_video/live.h264'
#    target_cap = './test_video/live.h264'
    ud1 = UpdateDist(line1, source_cap, target_cap, "ssim")
    ani1 = FuncAnimation(fig, ud1, frames=ud1.gen_ssim, interval=30, 
                         blit=True, init_func=ud1.init, repeat=False)
    ud2 = UpdateDist(line2, source_cap, target_cap, "psnr")
    ani2 = FuncAnimation(fig, ud2, frames=ud2.gen_ssim, interval=30, 
                         blit=True, init_func=ud2.init, repeat=False)
    
    plt.show();
