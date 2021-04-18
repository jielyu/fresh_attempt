# -*- coding: utf-8 -*-
# vispy: gallery 30
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
# Author: Nicolas P .Rougier
# Date:   06/03/2014
# Abstract: Fake electrons orbiting
# Keywords: Sprites, atom, particles
#
# Modified by Zulko for animation with MoviePy
# See result here : http://i.imgur.com/6PNEYB9.gif 250 %}
# -----------------------------------------------------------------------------

import numpy as np
from vispy import gloo
from vispy import app
from vispy.util.transforms import perspective, translate, rotate
from vispy.gloo.util import _screenshot

# Create vertices
n, p = 100, 150
data = np.zeros(p * n, [('a_position', np.float32, 2),
                        ('a_color',    np.float32, 4),
                        ('a_rotation', np.float32, 4)])
trail = .5 * np.pi
data['a_position'][:, 0] = np.resize(np.linspace(0, trail, n), p * n)
data['a_position'][:, 0] += np.repeat(np.random.uniform(0, 2 * np.pi, p), n)
data['a_position'][:, 1] = np.repeat(np.linspace(0, 2 * np.pi, p), n)

data['a_color'] = 1, 1, 1, 1
data['a_color'] = np.repeat(
    np.random.uniform(0.75, 1.00, (p, 4)).astype(np.float32), n, axis=0)
data['a_color'][:, 3] = np.resize(np.linspace(0, 1, n), p * n)

data['a_rotation'] = np.repeat(
    np.random.uniform(0, 2 * np.pi, (p, 4)).astype(np.float32), n, axis=0)


vert = """
#version 120
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform float u_size;
uniform float u_clock;
attribute vec2 a_position;
attribute vec4 a_color;
attribute vec4 a_rotation;
varying vec4 v_color;
mat4 build_rotation(vec3 axis, float angle)
{
    axis = normalize(axis);
    float s = sin(angle);
    float c = cos(angle);
    float oc = 1.0 - c;
    return mat4(oc * axis.x * axis.x + c,
                oc * axis.x * axis.y - axis.z * s,
                oc * axis.z * axis.x + axis.y * s,
                0.0,
                oc * axis.x * axis.y + axis.z * s,
                oc * axis.y * axis.y + c,
                oc * axis.y * axis.z - axis.x * s,
                0.0,
                oc * axis.z * axis.x - axis.y * s,
                oc * axis.y * axis.z + axis.x * s,
                oc * axis.z * axis.z + c,
                0.0,
                0.0, 0.0, 0.0, 1.0);
}
void main (void) {
    v_color = a_color;
    float x0 = 1.5;
    float z0 = 0.0;
    float theta = a_position.x + u_clock;
    float x1 = x0*cos(theta) + z0*sin(theta);
    float y1 = 0.0;
    float z1 = (z0*cos(theta) - x0*sin(theta))/2.0;
    mat4 R = build_rotation(a_rotation.xyz, a_rotation.w);
    gl_Position = u_projection * u_view * u_model * R * vec4(x1,y1,z1,1);
    gl_PointSize = 8.0 * u_size * sqrt(v_color.a);
}
"""

frag = """
#version 120
varying vec4 v_color;
varying float v_size;
void main()
{
    float d = 2*(length(gl_PointCoord.xy - vec2(0.5,0.5)));
    gl_FragColor = vec4(v_color.rgb, v_color.a*(1-d));
}
"""

class Canvas(app.Canvas):

    def __init__(self):
        app.Canvas.__init__(self, keys='interactive')
        self.size = 800, 800

        self.program = gloo.Program(vert, frag)
        self.view = np.eye(4, dtype=np.float32)
        self.model = np.eye(4, dtype=np.float32)
        self.projection = np.eye(4, dtype=np.float32)
        self.translate = 4.5
        #translate(self.view, 0, 0, -self.translate)
        self.view = translate([0, 0, -self.translate])

        self.program.bind(gloo.VertexBuffer(data))
        self.program['u_model'] = self.model
        self.program['u_view'] = self.view
        self.program['u_size'] = 5 / self.translate

        gloo.set_state('translucent', depth_test=False)
        self.program['u_clock'] = 0.0

    def on_resize(self, event):
        width, height = event.size
        gloo.set_viewport(0, 0, width, height)
        self.projection = perspective(45.0, width / float(height), 1.0, 1000.0)
        self.program['u_projection'] = self.projection

    def animation(self, t):
        """ Added for animation with MoviePy """
        self.program['u_clock'] = 2*t
        gloo.clear('red')
        self.program.draw('points')
        return  _screenshot((0, 0, self.size[0], self.size[1]))[:,:,:3]



if __name__ == '__main__':

    from moviepy.editor import VideoClip
    canvas = Canvas()
    canvas.show()
    clip = VideoClip(canvas.animation, duration=np.pi).resize(0.3)
    clip.write_videofile('atom3.mp4', fps=20)
    #clip.write_gif('atom3.gif', fps=20, opt='OptimizePlus')