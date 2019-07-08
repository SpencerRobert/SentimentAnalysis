# graphics.py
# (c) 2013 by Rance Necaise
# http://graphics.necaiseweb.org
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

## graphics.py
#  version 1.0
#  This module is part of the PyWare open source project that provides modules and
#  and tools for use in the classroom. This module provides classes for creating
#  top-level GUI windows that can be used for creating and displaying simple
#  geometric shapes and color digital images. Complete documentation of the module
#  is available at http://graphics.necaseweb.org.

import tkinter as tk

## This class defines a basic top level window that can be opened on the
#  desktop and used to produce simple graphical drawings. It contains a
#  canvas on which geometric shapes can be drawn and manipulated.
#
class GraphicsWindow :
  ## Creates a new graphics window with an empty canvas.
  #  @param width The horizontal size of the canvas in pixels.
  #  @param height The vertical size of the canvas in pixels.
  #
  def __init__(self, width = 400, height = 400) :
    global TheMainWindow

     # Is the window open or closed. It must be open to use most operations.
    self._isClosed = False

     # If this is the first toplevel window, remember it as the main window. The
     # event loop is only terminated when the main window is closed.
    if TheMainWindow is None :
      TheMainWindow = self

     # Create a top-level window for the graphics window.
    self._tkwin = tk.Toplevel(rootWin, padx=0, pady=0, bd=0)
    self._tkwin.protocol("WM_DELETE_WINDOW", self.close)
    self._tkwin.title("")

     # Create a canvas inside the top-level window which is used for
     # drawing the graphical objects and text.
    self._canvas = GraphicsCanvas( self, width, height )

     # Bring the window to the front of all other windows and force an update.
    self._tkwin.lift()
    self._tkwin.resizable(0, 0)
    self._tkwin.update_idletasks()

  ## Closes and destroys the window. A closed window can not be used.
  #
  def close(self) :
     # Set the closed flag to true so no other ops can be performed on
     # the window object.
    if self._isClosed : return
    self._isClosed = True

     # Destroy the window and force an update so it will close when
     # used in IDLE or Wing IDE.
    self._tkwin.destroy()
    self._tkwin.update_idletasks()

     # If the main window is being closed, then the mainloop has to be terminated.
    if self is TheMainWindow :
       self._tkwin.quit()

  ## Starts the event loop which handles various window events. This causes
  #  the sequential execution of the program to stop and wait for the user
  #  to click the close button on the main window or to call the quit method
  #  on any window. This method should only be called on the main window.
  #
  def wait(self) :
    if not self._isClosed :
      self._tkwin.mainloop()

  ## Returns a reference to the canvas contained within the window.
  #  The canvas can be used to draw and manipulate geometric shapes and text.
  #  @return A reference to the GraphicsCanvas contained in the window.
  #
  def canvas(self) :
    if self._isClosed : raise GraphicsWinError()
    return self._canvas

  ## Sets the title of the window. By default, the window has no title.
  #  @param title A text string to which the title of the window is set. To
  #          remove the title, use pass an empty string to the method.
  #
  def setTitle(self, title) :
    self._tkwin.title( title )

  ## Returns a Boolean indicating whether the window exists or was previously closed.
  #  Window operations can not be performed on a closed window.
  #  @return @c True if the window is closed and @c False otherwise.
  #
  def isClosed(self) :
    return self._isClosed

  ## Hides or iconifies the top level window.
  #  The window still exists and can be displayed again using the show method.
  #
  def hide(self) :
    if self._isClosed : raise GraphicsWinError()
    self._tkwin.withdraw()
    self._tkwin.update_idletasks()

  ## Shows or deiconifies a previously hidden top level window.
  #
  def show(self) :
    if self._isClosed : raise GraphicsWinError()
    self._tkwin.deiconify()
    self._tkwin.update_idletasks()


#--- The graphics canvas.

