# encoding: utf-8

import json
from osgeo import ogr, osr
import matplotlib.pyplot as plt
import numpy as np


def get_contour_points(polygon):
    ## 获取轮廓点 ##
    geom = polygon.GetGeometryRef()
    points = json.loads(geom.ExportToJson())["coordinates"]
    pts = np.array(points)
    pts = np.squeeze(pts)
    if len(pts.shape) < 3:
        pts = np.expand_dims(pts, axis=0)
    points = pts.tolist()
    return points


def disp_polygon(polygon):
    ## 显示线矢量文件 ##
    points = get_contour_points(polygon)
    for i, obj in enumerate(points):
        for j, pt in enumerate(obj):
            if j == 0:
                x = pt[0]
                y = pt[1]
            else:
                plt.plot([x, pt[0]], [y, pt[1]], "k-")
                x = pt[0]
                y = pt[1]


def create_polygon():
    ## 生成线矢量文件 ##
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_source = driver.CreateDataSource("Polygon.shp")  ## shp文件名称
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)  ## 空间参考：WGS84
    layer = data_source.CreateLayer("Polygon", srs, ogr.wkbPolygon)  ## 图层名称要与shp名称一致
    field_name = ogr.FieldDefn("Name", ogr.OFTString)  ## 设置属性
    field_name.SetWidth(20)  ## 设置长度
    layer.CreateField(field_name)  ## 创建字段
    field_length = ogr.FieldDefn("Area", ogr.OFTReal)  ## 设置属性
    layer.CreateField(field_length)  ## 创建字段
    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetField("Name", "polygon")  ## 设置字段值
    feature.SetField("Area", "500")  ## 设置字段值

    fig = plt.figure()

    wkt = "POLYGON((100 50, 100 60, 90 60, 90 50, 100 50))"  ## 创建面
    polygon = ogr.CreateGeometryFromWkt(wkt)  ## 生成面
    feature.SetGeometry(polygon)  ## 设置面
    layer.CreateFeature(feature)  ## 添加面
    disp_polygon(feature)

    wkt = "POLYGON((105 55, 105 65, 95 65, 95 55, 105 55))"  ## 创建面
    polygon = ogr.CreateGeometryFromWkt(wkt)  ## 生成面
    feature.SetGeometry(polygon)  ## 设置面
    layer.CreateFeature(feature)  ## 添加面
    disp_polygon(feature)

    wkt = "POLYGON((50 30, 50 40, 40 40, 40 30, 50 30))"  ## 创建面
    polygon = ogr.CreateGeometryFromWkt(wkt)  ## 生成面
    feature.SetGeometry(polygon)  ## 设置面
    layer.CreateFeature(feature)  ## 添加面
    disp_polygon(feature)

    wkt = "POLYGON((55 35, 55 45, 45 45, 45 35, 55 35))"  ## 创建面
    polygon = ogr.CreateGeometryFromWkt(wkt)  ## 生成面
    feature.SetGeometry(polygon)  ## 设置面
    layer.CreateFeature(feature)  ## 添加面
    disp_polygon(feature)

    feature = None  ## 关闭属性
    data_source = None  ## 关闭数据


def read_polygon():
    ## 读取线矢量文件 ##
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource = driver.Open("Polygon.shp", 1)  ## 打开文件
    layer = dataSource.GetLayer()  ## 获取图层

    out_ds = driver.CreateDataSource("Polygon_out.shp")  ## 创建文件
    out_layer = out_ds.CreateLayer(
        "Polygon_out", layer.GetSpatialRef(), ogr.wkbPolygon
    )  ## 创建图层
    def_feat = layer.GetLayerDefn()  ## 获取属性
    print("the length of layer is:", len(layer))  ## 获取属性个数
    fig = plt.figure()

    for i, feature in enumerate(layer):
        geometry = feature.GetGeometryRef()  ## 获取面
        print("the geometry is:", geometry)  ## 获取面
        if i == 0:
            current_union = geometry.Clone()  ## 克隆面
        else:
            current_union = current_union.Union(geometry).Clone()  ## 合并面
            # current_union = current_union.Difference(geometry).Clone()  ## 合并面

    print(current_union)
    out_feature = ogr.Feature(def_feat)  ## 创建属性
    out_feature.SetGeometry(current_union)  ## 设置属性

    disp_polygon(out_feature)

    out_layer.ResetReading()  ## 添加属性
    out_layer.CreateFeature(out_feature)  ## 添加属性


if __name__ == "__main__":
    create_polygon()
    read_polygon()
    plt.show()
