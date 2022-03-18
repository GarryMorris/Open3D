# ----------------------------------------------------------------------------
# -                        Open3D: www.open3d.org                            -
# ----------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2018-2021 www.open3d.org
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
# ----------------------------------------------------------------------------

import os
from multiprocessing import Process
import subprocess as sp
from time import sleep
import pytest


def draw_box():
    import open3d as o3d
    cube_red = o3d.geometry.TriangleMesh.create_box(1, 2, 4)
    cube_red.compute_vertex_normals()
    cube_red.paint_uniform_color((1.0, 0.0, 0.0))
    o3d.visualization.draw(cube_red, non_blocking_and_return_uid=True)
    # Actual rendering
    o3d.visualization.gui.Application.instance.run_one_tick()
    o3d.visualization.gui.Application.instance.quit()


def test_draw_cpu():
    """Test CPU rendering in a separate process."""
    os.environ['OPEN3D_CPU_RENDERING'] = 'true'
    proc = Process(target=draw_box)
    proc.start()
    proc.join(timeout=3)  # Wait for process to complete
    if proc.exitcode is None:
        proc.terminate()  # Kill on failure
        assert False, __name__ + " did not complete."
    assert proc.exitcode == 0