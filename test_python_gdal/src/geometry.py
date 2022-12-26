from osgeo import ogr


def test_point():
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(1198054.34, 648493.09)
    print(point.ExportToWkt())


def test_line():
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(1116651.439379124, 637392.6969887456)
    line.AddPoint(1188804.0108498496, 652655.7409537067)
    line.AddPoint(1226730.3625203592, 634155.0816022386)
    line.AddPoint(1281307.30760719, 636467.6640211721)
    print(line.ExportToWkt())


def test_polygon():
    # Create ring
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(1179091.1646903288, 712782.8838459781)
    ring.AddPoint(1161053.0218226474, 667456.2684348812)
    ring.AddPoint(1214704.933941905, 641092.8288590391)
    ring.AddPoint(1228580.428455506, 682719.3123998424)
    ring.AddPoint(1218405.0658121984, 721108.1805541387)
    ring.AddPoint(1179091.1646903288, 712782.8838459781)

    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)

    print(poly.ExportToWkt())


def test_polygon_hole():
    # Create outer ring
    outRing = ogr.Geometry(ogr.wkbLinearRing)
    outRing.AddPoint(1154115.274565847, 686419.4442701361)
    outRing.AddPoint(1154115.274565847, 653118.2574374934)
    outRing.AddPoint(1165678.1866605144, 653118.2574374934)
    outRing.AddPoint(1165678.1866605144, 686419.4442701361)
    outRing.AddPoint(1154115.274565847, 686419.4442701361)

    # Create inner ring
    innerRing = ogr.Geometry(ogr.wkbLinearRing)
    innerRing.AddPoint(1149490.1097279799, 691044.6091080031)
    innerRing.AddPoint(1149490.1097279799, 648030.5761158396)
    innerRing.AddPoint(1191579.1097525698, 648030.5761158396)
    innerRing.AddPoint(1191579.1097525698, 691044.6091080031)
    innerRing.AddPoint(1149490.1097279799, 691044.6091080031)

    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(outRing)
    poly.AddGeometry(innerRing)

    print(poly.ExportToWkt())


def test_multi_point():
    multipoint = ogr.Geometry(ogr.wkbMultiPoint)

    point1 = ogr.Geometry(ogr.wkbPoint)
    point1.AddPoint(1251243.7361610543, 598078.7958668759)
    multipoint.AddGeometry(point1)

    point2 = ogr.Geometry(ogr.wkbPoint)
    point2.AddPoint(1240605.8570339603, 601778.9277371694)
    multipoint.AddGeometry(point2)

    point3 = ogr.Geometry(ogr.wkbPoint)
    point3.AddPoint(1250318.7031934808, 606404.0925750365)
    multipoint.AddGeometry(point3)

    print(multipoint.ExportToWkt())


def test_multi_line():
    multiline = ogr.Geometry(ogr.wkbMultiLineString)

    line1 = ogr.Geometry(ogr.wkbLineString)
    line1.AddPoint(1214242.4174581182, 617041.9717021306)
    line1.AddPoint(1234593.142744733, 629529.9167643716)
    multiline.AddGeometry(line1)

    line1 = ogr.Geometry(ogr.wkbLineString)
    line1.AddPoint(1184641.3624957693, 626754.8178616514)
    line1.AddPoint(1219792.6152635587, 606866.6090588232)
    multiline.AddGeometry(line1)

    print(multiline.ExportToWkt())


