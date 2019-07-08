__author__ = 'Bauer'

from graphics import GraphicsWindow

def drawHappyFace(canvas,x,y):
    canvas.setColor("yellow")
    canvas.setOutline("black")
    #canvas.drawOval(100, 100, 30, 30)
    canvas.drawOval(x, y, 30, 30)
    canvas.setColor("black")
    #canvas.drawOval(108, 110, 5, 5)
    canvas.drawOval(x+8, y+10, 5, 5)
    #canvas.drawOval(118, 110, 5, 5)
    canvas.drawOval(x+18, y+10, 5, 5)
    #canvas.drawLine(110, 122, 113, 125)
    canvas.drawLine(x+10, y+22, x+13, y+25)
    #canvas.drawLine(113, 125, 117, 125)
    canvas.drawLine(x+13, y+25, x+17, y+25)
    #canvas.drawLine(117, 125, 120, 122)
    canvas.drawLine(x+17, y+25, x+20, y+22)

def drawSadFace(canvas,x,y):
    canvas.setColor("yellow")
    canvas.setOutline("black")
    #canvas.drawOval(100, 100, 30, 30)
    canvas.drawOval(x, y, 30, 30)
    canvas.setColor("black")
    #canvas.drawOval(108, 110, 5, 5)
    canvas.drawOval(x+8, y+10, 5, 5)
    #canvas.drawOval(118, 110, 5, 5)
    canvas.drawOval(x+18, y+10, 5, 5)
    #canvas.drawLine(110, 122, 113, 125)
    canvas.drawLine(x+10, y+23, x+13, y+20)
    #canvas.drawLine(113, 125, 117, 125)
    canvas.drawLine(x+13, y+20, x+17, y+20)
    #canvas.drawLine(117, 125, 120, 122)
    canvas.drawLine(x+17, y+20, x+20, y+23)

def drawSimpleHistogram(eval,cval,mval,pval):
    # Draws a simple histogram of 4 values - sentiment values from 4 regions
    # Assumes that the values are in the range of 0-10
    #
    # Parameters:
    #   - eval - value of the Eastern region
    #   - cval - value of the Central region
    #   - mval - value of the Mountain region
    #   - pval - value of the Pacific region

    win = GraphicsWindow(400, 400)
    canvas = win.canvas()
    wid = 400
    hght = 400
    C = 0.8
    facew = 30
    step = 5
    if ((wid-(80+2*facew)) < 100) or (hght < 150):
        canvas.drawText(wid/2-10,hght/2-10,"Oops! Window dimensions too small!")
    else:
        wuse = wid-(80+2*facew)
        huse = (hght-120)/5
        barx = 110+step # 80 plus width of face, which is 30, plus step
        endofbar = wid-facew-step
        canvas.drawLine(75, 0, 75, hght)
        # Draw bar for East
        canvas.drawText(2, huse, "Eastern")
        drawSadFace(canvas, 80, C*huse)
        lngth = wuse*eval/10.0
        canvas.setColor(240,0,0)
        canvas.setOutline("black")
        canvas.drawRectangle(barx, C*huse, lngth, facew)
        drawHappyFace(canvas,endofbar,C*huse)
        # Draw bar for Central
        canvas.drawText(2, 2*huse+facew, "Central")
        drawSadFace(canvas, 80, (1+C)*huse+facew)
        lngth = wuse*cval/10.0
        canvas.setColor(120,240,120)
        canvas.setOutline("black")
        canvas.drawRectangle(barx, (1+C)*huse+facew, lngth, facew)
        drawHappyFace(canvas, endofbar, (1+C)*huse+facew)
                # Draw bard for Mountain
        canvas.drawText(2, 3*huse+2*facew, "Mountain")
        drawSadFace(canvas, 80, (2+C)*huse+2*facew)
        lngth = wuse*mval/10.0
        canvas.setColor(0,0,240)
        canvas.setOutline("black")
        canvas.drawRectangle(barx, (2+C)*huse+2*facew, lngth, facew)
        drawHappyFace(canvas, endofbar, (2+C)*huse+2*facew)
        # Draw bar for Pacific
        canvas.drawText(2, 4*huse+3*facew, "Pacific")
        drawSadFace(canvas, 80, (3+C)*huse+3*facew)
        lngth = wuse*pval/10.0
        canvas.setColor(120,120,120)
        canvas.setOutline("black")
        canvas.drawRectangle(barx, (3+C)*huse+3*facew, lngth, facew)
        drawHappyFace(canvas, endofbar, (3+C)*huse+3*facew)
        win.wait()
