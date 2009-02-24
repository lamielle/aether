from aether.core import AetherDriver

def run():
  """ Convenience function that runs the Peepers Module with camera enabled """
  from aether.modules import PeepersModule
  driver = AetherDriver(640)
  driver.register_module(PeepersModule(driver))
  driver.run()

def run_debug():
  """ Convenience function that runs the Peepers Module in debug mode """
  from aether.modules import BoidsModule,PeepersModule, ParticleModule
  driver = AetherDriver(640,debug=True)
  driver.register_module(PeepersModule(driver))
  #driver.register_module(BoidsModule(driver))
  #driver.register_module(ParticleModule(driver))
  driver.run()