def test_multi_polygon():
    multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)

    # Create ring #1
    ring1 = ogr.Geometry(ogr.wkbLinearRing)
    ring1.AddPoint(1204067.0548148106, 634617.5980860253)
    ring1.AddPoint(1204067.0548148106, 620742.1035724243)
    ring1.AddPoint(1215167.4504256917, 620742.1035724243)
    ring1.AddPoint(1215167.4504256917, 634617.5980860253)
    ring1.AddPoint(1204067.0548148106, 634617.5980860253)

    # Create polygon #1
    poly1 = ogr.Geometry(ogr.wkbPolygon)
    poly1.AddGeometry(ring1)
    multipolygon.AddGeometry(poly1)

    # Create ring #2
    ring2 = ogr.Geometry(ogr.wkbLinearRing)
    ring2.AddPoint(1179553.6811741155, 647105.5431482664)
    ring2.AddPoint(1179553.6811741155, 626292.3013778647)
    ring2.AddPoint(1194354.20865529, 626292.3013778647)
    ring2.AddPoint(1194354.20865529, 647105.5431482664)
    ring2.AddPoint(1179553.6811741155, 647105.5431482664)

    # Create polygon #2
    poly2 = ogr.Geometry(ogr.wkbPolygon)
    poly2.AddGeometry(ring2)
    multipolygon.AddGeometry(poly2)

    print(multipolygon.ExportToWkt())


def test_geometry_collection():
    # Create a geometry collection
    geomcol = ogr.Geometry(ogr.wkbGeometryCollection)

    # Add a point
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(-122.23, 47.09)
    geomcol.AddGeometry(point)

    # Add a line
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(-122.60, 47.14)
    line.AddPoint(-122.48, 47.23)
    geomcol.AddGeometry(line)

    print(geomcol.ExportToWkt())


def test_geometry_from_wtk():
    wkt = "POINT (1120351.5712494177 741921.4223245403)"
    point = ogr.CreateGeometryFromWkt(wkt)
    print("%d,%d" % (point.GetX(), point.GetY()))


def test_geometry_from_json():
    geojson = """{"type":"Point","coordinates":[108420.33,753808.59]}"""
    point = ogr.CreateGeometryFromJson(geojson)
    print("%d,%d" % (point.GetX(), point.GetY()))


def test_geometry_from_gml():
    gml = """<gml:Point xmlns:gml="http://www.opengis.net/gml"><gml:coordinates>108420.33,753808.59</gml:coordinates></gml:Point>"""
    point = ogr.CreateGeometryFromGML(gml)
    print("%d,%d" % (point.GetX(), point.GetY()))


def test_count_points():
    wkt = "LINESTRING (1181866.263593049 615654.4222507705, 1205917.1207499576 623979.7189589312, 1227192.8790041457 643405.4112779726, 1224880.2965852122 665143.6860159477)"
    geom = ogr.CreateGeometryFromWkt(wkt)
    print("Geometry has %i points" % (geom.GetPointCount()))


def test_count_geometries():
    wkt = "MULTIPOINT (1181866.263593049 615654.4222507705, 1205917.1207499576 623979.7189589312, 1227192.8790041457 643405.4112779726, 1224880.2965852122 665143.6860159477)"
    geom = ogr.CreateGeometryFromWkt(wkt)
    print("Geometry has %i geometries" % (geom.GetGeometryCount()))


def test_geometry_iter():
    wkt = "MULTIPOINT (1181866.263593049 615654.4222507705, 1205917.1207499576 623979.7189589312, 1227192.8790041457 643405.4112779726, 1224880.2965852122 665143.6860159477)"
    geom = ogr.CreateGeometryFromWkt(wkt)
    for i in range(0, geom.GetGeometryCount()):
        g = geom.GetGeometryRef(i)
        print("%i). %s" % (i, g.ExportToWkt()))


def test_geometry_get_point():
    wkt = "LINESTRING (1181866.263593049 615654.4222507705, 1205917.1207499576 623979.7189589312, 1227192.8790041457 643405.4112779726, 1224880.2965852122 665143.6860159477)"
    geom = ogr.CreateGeometryFromWkt(wkt)
    for i in range(0, geom.GetPointCount()):
        # GetPoint returns a tuple not a Geometry
        pt = geom.GetPoint(i)
        print("%i). POINT (%d %d)" % (i, pt[0], pt[1]))


def test_geometry_buffer():
    wkt = "POINT (1198054.34 648493.09)"
    pt = ogr.CreateGeometryFromWkt(wkt)
    bufferDistance = 500
    poly = pt.Buffer(bufferDistance)
    print(
        "%s buffered by %d is %s"
        % (pt.ExportToWkt(), bufferDistance, poly.ExportToWkt())
    )