## This class defines a canvas on which geometric shapes and text can be
#  drawn. The canvas uses discrete Cartesian coordinates >= 0 with (0,0)
#  being in the upper-left corner of the window. Unlike a canvas that a
#  painter might use, shapes drawn on a graphics canvas are stored as
#  objects that can later be reconfigured without having to redraw them.
#  A collection of shape properties are also maintained as part of the
#  canvas. These properties, which can be changed by calling specific
#  methods, are used in drawing the various shapes and text. All shapes
#  and text are drawn using the current context or the property settings
#  at the time the shape is first drawn.
#
class GraphicsCanvas :
  ## Creates a new empty graphics canvas. A graphics canvas is
  #  automatically created as part of a GraphicsWindow. Thus, there should
  #  be no need for the user of this module to explicitly create one.
  #  @param win, A reference to the GraphicsWindow in which the canvas is used.
  #  @param width, (int) The width of the canvas in pixels.
  #  @param height, (int) The height of the canvas in pixels.
  #
  def __init__(self, win, width, height) :
    # The GraphicsWindow that contains the canvas.
   self._win = win

    # Keep track of the size of the canvas.
   self._width = width
   self._height = height

    # Maintain the options used for drawing objects and text.
   self._polyOpts = {"outline" : "black", "width" : 1, "dash" : None, "fill" : ""}
   self._textOpts = {"text" : "", "justify" : tk.LEFT, "anchor" : tk.NW,
                     "fill" : "black",
                     "font" : ("helvetica", 10, "normal") }

    # Create the tk canvas inside the given window.
   self._tkcanvas = tk.Canvas(self._win._tkwin, highlightthickness = 0,
                              width = width, height = height, bg = "white" )
   self._tkcanvas.pack()


  ## Changes the height of the canvas.
  #  The window is resized to fit the size of the canvas.
  #  @param size (int) The new height of the canvas in number of pixels.
  #
  def setHeight(self, size) :
    self._checkValid()
    if type(size) != int or size <= 0 :
      raise GraphicsParamError( "The window height must be >= 1." )
    self._tkcanvas.config(height=size)
    self._height = size
    self._tkcanvas.update_idletasks()

  ## Changes the width of the canvas.
  #  The window is resized to fit the size of the canvas.
  #  @param size (int) The new width of the canvas in number of pixels.
  #
  def setWidth(self, size) :
    self._checkValid()
    if type(size) != int or size <= 0 :
      raise GraphicsParamError( "The window width must be >= 1." )
    self._tkcanvas.config(width=size)
    self._width = size
    self._tkcanvas.update_idletasks()

  ## Returns the height of the canvas.
  #  @return The canvas height in number of pixels.
  #
  def height( self ):
    return self._height

  ## Returns the width of the canvas.
  #  @return The canva width in number of pixels.
  #
  def width( self ):
    return self._width

  ## Clears the canvas by removing all items previously drawn on it. The canvas
  #  acts as a container of shapes and text. Thus, when a geometric shape or
  #  text is drawn on the canvas, it is maintained internally as an object
  #  until cleared.
  #
  def clear(self):
    self._checkValid()
    self._tkcanvas.delete(tk.ALL)
    self._tkcanvas.update_idletasks()

  ## Sets the current background color of the canvas. The color can either
  #  be specified as a string that names a color or as three integer values
  #  in the range [0..255].
  #
  #     c.setBackground(colorname)
  #     c.setBackground(red, green, blue)
  #
  def setBackground(self, red, green = None, blue = None) :
    if type(red) == int :
      color = "#%02X%02X%02X" % (red, green, blue)
    elif type(red) != str :
      raise GraphicsParamError( "Invalid color." )
    else :
      color = red
    self._checkValid()
    self._tkcanvas.config(bg = color)
    self._tkcanvas.update_idletasks()

  ## Sets the fill color used when drawing new polygon shapes. The color
  #  can be specified either as a string that names the color or as three
  #  integer values in the range [0..255]. If no argument is provided, it
  #  clears the fill color and the shapes will be drawn in outline form only.
  #
  #     c.setFill()
  #     c.setFill(colorname)
  #     c.setFill(red, green, blue)
  #
  def setFill( self, red = None, green = None, blue = None) :
    if red is None :
      color = ""
    elif type(red) == int :
      color = "#%02X%02X%02X" % (red, green, blue)
    elif type(red) != str :
      raise GraphicsParamError( "Invalid color." )
    else :
      color = red
    self._polyOpts["fill"] = color

  ## Sets the outline color used when drawing new polygon shapes and the
  #  color used to draw lines, pixels, and text. The color can be specified
  #  either as a string that names the color or as three integer values in
  #  the range [0..255]. If no argument is provided, it clears the outline
  #  color. A cleared outline color is only meant for drawing polygon type
  #  shapes that are only filled, without an outline.
  #
  #     c.setOutline()
  #     c.setOutline(colorname)
  #     c.setOutline(red, green, blue)
  #
  def setOutline( self, red = None, green = None, blue = None) :
    if red is None :
      color = ""
    elif type(red) == int :
      color = "#%02X%02X%02X" % (red, green, blue)
    elif type(red) != str :
      raise GraphicsParamError( "Invalid color." )
    else :
      color = red
    self._polyOpts["outline"] = color
    self._textOpts["fill"] = color

  ## Sets both the fill and outline colors used when drawing shapes and text
  #  on the canvas. The color can be specified either as a string that names
  #  the color or as three integer values in the range [0..255].
  #
  #     c.setFill(colorname)
  #     c.setFill(red, green, blue)
  #
  def setColor( self, red, green = None, blue = None ) :
    if type(red)  == int :
       color = "#%02X%02X%02X" % (red, green, blue)
    elif type(red) != str :
       raise GraphicsParamError( "Invalid color." )
    else :
       color = red
    self._polyOpts["outline"] = color
    self._polyOpts["fill"] = color
    self._textOpts["fill"] = color

  ## Sets the width of lines drawn on the canvas. This includes the line and
  #  vector shapes and the outlines of polygons.
  #  @param size (int) The new line width in number of pixels.
  #
  def setLineWidth(self, size) :
    if type(size) != int or size <= 0 :
      raise GraphicsParamError( "Invalid line width." )
    self._polyOpts["width"] = size

  ## Sets the style used to drawn lines on the canvas. This includes the line
  #  and vector shapes and the outlines of polygons.
  #  @param style (str) The style to use for new lines. It can be either
  #               "solid" or "dashed".
  #
  def setLineStyle(self, style) :
    if style == "solid" :
      self._polyOpts["dash"] = None
    elif style == "dashed" :
      self._polyOpts["dash"] = (4,)
    else :
      raise GraphicsParamError("Invalid line style.")

  ## Sets the font used to draw text on the canvas.
  #  @param family (str) The font family. It can be one of:
  #            "arial", "courier", "times", "helvetica".
  #  @param size (int) The point size of the font.
  #  @param style (string) The font style. It can be one of:
  #            "normal", "bold", "italic", or "bold italic".
  #
  def setTextFont(self, family = None, size = None, style = None) :
    origFamily, origSize, origStyle = self._fontOpts["font"]
    if (family is not None and
       family not in ('helvetica', 'arial', 'courier', 'times', 'times roman')) :
      raise GraphicsParamError( "Invalid font family." )
    else :
      family = origFamily

    if (style is not None and
       style not in ('bold', 'normal', 'italic', 'bold italic')) :
      raise GraphicsParamError( "Invalid font style." )
    else :
      style = origStyle

    if size is not None and (type(size) != int or size <= 0) :
      raise GraphicsParamError( "Invalid font size." )
    else :
       size = origSize

    self._textOpts["font"] = (family, size, style)

  ## Sets the position that text is drawn in relation to a bounding box.
  #  The (x, y) coordinate provided with drawText() is anchored to a spot on
  #  the bounding box that surrounds the text and the text is positioned
  #  relative to the anchor.
  #  @param position A string indicating the anchor position on the
  #              bounding box. It can be one of:
  #              "n", "s", "e", "w", "center", "nw", "ne", "sw", "se".
  #
  def setTextAnchor(self, position) :
    if position not in ('n', 's', 'e', 'w', 'nw', 'ne', 'sw', 'se', 'center') :
      raise GraphicsParamError( "Invalid anchor position." )
    self._textOpts["anchor"] = position

  ## Sets the justification used to draw new multiline text on the canvas..
  #  @param style A string specifying the justification. It can be one of:
  #               "left", "center", or "right".
  #
  def setTextJustify(self, style) :
    if style == "left" :
      self._fontOpts["justify"] = tk.LEFT
    elif style == "center" :
      self._fontOpts["justify"] = tk.CENTER
    elif style == "right" :
      self._fontOpts["justify"] = tk.RIGHT
    else :
      raise GraphicsParamError( "Invalid justification value." )

 #--- The shape drawing methods.

  ## Draws or plots a single point (pixel) on the canvas.
  #  @param x, y  Integers indicating the (x, y) pixel coordinates at which
  #               the point is drawn.
  #  @return An integer that uniquely identifies the new canvas item.
  #
  def drawPoint( self, x, y ):
    self._checkValid()
    obj = self._tkcanvas.create_line( x, y, x+1, y,
                                    fill=self._polyOpts["outline"],
                                    width=self._polyOpts["width"] )
    self._tkcanvas.update_idletasks()
    return obj

  ## Draws a line segment on the canvas. The line is drawn between two
  #  discrete end points.
  #  @param x1, y1 The coordinates of the starting point.
  #  @param x2, y2 The coordinates of the ending point.
  #  @return An integer that uniquely identifies the new canvas item.
  #
  def drawLine(self, x1, y1, x2, y2) :
    self._checkValid()
    obj = self._tkcanvas.create_line( x1, y1,
                                     x2, y2,
                                     fill=self._polyOpts["outline"],
                                     width=self._polyOpts["width"],
                                     dash=self._polyOpts["dash"] )
    self._tkcanvas.update_idletasks()
    return obj

  ## Draws an arrow or vector on the canvas. The same as a line segment,
  #  except an arrow head is drawn at the end of the segment.
  #  @returns An integer that uniquely identifies the new canvas item.
  #
  def drawArrow(self, x1, y1, x2, y2) :
    self._checkValid()
    obj = self._tkcanvas.create_line( x1, y1, x2, y2,
                                     fill=self._polyOpts["outline"],
                                     width=self._polyOpts["width"],
                                     dash=self._polyOpts["dash"],
                                     arrow=tk.LAST )
    self._tkcanvas.update_idletasks()
    return obj

  ## Draws a rectangle on the canvas. The rectangle is defined by the coordinates
  #  of the upper left corner of the rectangle and its width and height.
  #  @param x, y The coordinates of the upper-left corner of the rectangle.
  #  @param width, height The dimensions of the rectangle.
  #  @returns An integer that uniquely identifies the new canvas item.
  #
  def drawRectangle(self, x, y, width, height) :
    self._checkValid()
    obj = self._tkcanvas.create_rectangle(x, y, x + width, y + height, self._polyOpts )
    self._tkcanvas.update_idletasks()
    return obj

  ## The same as drawRectangle().
  #
  def drawRect(self, x, y, width, height) :
    return self.drawRectangle(x, y, width, height)

  ## Draws a polygon on the canvas. The polygon is defined by three or more vertices
  #  specified in counter-clockwise order. There are two forms of the method:
  #
  #     c.drawPolygon(x1, y1, x2, y2, ..., xN, yN)
  #     c.drawPolygon(sequence)
  #
  #  @returns An integer that uniquely identifies the new canvas item.
  #
  def drawPolygon( self, *coords ):
     # Unwrap the cooridinates which allows the method to accept individual vertices
     # or a list of vertices.
    if len(coords) == 1 and (type(coords[0]) == list or type(coords[0] == tuple)) :
       expCoords = tuple(*coords)
    else :
       expCoords = coords

    self._checkValid()
    if len(expCoords) < 6 :
      raise GraphicsParamError( "At least 3 vertices must be provided." )
    obj = self._tkcanvas.create_polygon( expCoords, self._polyOpts )
    self._tkcanvas.update_idletasks()
    return obj

  ## The same as drawPolygon().
  #
  def drawPoly(self, *coords) :
    return self.drawPolygon(coords)

  ## Draws an oval on the canvas. The oval is defined by a bounding rectangle
  #  that is specified by the coordinates of its upper-left corner and its
  #  dimensions.
  #  @param x, y The upper-left coordinates of the bounding rectangle.
  #  @param width, height The dimensions of the bounding rectangle.
  #  @returns An integer that uniquely identifies the new canvas item.
  #
  def drawOval( self, x, y, width, height ):
    self._checkValid()
    obj = self._tkcanvas.create_oval( x, y, x + width, y + height, self._polyOpts )
    self._tkcanvas.update_idletasks()
    return obj


  ## Draws an arc or part of a circle on the canvas. The arc is defined by a
  #  bounding square and two angles. The angles are specified in degrees with
  #  zero degrees corresponding to the x-axis.
  #  @param x, y The upper-left coordinates of the bounding square.
  #  @param diameter The dimensions of the bounding rectangle.
  #  @param startAngle The angle in degrees at which the arc begins.
  #  @param extent The extent of the arc given as an angle in degrees.
  #  @returns An integer that uniquely identifies the new canvas item.
  #
  def drawArc( self, x, y, diameter, startAngle, extent ):
    self._checkValid()
    obj = self._tkcanvas.create_arc( x, y, x + diameter, y + diameter, self._polyOpts,
                                    start=startAngle, extent=extent )
    self._tkcanvas.update_idletasks()
    return obj

  ## Draws text on the canvas. The text is drawn such that an anchor point on a
  #  bounding box is positioned at a given point on the canvas. The default
  #  position of the anchor is in the upper-left (northwest) corner of the
  #  bounding box. The anchor position can be changed using the setTextAnchor()
  #  method. The text is drawn using the default font family, size, and style.
  #  The setTextFont() method can be used to change those characteristics. The
  #  text to be drawn can consists of multiple lines, each separated by a
  #  newline character. The justification of the text can be set when drawing
  #  multiple lines of text.
  #  @param x, y The position on the canvas at which the anchor point of the
  #              bounding box is positioned.
  #  @param text A string containing the text to be drawn on the canvas.
  #
  def drawText(self, x, y, text) :
    self._checkValid()
    self._textOpts["text"] = text
    obj = self._tkcanvas.create_text( x, y, self._textOpts )
    self._tkcanvas.update_idletasks()
    return obj

 #--- Methods that can be used to manipulate the item previously drawn on the
 #--- canvas. Each drawing method returns a unique id number used to identify
 #--- the resulting shape. See the online documentation for more information.

  def shiftItem(self, itemId, dx, dy) :
    self._checkContains(itemId)
    self._tkcanvas.move(itemId, dx, dy)
    self._tkcanvas.update_idletasks()

  def removeItem(self, itemId) :
    self._checkContains(itemId)
    self._tkcanvas.delete(itemId)
    self._tkcanvas.update_idletasks()

  def showItem(self, itemId) :
    self._checkContains(itemId)
    self._tkcanvas.itemconfig(itemId, state = "normal")
    self._tkcanvas.update_idletasks()

  def hideItem(self, itemId) :
    self._checkContains(itemId)
    self._tkcanvas.itemconfig(itemId, state = "hidden")
    self._tkcanvas.update_idletasks()

  def raiseItem(self, itemId, above = None) :
    self._checkContains(itemId)
    self._tkcanvas.tag_raise(itemId)
    self._tkcanvas.update_idletasks()

  def lowerItem(self, itemId, below = None) :
    self._checkContains(itemId)
    self._tkcanvas.tag_lower(itemId)
    self._tkcanvas.update_idletasks()

  def __contains__(self, itemId):
    if self._tkcanvas.winfo_ismapped() :
      return len(self._tkcanvas.find_withtag(itemId)) > 0
    else :
      return False

  def itemType(self, itemId) :
    self._checkContains(itemId)
    return self._canvas.type(itemId)

  def items( self ):
    self._checkValid()
    return self.find_all()

 #--- Helper methods.
  def _checkValid( self ):
    if self._win.isClosed() :
      raise GraphicsWinError()

  def _checkContains(self, itemId) :
    if self._win.isClosed() : raise GraphicsWinError()
    if itemId in self : raise GraphicsObjError()



