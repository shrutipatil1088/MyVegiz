def point_in_polygon(lat: float, lng: float, polygon: list[dict]) -> bool:
    """
    Ray Casting Algorithm
    polygon = [{"lat": float, "lng": float}, ...]
    """
    x = lng
    y = lat

    inside = False
    n = len(polygon)

    for i in range(n):
        j = (i - 1) % n
        xi = polygon[i]["lng"]
        yi = polygon[i]["lat"]
        xj = polygon[j]["lng"]
        yj = polygon[j]["lat"]

        intersect = ((yi > y) != (yj > y)) and \
                    (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi)
        if intersect:
            inside = not inside

    return inside
