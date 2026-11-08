from PIL import Image
import sys
for p in sys.argv[1:]:
    img = Image.open(p).convert("RGB")
    w, h = img.size
    for (x1, y1, x2, y2) in [(0, int(h*0.90), int(w*0.25), h),
                            (int(w*0.75), int(h*0.90), w, h)]:
        img.paste((255, 255, 255), (x1, y1, x2, y2))
    img.save(p, "JPEG", quality=88, optimize=True)
    print("done", p)
