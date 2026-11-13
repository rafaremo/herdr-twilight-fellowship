# Turns generated sprite sheets and pictures in GEN into the mods' art in MODS.
# usage: python3 build-art.py <gen dir> <mods dir> [names...]
import sys, os
from PIL import Image

GEN, OUT = sys.argv[1], sys.argv[2]
ONLY = set(sys.argv[3:])
W, H, SCALE = 36, 48, 4  # sprite pixels, shown at 4x like Traveler's
GOLD, INK = (227, 160, 79, 255), (11, 17, 36, 255)


def key(img):
    """Pure green background (and its antialiased fringe) -> transparent."""
    img = img.convert("RGBA")
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            spill = g - max(r, b)
            # Some sheets come back already transparent, with a faint haze around the figure.
            if a < 128:
                px[x, y] = (0, 0, 0, 0)
            elif (g > 150 and spill > 70) or (g > 110 and spill > 55):
                px[x, y] = (0, 0, 0, 0)
            elif spill > 25 and g > 90:
                px[x, y] = (r, max(r, b), b, a)  # despill the edge
    return img


def frames(img, want=4):
    """Split a keyed sheet into `want` figures by empty columns."""
    alpha = img.getchannel("A")
    cols = [any(alpha.getpixel((x, y)) for y in range(0, img.height, 2)) for x in range(img.width)]
    segs, start = [], None
    for x, on in enumerate(cols + [False]):
        if on and start is None:
            start = x
        elif not on and start is not None:
            segs.append([start, x])
            start = None
    segs = [s for s in segs if s[1] - s[0] > 6]
    while len(segs) > want:  # glue sword tips and sparks back onto their figure
        i = min(range(len(segs) - 1), key=lambda i: segs[i + 1][0] - segs[i][1])
        segs[i:i + 2] = [[segs[i][0], segs[i + 1][1]]]
    while len(segs) < want:  # two figures touch (a blade crossing over): cut at the thinnest column
        i = max(range(len(segs)), key=lambda i: segs[i][1] - segs[i][0])
        x0, x1 = segs[i]
        lo, hi = x0 + (x1 - x0) // 4, x1 - (x1 - x0) // 4
        cut = min(range(lo, hi), key=lambda x: sum(1 for y in range(0, img.height, 2) if alpha.getpixel((x, y))))
        segs[i:i + 1] = [[x0, cut], [cut, x1]]
    out = []
    for x0, x1 in segs:
        part = img.crop((x0, 0, x1, img.height))
        out.append(part.crop(part.getbbox()))
    return out


def feet_x(fig):
    """Horizontal center of the bottom tenth: where the character stands."""
    a = fig.getchannel("A")
    ys = range(int(fig.height * 0.9), fig.height)
    xs = [x for y in ys for x in range(fig.width) if a.getpixel((x, y)) > 0]
    return sum(xs) / len(xs) if xs else fig.width / 2


def pixelate(fig, scale, fx):
    """Place a figure on the 36x48 canvas, feet centered at the bottom."""
    w, h = max(1, round(fig.width * scale)), max(1, round(fig.height * scale))
    small = fig.resize((w, h), Image.BOX)
    a = small.getchannel("A").point(lambda v: 255 if v >= 110 else 0)
    small.putalpha(a)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(small, (round(W / 2 - fx * scale), H - h))
    return canvas


def breathe(c):
    """The upper body sinks one pixel: a slow breath."""
    box = c.getbbox()
    if not box:
        return c.copy()
    cut = box[1] + int((box[3] - box[1]) * 0.55)
    out = c.copy()
    out.paste((0, 0, 0, 0), (0, 0, W, cut + 1))
    out.alpha_composite(c.crop((0, 0, W, cut)), (0, 1))
    return out


