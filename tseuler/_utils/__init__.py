import colorsys

get_valhexrg = lambda x : '#%02x%02x%02x' % tuple(int(k*255) for k in colorsys.hsv_to_rgb((133/360)*x, .89, .56))
get_valhex11rg = lambda x : '#%02x%02x%02x' % tuple(int(k*255) for k in colorsys.hsv_to_rgb((133/360)*(1+x)*0.5, .89, .56))
get_valhexgr = lambda x : '#%02x%02x%02x' % tuple(int(k*255) for k in colorsys.hsv_to_rgb((133/360)*(1-x), .89, .56))
get_rgbtohex = lambda r,g,b : '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))




# Inspired from  :- https://stackoverflow.com/a/23788343/6297658
from bisect import bisect
# A mapping of breakpoints for _suffixes.
_suffixes = {1e-9: 'n',
            1e-6: 'u',
            1e-3: 'm',
            1: '',
            1e3: 'k',
            1e6: 'M',
            1e9: 'G',
            1e12: 'T',
            1e15: 'Y'}

# List of sorted breakpoints' values.
_suffix_breakpoints = sorted(_suffixes.keys())

def format_with_suffix(num):
    num_format = '{:.2f}{}'
    if not num:
       return num_format.format(num, '')

    if num in _suffixes:
       return num_format.format(1.0, _suffixes[num])

    is_negative = num<0
    if is_negative: num = abs(num)


    # Find the index of first breakpoint `x`, that's greater than `num`
    # using binary search.
    breakpoint_idx = bisect(_suffix_breakpoints, num)

    # Get the breakpoint's value. If `num` is lower than the first breakpoint, use
    # that instead.
    breakpoint = _suffix_breakpoints[breakpoint_idx - 1 if breakpoint_idx else 0]

    # Get the suffix.
    suffix = _suffixes[breakpoint]
    formatted_num = num_format.format(float(num) / breakpoint, suffix)
    if is_negative : formatted_num = '-'+formatted_num
    return formatted_num