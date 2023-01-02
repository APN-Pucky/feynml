from pyx import *

c = canvas.canvas()


sep = 0.2


p1 = path.path(
    path.moveto(-3, -4),
    path.lineto(1 - sep, 0 - sep),
    path.moveto(1 + sep, 0 + sep),
    path.curveto(2, 1, 3, 1, 4, 0),
    path.curveto(5, -1, 6, -1, 7 - sep, 0 - sep),
    path.moveto(7 + sep, 0 + sep),
    path.curveto(8, 1, 9, 1, 10, 0),
    path.lineto(14, -4),
)

t1 = path.path(
    path.moveto(14, -4),
    path.lineto(14 + sep, -4 - sep / 2.0),
    path.moveto(14, -4),
    path.lineto(14 + sep / 2.0, -4 - sep),
)


p2 = path.path(
    path.moveto(14, 4),
    path.lineto(10 + sep, 0 + sep),
    path.moveto(10 - sep, 0 - sep),
    path.curveto(9, -1, 8, -1, 7, 0),
    path.curveto(6, 1, 5, 1, 4 + sep, 0 + sep),
    path.moveto(4 - sep, 0 - sep),
    path.curveto(3, -1, 2, -1, 1, 0),
    path.lineto(-3, 4),
)

t2 = path.path(
    path.moveto(-3, 4),
    path.lineto(-3 - sep, 4 + sep / 2.0),
    path.moveto(-3, 4),
    path.lineto(-3 - sep / 2.0, 4 + sep),
)


c.stroke(
    p1, [color.cmyk.RoyalBlue, style.linewidth.THICK, deco.earrow.LARge, deco.barrow]
)
c.stroke(t1, [color.cmyk.RoyalBlue, style.linewidth.thick])


c.stroke(
    p2, [color.cmyk.MidnightBlue, style.linewidth.THICK, deco.earrow.LARge, deco.barrow]
)
c.stroke(t2, [color.cmyk.MidnightBlue, style.linewidth.thick])


c.writeSVGfile("pyfeyn-logo")