## This class defines a basic top level window that can contains a digital
#  image, the pixels of which can be accessed or set.
#
class ImageWindow :
  ## Creates a new image window with an empty image.
  #  @param width The horizontal size of the image in pixels.
  #  @param height The vertical size of the image in pixels.
  #
  def __init__(self, width = 400, height = 400):
    global TheMainWindow

     # Is the window open or closed. It must be open to use most operations.
    self._isClosed = False

     # If this is the first toplevel window, remember it as the main window. The
     # event loop is only terminated when the main window is closed.
    if TheMainWindow is None :
      TheMainWindow = self

     # Create a top-level window for the graphics window.
    self._tkwin = tk.Toplevel(rootWin, width=width, height=height,
                              borderwidth=0, padx=0, pady=0, bd=0)
    self._tkwin.protocol("WM_DELETE_WINDOW", self.close)
    self._tkwin.title("")

     # Create the photo image and tk canvas inside the window.
    self._tkimage = tk.PhotoImage(width=width, height=height)
    self._tkcanvas = tk.Canvas(self._tkwin, width=width, height=height,
                               bg = "white", bd = 0)

     # Add the photo image object to the canvas.
    self._tkcanvas.create_image(0, 0, anchor="nw", image=self._tkimage)
    self._tkcanvas.pack()

     # Bring the window to the front of all other windows and force an update.
    self._tkwin.lift()
    self._tkwin.resizable(0, 0)
    self._tkwin.update_idletasks()

  ## Sets the title of the window. By default, the window has no title.
  #  @param title A text string to which the title of the window is set. To
  #          remove the title, use pass an empty string to the method.
  #
  def setTitle(self, title) :
    self._tkwin.title( title )

  ## Returns a Boolean indicating whether the window exists or was previously closed.
  #  Window operations can not be performed on a closed window.
  #  @return @c True if the window is closed and @c False otherwise.
  #
  def isClosed(self) :
    return self._isClosed

  ## Hides or iconifies the top level window.
  #  The window still exists and can be displayed again using the show method.
  #
  def hide(self) :
    if self._isClosed : raise GraphicsWinError()
    self._tkwin.withdraw()
    self._tkwin.update_idletasks()

  ## Shows or deiconifies a previously hidden top level window.
  #
  def show(self) :
    if self._isClosed : raise GraphicsWinError()
    self._tkwin.deiconify()
    self._tkwin.update_idletasks()

  ## Closes and destroys the window. A closed window can not be used.
  #
  def close( self ):
     # Set the closed flag to true so no other ops can be performed on
     # the window object.
    if self._isClosed : return
    self._isClosed = True

     # Destroy the window and force an update so it will close when
     # used in IDLE or Wing IDE.
    self._tkwin.destroy()
    self._tkwin.update_idletasks()

     # Terminate the mainloop so the program will exit.
    self._tkwin.quit()

  ## Starts the event loop which handles various window events. This causes
  #  the sequential execution of the program to stop and wait for the user
  #  to click the close button on the main window or to call the quit method
  #  on any window. This method should only be called on the main window.
  #
  def wait( self ):
    if self._isClosed : raise GraphicsWinError()
    self._tkwin.mainloop()

  ## Sets a pixel to a given RGB color.
  #  @param row, col The pixel coordinates.
  #  @param red, green, blue The discrete RGB color components in the range [0..255].
  #
  def setPixel(self, row, col, red, green, blue) :
    self._tkimage.put("#%02x%02x%02x" % (red, green, blue), (col, row))

  ## Returns a 3-tuple containing the RGB color of a given pixel.
  #  @param row, col The pixel coordinates.
  #  @returns An RGB color as a 3-tuple.
  #
  def getPixel(self, row, col) :
    string = self._tkimage.get(col, row)
    parts = string.split()
    return (int(parts[0]), int(parts[1]), int(parts[2]))

# --- Defines special graphics exceptions that are raised when an error
# --- occurs in a GraphicsWindow method.
class GraphicsError( Exception ) :
  def __init__( self, message ):
    super(GraphicsError, self).__init__( message )

class GraphicsObjError( GraphicsError ) :
  def __init__( self ):
    super(GraphicsObjectError, self).__init__( "Invalid object id." )

class GraphicsWinError( GraphicsError ) :
  def __init__( self ):
    super(GraphicsWinError, self).__init__(
              "Operation can not be performed on a closed window." )

class GraphicsParamError( GraphicsError ) :
  def __init__( self, message ):
    super(GraphicsParamError, self).__init__( message )


# --- Create an invisible root window and initialize the Tk system.
rootWin = tk.Tk()
rootWin.withdraw()

# --- Remember the first toplevel window created which serves as the main window.
TheMainWindow = None


