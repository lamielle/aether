Tutorial 3 -- :class:`~aether.core.FaceInputProvider` example
=============================================================

In this tutorial we will walk through how write a module that uses the :class:`~aether.core.FaceInputProvider` class.  The :class:`~aether.core.FaceInputProvider` class uses `OpenCV's <http://opencv.willowgarage.com/wiki/>`_ Haar Cascade Classification to detect faces in the camera's captured image which means this mode of input is probably best paired with a camera facing directly back at you.  The code is exceedingly simple, so let's dive in.

Now, I love tiki masks as much as the next guy.  So, I asked myself the obvious question: what better way to get my idol on than with a module that puts a tiki mask on you when you're sitting in front of your computer?  I set to work, starting with creating a file ``TikiModule.py`` and some import statements::

   from aether.core import AetherDriver, FaceInputProvider, AetherModule

   import pygame.image
   from pygame.color import THECOLORS
   import pygame.transform

Nice and boring.  Immediately after came the module definition, extending :class:`~aether.core.AetherModule`::

   class TikiModule(AetherModule) :

      def __init__(self,*args) :
         # need to call parent class' init method explicitly in python
         AetherModule.__init__(self,*args)

         # load our image, this will look in the directory where the file is executed
         self.tiki = pygame.image.load("tiki.png")

         # make any white in the image transparent
         self.tiki.set_colorkey(THECOLORS["white"])

The comments are pretty self explanatory.  The :meth:`AetherModule.__init__(self,\*args) <aether.core.AetherModule__init__>` is the first thing any subclassed :class:`~aether.core.AetherModule` should call because it sets up vital class members needed to do anything interesting.  Second, the pygame.image.load_ function does what it claims to do - loads the image *tiki.png* from the directory the module is run from (i.e., where you ran ``$> python TikiModule.py``).  Images loaded into pygame_ this way usually don't have any transparency information loaded with them, so we have to specify what color we'd like to be transparent.  The last line of code does this, setting the color white to be transparent.  Had we not included this line the image would have a white border around it (try it and see).

.. _pygame.image.load: http://www.pygame.org/docs/ref/image.html#pygame.image.load
.. _pygame: http://www.pygame.org

There is one more method required for the module to do anything interesting: :meth:`~aether.core.AetherModule.draw`.  This is the method that is called every frame by the :class:`~aether.core.AetherDriver` and is responsible for drawing content to the screen.  Here is the definition::

   def draw(self,screen) :
      # get the current frame
      raw_image = self.input.get_curr_frame()

      # scale incoming image to the driver screen size and blit it to the screen
      scaled_raw_image = pygame.transform.scale(raw_image,self.dims)
      screen.blit(scaled_raw_image,(0,0))

      # get the rectangle of the biggest face the input provider can find
      face = self.input.get_verts()

      # if it found a face, draw the mask
      if face is not None :
         # figure out the face's dimensions
         width, height = face[1][0]-face[0][0], face[2][1]-face[1][1]

         # scale the original image onto a new surface and draw to the screen
         scaled_tiki = pygame.transform.scale(self.tiki,(width,height))
         screen.blit(scaled_tiki,face[0])

Again, the comments are pretty self explanatory.  The :class:`~aether.core.InputProvider` interface provides, among others, two useful methods: :meth:`~aether.core.InputProvider.get_curr_frame` and :meth:`~aether.core.InputProvider.get_verts`.  The first returns a pygame.Surface_ object representing the image the camera captures (good for debugging).  The second, in the case of :class:`~aether.core.FaceInputProvider`, returns a four tuple with the four points of the rectangle defined by the face found wound clockwise from the upper leftmost corner.  If the module did not find any faces, the function returns **None**.  We cannot be sure that the image captured by the camera is the same size as our Aether screen, so we scale it first using the :attr:`~aether.core.AetherModule.dims` attribute that is set when :meth:`~aether.core.AetherModule.__init__` is called.  The scaled image is blitted to the screen starting at the top left corner (0,0).  This same scaling is performed on the tiki face.

.. _pygame.Surface: http://www.pygame.org/docs/ref/surface.html

.. note::

   Note that the original image is never modified, but rather copied to a new surface every time the method is called.  If we were to rescale the same image up and down throughout execution the image would lose quality very quickly.

Blitting the scaled tiki mask image to the screen is the last thing we need to do before the module is ready to be run.

The final step is to set up the :class:`~aether.core.AetherDriver` with a :class:`~aether.core.FaceInputProvider` instance and our new **TikiModule**.  In true pythonic fashion, the following four lines of code does exactly that::

   if __name__ == "__main__" :

      # initialize a FaceInputProvider that looks for faces from the camera image
      face_input = FaceInputProvider("/home/labadorf/development/facedetect/haarcascade_frontalface_alt.xml",flip=True)

      # create the driver
      driver = AetherDriver(640,input=face_input)

      # register the module we just wrote
      driver.register_module(TikiModule(driver))

      # go be a tiki god
      driver.run()

Alright, so it's technically five lines with the first conditional, but python programmers are so used to writing that line we barely notice it anymore, right?  The :class:`~aether.core.FaceInputProvider` constructor requires one argument - the cascade database file.  The details of what this file is is way beyond the scope of this little tutorial, which is a fancy way of saying I have no idea what it does.  Just replace the path here with the path to the *examples* directory where the file exists or to whatever path it may be in if you've moved it.  The *flip* argument tells :class:`~aether.core.FaceInputProvider` to take the mirror image of the images the camera captures.  This results in more natural feedback to the user whereby when you move your face to the left, the face detected moves with you (otherwise it would move the other way, try it out with *flip=False* to see what I mean).  The remaining code creates an :class:`~aether.core.AetherDriver` instance that has a height of 640 pixels and uses the input module we just created, has a **TikiModule** instance registered as its only module, and off it goes.  < 50 lines of code does it!  How can anyone **NOT** love python?
