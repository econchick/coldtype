from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
from fontTools.pens.basePen import BasePen

try:
    import cairo
except:
    pass

if __name__ == "__main__":
    import sys
    import os
    dirname = os.path.realpath(os.path.dirname(__file__))
    sys.path.append(f"{dirname}/../..")

from coldtype.geometry import Rect, Edge, Point
from coldtype.pens.drawablepen import DrawablePenMixin
from coldtype.color import Color, Gradient
from coldtype.beziers import raise_quadratic
import base64


class CairoPen(DrawablePenMixin, BasePen):
    def __init__(self, dat, h, ctx, style=None):
        super().__init__(None)
        self.dat = dat
        self.h = h
        self.ctx = ctx
        self._value = []
        tp = TransformPen(self, (1, 0, 0, -1, 0, h))
        
        attrs = list(self.findStyledAttrs(style))
        methods = [a[0] for a in attrs]

        if True or "shadow" not in methods:
            for attr in attrs:
                method, *args = attr
                self.ctx.save()
                if method in ["fill", "stroke"]:
                    dat.replay(tp)
                self.applyDATAttribute(attr)
                self.ctx.restore()

    def _moveTo(self, p):
        self.ctx.move_to(p[0], p[1])
        self._value.append(p)

    def _lineTo(self, p):
        self.ctx.line_to(p[0], p[1])
        self._value.append(p)

    def _curveToOne(self, p1, p2, p3):
        self.ctx.curve_to(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1])
        self._value.extend([p1, p2, p3])

    def _qCurveToOne(self, p1, p2):
        start = self._value[-1]
        q1, q2, q3 = raise_quadratic(start, (p1[0], p1[1]), (p2[0], p2[1]))
        self.ctx.curve_to(q1[0], q1[1], q2[0], q2[1], q3[0], q3[1])
        self._value.extend([q1, q2, q3])

    def _closePath(self):
        self.ctx.close_path()
    
    def fill(self, color=None):
        if color:
            if isinstance(color, Gradient):
                self.gradient(color)
            else:
                self.ctx.set_source_rgba(color.red, color.green, color.blue, color.alpha)
            self.ctx.fill()
    
    def stroke(self, weight=1, color=None):
        self.ctx.set_source_rgba(color.red, color.green, color.blue, color.alpha)
        self.ctx.set_line_width(weight)
        self.ctx.stroke()
    
    def gradient(self, gradient):
        pat = cairo.LinearGradient(*[p for s in reversed(gradient.stops) for p in s[1]])
        for idx, stop in enumerate(gradient.stops):
            c = stop[0]
            pat.add_color_stop_rgba(idx, c.red, c.green, c.blue, c.alpha)
        self.ctx.set_source(pat)
    
    def image(self, src=None, opacity=None, rect=None):
        image_surface = cairo.ImageSurface.create_from_png(src)
        pattern = cairo.SurfacePattern(image_surface)
        pattern.set_extend(cairo.Extend.REPEAT)
        if rect:
            self.ctx.scale(rect.h/self.h/2, rect.h/self.h/2)
        else:
            self.ctx.scale(0.5, 0.5)
        #self.ctx.translate(left, top)
        self.ctx.set_source(pattern)
        #self.ctx.set_source_surface(pattern)
        self.ctx.paint_with_alpha(opacity)
        pass
    
    def shadow(self, clip=None, radius=10, alpha=0.3, color=Color.from_rgb(1,0,0,1)):
        pass
    
    def Composite(pens, rect, image_path, save=True, style=None):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(rect.w*2), int(rect.h*2))
        ctx = cairo.Context(surface)
        ctx.scale(2, 2)
        for pen in CairoPen.FindPens(pens):
            CairoPen(pen, rect.h, ctx, style=style)
        if save:
            surface.write_to_png(image_path)
        else:
            print("Should write to base64 and return — not yet supported")

if __name__ == "__main__":
    from coldtype.pens.datpen import DATPen
    from coldtype.pens.svgpen import SVGPen
    from coldtype.viewer import viewer
    from random import random
    
    r1 = Rect((0, 0, 50, 50))
    p1 = os.path.realpath(f"{dirname}/../../test/artifacts/cairopen_test3.png")

    dp = DATPen(fill=(1, 0, 0.5)).oval(r1.inset(10, 10))
    CairoPen.Composite([dp], r1, p1, style="default")

    r = Rect((0, 0, 500, 500))
    p2 = os.path.realpath(f"{dirname}/../../test/artifacts/cairopen_test2.png")
    
    dp = DATPen(fill=Gradient.Random(r), stroke=dict(weight=20, color="royalblue"))
    dp.attr("dark", fill="black", stroke="hotpink", strokeWidth=20)
    dp.oval(r.inset(100, 100))
    dp2 = DATPen(fill=None, image=dict(src=p1, opacity=0.3, rect=r1)).rect(r)

    CairoPen.Composite([dp, dp2], r, p2, style="default")
    
    with viewer() as pv:
        pv.send(SVGPen.Composite([dp, dp2], r), r)
        pv.send(p1, r1, image=True)
        pv.send(p2, r, image=True)