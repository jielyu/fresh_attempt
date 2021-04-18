import numpy as np
import mayavi.mlab as mlab
import  moviepy.editor as mpy

duration= 2 # duration of the animation in seconds (it will loop)

# 用Mayavi制作一个图形

fig_myv = mlab.figure(size=(220,220), bgcolor=(1,1,1))
X, Y = np.linspace(-2,2,200), np.linspace(-2,2,200)
XX, YY = np.meshgrid(X,Y)
ZZ = lambda d: np.sinc(XX**2+YY**2)+np.sin(XX+d)

# 用MoviePy将图形转换为动画，编写动画GIF

def make_frame(t):
    mlab.clf() # 清掉图形（重设颜色）
    mlab.mesh(YY,XX,ZZ(2*np.pi*t/duration), figure=fig_myv)
    return mlab.screenshot(antialiased=True)

animation = mpy.VideoClip(make_frame, duration=duration)
animation.write_gif("sinc.gif", fps=20)