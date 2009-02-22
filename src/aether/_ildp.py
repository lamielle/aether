from ildp.core import ILDDriver

def run():
  """ Convenience function that runs the Peepers Module with camera enabled """
  from ildp.modules import PeepersModule
  driver = ILDDriver(640)
  driver.register_module(PeepersModule(driver))
  driver.run()

def run_debug():
  """ Convenience function that runs the Peepers Module in debug mode """
  from ildp.modules import BoidsModule,PeepersModule, ParticleModule
  driver = ILDDriver(640,debug=True)
  driver.register_module(PeepersModule(driver))
  #driver.register_module(BoidsModule(driver))
  #driver.register_module(ParticleModule(driver))
  driver.run()
