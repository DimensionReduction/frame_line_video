import os
import sys
import cv2
import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageFilter, ImageOps

def video_to_frame(video):#视频转图片帧
    path=Image.open(video)
    if path is None:
        print('没有找到该文件，程序结束！')
        sys.exit()
    if os.path.exists('./帧/')==False:
        os.mkdir('./帧/')
    cap=cv2.VideoCapture(video)
    k=0
    while True:
        if cap.grab():
            k+=1
            flag,frame=cap.retrieve()
            if flag:
                new=f'./帧/{k}.jpg'
                print(f'正在生成图片帧：{k}.jpg')
                cv2.imencode('.jpg', frame)[1].tofile(new)
        else:
            break

def frame_to_line():#图片帧转线稿
    img_array=os.listdir('./帧/')
    if os.path.exists('./线稿')==False:
        os.mkdir('./线稿')
    for k in range(1,len(img_array)+1):
        img=Image.open(f'./帧/{k}.jpg')
        img1=img.convert('L')
        img2=img1.copy()
        img2=ImageOps.invert(img2)
        for i in range(25):
            img2=img2.filter(ImageFilter.BLUR)
        width,height=img1.size
        for x in range(width):
            for y in range(height):
                a=img1.getpixel((x,y))
                b=img2.getpixel((x,y))
                img1.putpixel((x,y),min(int(a*255/(256-b*1)),255))
        img1.save(f'./线稿/{k}.jpg')
        print(f'正在转换为线稿：{k}.jpg')

def line_to_video():#线稿合并为视频
    img_array=os.listdir('./线稿/')
    img_array.sort(key=lambda x:int(x[:-4]))
    pic=Image.open('./线稿/'+img_array[0])
    video=cv2.VideoWriter('线稿视频.mp4',cv2.VideoWriter_fourcc('m','p','4','v'),20, (pic.size[0],pic.size[1]))
    for i in range(1,len(img_array)+1):
        img=imageio.imread('./线稿/'+img_array[i-1])
        img2=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        video.write(img2)
    video.release()
    print('线稿视频.mp4已生成！')

if __name__=='__main__':
    video=input('请输入视频文件路径(如：一人之下.mp4)：')
    video_to_frame(video)
    frame_to_line()
    line_to_video()


