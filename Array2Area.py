import numpy as np
import matplotlib.pyplot as plt
import geopandas as gp

def Array2gdf(x, y, z, levels):
    # x, y是1-D数组或列表，保存数据的坐标信息
    # z是2-D数组或列表，保存数据的变量信息。z的维度长度必须与x和y相等，即z.shape==[len(x), len(y)]
    # levels是1-D列表，应包含至少2个数值元素并从小向大排列，每个数值均表示面积计算的等值边界
    shps = []
    lev = []
    cnf = plt.contourf(x, y, z, levels=levels)
    segs = cnf.allsegs
    levnum = 1
    for level in segs:
        poly = []
        for elem in level:
            lons = elem[:, 0]
            lats = elem[:, 1]
            if len(lons) < 3 or len(lats) < 3:
                continue
            p = [(i[0],i[1]) for i in zip(lons, lats)]
            poly.append(Polygon(p))
            lev.append(levnum)
        shps = shps+poly
        levnum = levnum+1
    gdf = gp.GeoDataFrame({'geometry':shps, 'level':lev}, crs='EPSG:4326')    #地理坐标系设置为WGS84
    plt.close()   #这条命令会导致绘图窗口关闭，因此应该在调用此函数后再创建figure和画图
    return gdf

def Array2Area(x, y, z, levels, projection='World_Cylindrical_Equal_Area')
    # x, y是1-D数组或列表，保存数据的坐标信息
    # z是3-D数组或列表，保存数据的变量信息。z的第一个维度是时间维度，后两个维度是空间维度且长度必须分别与x和y相等
    # levels是1-D列表，应包含至少2个数值元素并从小向大排列，每个数值均表示面积计算的等值边界
    area = []
    for i in np.arange(0, z.shape[0], 1):
        gdf = Array2Shp(x, y, z[i, :, :], levels)
        gdf_proj = gdf.to_crs(projection)
        # area.append(gdf_proj.area.sum()/1e12)
        area_lev = []
        for j in range(1, len(levels), 1):
            area_lev.append(gdf_proj.loc[gdf_proj['level']==j].area.sum()/1e12)
        area.append(area_lev)   #[70, 4]
        del(gdf, gdf_proj)
    area = np.array(area, dtype=np.float32)
    area_year = area #干旱区总面积的年变化序列
    return area_year
