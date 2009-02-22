import ildp.core.input
from ildp.core.input import Settings
from pygame import mouse
from math import cos,sin,pi
import os

class InputProvider(object):

  # used for debug mode
  CIRCLE, PERSON, POLY = range(3)

  def __init__(self,dims,settings_file_name,debug=False):
    if debug:
      InputProvider.com=self.get_com_debug
      InputProvider.verts=self.get_verts_debug
      InputProvider.polys=self.get_polys_debug
      InputProvider.calibrate=self.calibrate_debug
      self.sim_shadow_shape = InputProvider.CIRCLE
    else:
      InputProvider.com=self.get_com
      InputProvider.verts=self.get_verts
      InputProvider.polys=self.get_polys
      InputProvider.calibrate=self.calibrate

    self.dims = dims
    self.settings_file_name=settings_file_name
    self.settings=Settings()
    if os.path.isfile(self.settings_file_name):
      self.settings.load(self.settings_file_name)
    if not debug: self.calibrate()

  #Camera input methods
  def get_com(self):
    p = ildp.core.input.get_com()
    return int((p[0]/100.)*self.dims[0]), int((p[1]/100.)*self.dims[1])

  def get_verts(self):
    verts = ildp.core.input.get_verts()
    if len(verts) != 0 :
      for i,p in enumerate(verts) :
        verts[i] = int((p[0]/100.)*self.dims[0]), int((p[1]/100.)*self.dims[1])
    return verts

  def get_polys(self):
    polys = ildp.core.input.get_polys()
    for poly in polys :
      if len(poly) != 0 :
        for i,p in enumerate(poly) :
          poly[i] = int((p[0]/100.)*self.dims[0]), int((p[1]/100.)*self.dims[1])
    return polys

  def get_lp_pts(self):
    return ildp.core.input.get_lp_pts()

  def calibrate(self):
    ildp.core.input.calibrate(self.settings)
    self.settings.save(self.settings_file_name)

  #Debug input methods
  def get_com_debug(self): return mouse.get_pos()

  def get_verts_debug(self):
    if self.sim_shadow_shape == InputProvider.PERSON :
      pts = [(.4,1),(.4,.65),(.25,.4),(.25,.3),(.35,.2),(.35,.25),(.3,.35),(.45,.55),(.45,.5),(.4,.4),(.4,.3),(.45,.25),(.5,.25),(.55,.3),(.55,.4),(.5,.5),(.55,.5),(.6,.55),(.7,.55),(.75,.5),(.75,.4),(.8,.4),(.8,.55),(.7,.6),(.55,.6),(.55,1)]
      pos = mouse.get_pos()
      pts = [(p[0]*self.dims[0]-(self.dims[0]/2)+pos[0],p[1]*self.dims[1]-(self.dims[1]/2)+pos[1]) for p in pts]
    elif self.sim_shadow_shape == InputProvider.POLY :
      pts = [(0.3, 0.7), (0.35, 0.6), (0.2, 0.45), (0.3, 0.25), (0.5, 0.35), (0.75, 0.15), (0.7, 0.35), (1.0, 0.4), (0.6, 0.5), (0.65, 0.6), (0.75, 0.65), (0.6, 0.7), (0.5, 0.65)]
      scale = 0.7
      pos = mouse.get_pos()
      pts = [((p[0]*self.dims[0]-(self.dims[0]/2))*scale+pos[0],(p[1]*self.dims[1]-(self.dims[1]/2))*scale+pos[1]) for p in pts]
    else :
      pts = [(mouse.get_pos()[0]+(sin(theta*(2*pi/360))*15.),mouse.get_pos()[1]+(cos(theta*(2*pi/360))*15.)) for theta in range(0,360,360/10) ]
    return pts

  def get_polys_debug(self): return (((6,7),(10,20),(5,100)),)
  def get_lp_pts_debug(self): return ((6,7),)
  def calibrate_debug(self): return None#raise NotImplementedError('Calibration is not supported in debug mode')
