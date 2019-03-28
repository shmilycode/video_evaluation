import numpy as np
import cv2
from skimage.measure import compare_ssim
from skimage.measure import compare_psnr 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
import argparse

threshold = 400
frame_seq = 20
 
class UpdateDist(object):
    def __init__(self, ax, source_cap, target_cap, skips, type):
        self.ax = ax
        self.lines = []
        color_set = ['r-', 'g-', 'b-', 'c-', 'm-', 'y-']
        for skip_step in skips:
            new_line, = ax.plot([],[],color_set[skip_step%6], marker='.')
            self.lines.append(new_line)

        self.frame_array = []
        self.result_arrays= [] 
        self.line_points=[]
        self.min_line_index = 0
        self.source_caps = []
        self.target_cap = cv2.VideoCapture(target_cap)
        self.type=type
        self.source_skip=source_skip
        self.threshold = threshold
        self.line_count = len(self.lines)
        print(self.threshold)

        for line_num in range(self.line_count):
            new_source = cv2.VideoCapture(source_cap)
            for skip in range(skips[line_num]):
                new_source.read()
            self.source_caps.append(new_source)
            self.result_arrays.append([])
            self.line_points.append({"frames":[], "results":[]})

    def __del__(self):
        for line_num in range(self.line_count):
            self.source_caps[line_num].release()
        self.target_cap.release()

    def __call__(self, frame):
        self.frame_array.append(frame)

        if frame % frame_seq == 0:
            result_means = [np.mean(result[frame-frame_seq:frame]) for result in self.result_arrays]
            max_mean_result_index = result_means[self.min_line_index:].index(
                max(result_means[self.min_line_index:])) + self.min_line_index;
            self.min_line_index = max_mean_result_index
            print("max_mean_result=%d, frame=%d" % (max_mean_result_index, frame))
            self.line_points[max_mean_result_index]["frames"].extend(
                self.frame_array[frame-frame_seq:frame]);

            self.line_points[max_mean_result_index]["results"].extend(
                self.result_arrays[max_mean_result_index][frame-frame_seq:frame])

            self.lines[max_mean_result_index].set_data(
                self.line_points[max_mean_result_index]["frames"],
                self.line_points[max_mean_result_index]["results"])

#        for line_num in range(self.line_count):
#            self.lines[line_num].set_data(self.frame_array, self.result_arrays[line_num])

        return tuple(self.lines,)

    def init(self):
        for line in self.lines:
            line.set_data([],[])
        return self.lines

    def gen_ssim(self):
        frame_index=0
        while (frame_index < self.threshold):
            target_ret,target_frame = self.target_cap.read()
            for line_num in range(self.line_count):
                source_cap = self.source_caps[line_num]
                source_ret,source_frame = source_cap.read()
                if source_ret and target_ret:
                    result = 0
                    if self.type == "ssim":
                        result=compare_ssim(cv2.cvtColor(source_frame, cv2.COLOR_BGR2GRAY),
                            cv2.cvtColor(target_frame, cv2.COLOR_BGR2GRAY));
                    elif self.type == "psnr":
                        result=compare_psnr(source_frame,target_frame);
                    self.result_arrays[line_num].append(result)
                else:
                    print("error read!")
                    return
            yield frame_index
            frame_index += 1

        return

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description = 'manual to this script')
    parse.add_argument('--validation_source', type=str, default=None, help="validation source")
    parse.add_argument('--test_target', type=str, default=None, help="test source")
    parse.add_argument('--skip', type=str, default=None, help="step to skip")
    parse.add_argument('--method', type=str, default=None, help="compare method, ssim or psnr")
    parse.add_argument('--threshold', type=int, default=0, help="max frame size to compare")
    argv = parse.parse_args()

    source_cap = argv.validation_source #'./test_video/dump.h264'
    target_cap = argv.test_target #'./test_video/live.h264'
    source_skip = argv.skip
    skip_set = source_skip.split(',')
    skip_set = [int(i) for i in skip_set]
    if len(skip_set) == 1:
        skip_set = [i for i in range(skip_set[0])]
    threshold = argv.threshold
    method = argv.method

    fig,ax2 = plt.subplots()
    ax2.set_title(method)
    ax2.set_xlim(0,threshold)

    if method == "ssim":
        ax2.set_ylim(0,1.0)
    elif method == "psnr":
        ax2.set_ylim(0,50)
    ax2.grid(True)

    print(source_cap+target_cap+str(skip_set)+method+str(threshold))
    ud2 = UpdateDist(ax2, source_cap, target_cap, skip_set, method)
    ani2 = FuncAnimation(fig, ud2, frames=ud2.gen_ssim, interval=30, 
                         blit=True, init_func=ud2.init, repeat=False)


    plt.show();