def test_geometry_envelope():
    wkt = "LINESTRING (1181866.263593049 615654.4222507705, 1205917.1207499576 623979.7189589312, 1227192.8790041457 643405.4112779726, 1224880.2965852122 665143.6860159477)"
    geom = ogr.CreateGeometryFromWkt(wkt)
    # Get Envelope returns a tuple (minX, maxX, minY, maxY)
    env = geom.GetEnvelope()
    print("minX: %d, minY: %d, maxX: %d, maxY: %d" % (env[0], env[2], env[1], env[3]))


def test_geometry_get_area():
    wkt = "POLYGON ((1162440.5712740074 672081.4332727483, 1162440.5712740074 647105.5431482664, 1195279.2416228633 647105.5431482664, 1195279.2416228633 672081.4332727483, 1162440.5712740074 672081.4332727483))"
    poly = ogr.CreateGeometryFromWkt(wkt)
    print("Area = %d" % poly.GetArea())


def test_geometry_get_length():
    wkt = "LINESTRING (1181866.263593049 615654.4222507705, 1205917.1207499576 623979.7189589312, 1227192.8790041457 643405.4112779726, 1224880.2965852122 665143.6860159477)"
    geom = ogr.CreateGeometryFromWkt(wkt)
    print("Length = %d" % geom.Length())


def test_geometry_get_type():
    wkts = [
        "POINT (1198054.34 648493.09)",
        "LINESTRING (1181866.263593049 615654.4222507705, 1205917.1207499576 623979.7189589312, 1227192.8790041457 643405.4112779726, 1224880.2965852122 665143.6860159477)",
        "POLYGON ((1162440.5712740074 672081.4332727483, 1162440.5712740074 647105.5431482664, 1195279.2416228633 647105.5431482664, 1195279.2416228633 672081.4332727483, 1162440.5712740074 672081.4332727483))",
    ]

    for wkt in wkts:
        geom = ogr.CreateGeometryFromWkt(wkt)
        print(geom.GetGeometryName())


def test_geometry_intersection():
    wkt1 = "POLYGON ((1208064.271243039 624154.6783778917, 1208064.271243039 601260.9785661874, 1231345.9998651114 601260.9785661874, 1231345.9998651114 624154.6783778917, 1208064.271243039 624154.6783778917))"
    wkt2 = "POLYGON ((1199915.6662253144 633079.3410163528, 1199915.6662253144 614453.958118695, 1219317.1067437078 614453.958118695, 1219317.1067437078 633079.3410163528, 1199915.6662253144 633079.3410163528)))"

    poly1 = ogr.CreateGeometryFromWkt(wkt1)
    poly2 = ogr.CreateGeometryFromWkt(wkt2)

    intersection = poly1.Intersection(poly2)

    print(intersection.ExportToWkt())


def test_geometry_union():
    wkt1 = "POLYGON ((1208064.271243039 624154.6783778917, 1208064.271243039 601260.9785661874, 1231345.9998651114 601260.9785661874, 1231345.9998651114 624154.6783778917, 1208064.271243039 624154.6783778917))"
    wkt2 = "POLYGON ((1199915.6662253144 633079.3410163528, 1199915.6662253144 614453.958118695, 1219317.1067437078 614453.958118695, 1219317.1067437078 633079.3410163528, 1199915.6662253144 633079.3410163528)))"

    poly1 = ogr.CreateGeometryFromWkt(wkt1)
    poly2 = ogr.CreateGeometryFromWkt(wkt2)

    union = poly1.Union(poly2)

    print(poly1)
    print(poly2)
    print(union.ExportToWkt())


def test_geometry_json():
    # Create test polygon
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(1179091.1646903288, 712782.8838459781)
    ring.AddPoint(1161053.0218226474, 667456.2684348812)
    ring.AddPoint(1214704.933941905, 641092.8288590391)
    ring.AddPoint(1228580.428455506, 682719.3123998424)
    ring.AddPoint(1218405.0658121984, 721108.1805541387)
    ring.AddPoint(1179091.1646903288, 712782.8838459781)
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)

    geojson = poly.ExportToJson()
    print(geojson)