def bang(c):
    """A gold '!' with a dark outline in the top-left corner."""
    out = c.copy()
    dots = [(x, y) for x in (2, 3) for y in list(range(1, 7)) + [8, 9]]
    for x, y in dots:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if (x + dx, y + dy) not in dots and 0 <= x + dx < W and 0 <= y + dy < H:
                    out.putpixel((x + dx, y + dy), INK)
    for p in dots:
        out.putpixel(p, GOLD)
    return out


def gif(path, pics, delays):
    big = [p.resize((W * SCALE, H * SCALE), Image.NEAREST) for p in pics]
    big[0].save(path, save_all=True, append_images=big[1:], duration=[d * 10 for d in delays],
                loop=0, disposal=2, optimize=False)


def square(img, size, pad=0.04):
    img = img.crop(img.getbbox())
    side = int(max(img.size) * (1 + pad * 2))
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.alpha_composite(img, ((side - img.width) // 2, (side - img.height) // 2))
    return canvas.resize((size, size), Image.BOX)


def character(name, agents):
    figs = frames(key(Image.open(f"{GEN}/sheet-{name}.png")))
    # Sized by the resting pose; a raised blade may run off the top.
    scale = min((H - 4) / figs[0].height, (W - 1) / max(f.width for f in figs))
    rest, work1, work2, call = [pixelate(f, scale, feet_x(f)) for f in figs]
    gif(f"{agents}/party-sprites/{name}-rest.gif", [rest, breathe(rest)], [150, 60])
    gif(f"{agents}/party-sprites/{name}-working.gif", [work1, work2], [32, 26])
    gif(f"{agents}/party-sprites/{name}-blocked.gif", [bang(call), call], [32, 32])
    # Tab portrait: head and shoulders of the resting pose, at full detail.
    r = figs[0]
    square(r.crop((0, 0, r.width, int(r.height * 0.55))), 256).save(f"{agents}/party-art/{name}.png")


def icon(src, dst):
    square(key(Image.open(src)), 256).save(dst)


def backdrop(src, dst, size, tint, amount):
    img = Image.open(src).convert("RGB")
    tw, th = size
    s = max(tw / img.width, th / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    l, t = (img.width - tw) // 2, (img.height - th) // 2
    img = img.crop((l, t, l + tw, t + th))
    Image.blend(img, Image.new("RGB", img.size, tint), amount).save(dst)


MODS = OUT
AGENTS, SPACES, TABS, CHROME = (f"{MODS}/twilight-fellowship-{m}" for m in ("agents", "spaces", "tabs", "chrome"))
want = lambda n: not ONLY or n in ONLY

HEROES = ["archer", "dwarf", "fingo", "halfling", "healer", "loremaster", "ranger", "smith", "wizard"]
VILLAINS = ["berserker", "darklord", "goblin", "orc", "sorcerer", "spy", "troll", "wraith"]
for n in HEROES + VILLAINS:
    if want(n) and os.path.exists(f"{GEN}/sheet-{n}.png"):
        character(n, AGENTS); print("character", n)
for n in ["valley", "gate", "burrow", "tower"]:
    if want(n) and os.path.exists(f"{GEN}/place-{n}.png"):
        icon(f"{GEN}/place-{n}.png", f"{SPACES}/art/{n}.png"); print("place", n)
for n in ["files", "changes", "inbox"]:
    if want(n) and os.path.exists(f"{GEN}/icon-{n}.png"):
        icon(f"{GEN}/icon-{n}.png", f"{TABS}/art/{n}.png"); print("icon", n)
if want("sidebar") and os.path.exists(f"{GEN}/sidebar.png"):
    backdrop(f"{GEN}/sidebar.png", f"{CHROME}/fellowship-sidebar.png", (460, 1844), (11, 17, 36), 0.25); print("sidebar")
if want("map") and os.path.exists(f"{GEN}/map.png"):
    backdrop(f"{GEN}/map.png", f"{CHROME}/fellowship-map.png", (1658, 1224), (11, 17, 36), 0.25); print("map")
