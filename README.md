# video_evaluation
Examples of video evaluation.

## video_eval.py

#### parameters
1. validation_source: The path of validation video, usually use the Lossless-video or original video
2. test_target: The path of test video, usually use the compressed video or damaged video.

#### Result
The graphic of SSIM and PSNR line


## video_eval_with_step.py

#### parameters

1. validation_source: The path of validation video, usually use the Lossless-video or original video
2. test_target: The path of test video, usually use the compressed video or damaged video.
3. skip: How man frame may be throw
4. method: ssim or psnr
5. threshold: max frame of video

#### Result
The graphic of PSNR or SSIM line, the change of color means frame thrown.