def test_geometry_to_wtk():
    # Create test polygon
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(1179091.1646903288, 712782.8838459781)
    ring.AddPoint(1161053.0218226474, 667456.2684348812)
    ring.AddPoint(1214704.933941905, 641092.8288590391)
    ring.AddPoint(1228580.428455506, 682719.3123998424)
    ring.AddPoint(1218405.0658121984, 721108.1805541387)
    ring.AddPoint(1179091.1646903288, 712782.8838459781)
    geom_poly = ogr.Geometry(ogr.wkbPolygon)
    geom_poly.AddGeometry(ring)

    # Export geometry to WKT
    wkt = geom_poly.ExportToWkt()
    print(wkt)


def test_geometry_to_wkb():
    # Create test polygon
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(1179091.1646903288, 712782.8838459781)
    ring.AddPoint(1161053.0218226474, 667456.2684348812)
    ring.AddPoint(1214704.933941905, 641092.8288590391)
    ring.AddPoint(1228580.428455506, 682719.3123998424)
    ring.AddPoint(1218405.0658121984, 721108.1805541387)
    ring.AddPoint(1179091.1646903288, 712782.8838459781)
    geom_poly = ogr.Geometry(ogr.wkbPolygon)
    geom_poly.AddGeometry(ring)

    # Export geometry to WKT
    wkb = geom_poly.ExportToWkb()
    print(wkb)


def test_geometry_to_kml():
    # Create test polygon
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(1179091.1646903288, 712782.8838459781)
    ring.AddPoint(1161053.0218226474, 667456.2684348812)
    ring.AddPoint(1214704.933941905, 641092.8288590391)
    ring.AddPoint(1228580.428455506, 682719.3123998424)
    ring.AddPoint(1218405.0658121984, 721108.1805541387)
    ring.AddPoint(1179091.1646903288, 712782.8838459781)
    geom_poly = ogr.Geometry(ogr.wkbPolygon)
    geom_poly.AddGeometry(ring)

    kml = geom_poly.ExportToKML()
    print(kml)


def test_polygon_to_multi_polygon():
    # Given a test polygon
    poly_wkt = "POLYGON ((1179091.164690328761935 712782.883845978067257,1161053.021822647424415 667456.268434881232679,1214704.933941904921085 641092.828859039116651,1228580.428455505985767 682719.312399842427112,1218405.065812198445201 721108.180554138729349,1179091.164690328761935 712782.883845978067257))"
    geom_poly = ogr.CreateGeometryFromWkt(poly_wkt)

    # Force a polygon to multipolygon
    if geom_poly.GetGeometryType() == ogr.wkbPolygon:
        geom_poly = ogr.ForceToMultiPolygon(geom_poly)
        # if are iterating over features just to update the geometry
        # to multipolygon you can update the geometry using "feature.SetGeometryDirectly(geom_poly)"

    # Then export geometry to WKT
    wkt = geom_poly.ExportToWkt()
    print(wkt)


def main():
    # test_point()
    # test_line()
    # test_polygon()
    # test_polygon_hole()
    # test_multi_point()
    # test_multi_line()
    # test_multi_polygon()
    # test_geometry_collection()
    # test_geometry_from_wtk()
    # test_geometry_from_json()
    # test_geometry_from_gml()
    # test_count_points()
    # test_count_geometries()
    # test_geometry_iter()
    # test_geometry_get_point()
    # test_geometry_buffer()
    # test_geometry_envelope()
    # test_geometry_get_area()
    # test_geometry_get_length()
    # test_geometry_get_type()
    # test_geometry_intersection()
    # test_geometry_union()
    # test_geometry_json()
    # test_geometry_to_wtk()
    # test_geometry_to_kml()
    test_geometry_to_wkb()
    # test_polygon_to_multi_polygon()


if __name__ == "__main__":
    main()
