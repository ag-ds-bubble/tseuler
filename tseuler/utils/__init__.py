from .dt_utils import get_datasummary
import colorsys

get_valhexrg = lambda x : '#%02x%02x%02x' % tuple(int(k*255) for k in colorsys.hsv_to_rgb((133/360)*x, .89, .56))
get_valhex11rg = lambda x : '#%02x%02x%02x' % tuple(int(k*255) for k in colorsys.hsv_to_rgb((133/360)*(1+x)*0.5, .89, .56))
get_valhexgr = lambda x : '#%02x%02x%02x' % tuple(int(k*255) for k in colorsys.hsv_to_rgb((133/360)*(1-x), .89, .56))
get_rgbtohex = lambda r,g,b : '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))
