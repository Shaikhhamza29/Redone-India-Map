import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from PIL import Image, ImageDraw

# 1. Load India shapefile
shapefile_path = r"D:\Projects\India_map_hostpots\in_shp\in.shp"
states = gpd.read_file(shapefile_path).to_crs(epsg=4326)

# Merge all states into a single India shape (no deprecation)
india_shape = states.union_all()   # returns a single (Multi)Polygon

# 2. Load your collage image  <-- make sure this path & filename are correct
image_path = r"D:\Projects\India_map_hostpots\trryyy.jpg"
img = Image.open(image_path).convert("RGBA")
width, height = img.size

# 3. Compute bounds of India geometry
minx, miny, maxx, maxy = india_shape.bounds
bbox_w = maxx - minx
bbox_h = maxy - miny

# Use UNIFORM scale to avoid distortion
scale = min(width / bbox_w, height / bbox_h)

# Center India in the image
x_offset = (width - scale * bbox_w) / 2.0
y_offset = (height - scale * bbox_h) / 2.0

# 4. Create a blank mask (grayscale: 0 = transparent, 255 = opaque)
mask = Image.new("L", (width, height), 0)
draw = ImageDraw.Draw(mask)


def draw_geom(geom):
    """Draw Polygon or MultiPolygon onto the mask."""
    if geom.is_empty:
        return

    # Normalize to list of Polygons
    if geom.geom_type == "Polygon":
        polys = [geom]
    elif geom.geom_type == "MultiPolygon":
        polys = list(geom.geoms)
    else:
        # If GeometryCollection etc., draw only polygon parts
        polys = [g for g in geom.geoms if g.geom_type in ("Polygon", "MultiPolygon")] \
                if hasattr(geom, "geoms") else []

    for poly in polys:
        if poly.is_empty:
            continue

        # Exterior ring
        exterior = []
        for x, y in poly.exterior.coords:
            px = (x - minx) * scale + x_offset
            py = height - ((y - miny) * scale + y_offset)  # invert Y
            exterior.append((px, py))

        draw.polygon(exterior, fill=255, outline=255)

        # Interior holes (if any)
        for interior in poly.interiors:
            hole = []
            for x, y in interior.coords:
                px = (x - minx) * scale + x_offset
                py = height - ((y - miny) * scale + y_offset)
                hole.append((px, py))
            draw.polygon(hole, fill=0, outline=0)


# 5. Draw India shape onto mask
draw_geom(india_shape)

# 6. Apply mask to original image
result = Image.new("RGBA", (width, height))
result.paste(img, (0, 0), mask)

# 7. Save and show
output_path = r"D:\Projects\India_map_hostpots\media\india_masked.png"
result.save(output_path)
result.show()

print("Saved:", output_path)
