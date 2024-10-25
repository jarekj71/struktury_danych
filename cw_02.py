from osgeo import ogr, osr
import os
import numpy as np

os.chdir(os.path.join(os.path.expanduser("~"),"Documents"))

poligonfile = "poligony.gpkg"
poligons = ogr.Open(poligonfile)
poligons is None
layer = poligons.GetLayer()

layer.GetFeatureCount()

f1 = layer.GetFeature(1)
f2 = layer.GetFeature(2)


g1 = f1.GetGeometryRef()
g1.GetGeometryCount()

g2 = f2.GetGeometryRef()
g2.GetGeometryCount()

g10 = g1.GetGeometryRef(0)

g20 = g2.GetGeometryRef(0)
g21 = g2.GetGeometryRef(1)
 ######
 
 
 p1 = (510989,356021)
 p2 = (511001,353451)
 
driver = ogr.GetDriverByName("GPKG")
proj = osr.SpatialReference()
proj.ImportFromEPSG(2180)
file = driver.CreateDataSource("dwapunkty.gpkg")
layer = file.CreateLayer("moje dwa punkty",proj,ogr.wkbPoint)
## Layer definition
fd = ogr.FieldDefn("Nazwa",ogr.OFTString)
layer.CreateField(fd)
fd = ogr.FieldDefn("Wsokość",ogr.OFTReal)
layer.CreateField(fd)
##
ld = layer.GetLayerDefn()

f = ogr.Feature(ld)
geom = ogr.Geometry(ogr.wkbPoint)
geom.AddPoint(*p1)

f.SetGeometry(geom)
f.SetField("Nazwa","słupek 1")
f.SetField("Wysokość",1.78)
layer.CreateFeature(f)
f = None


f = ogr.Feature(ld)
geom = ogr.Geometry(ogr.wkbPoint)
geom.AddPoint(*p2)

f.SetGeometry(geom)
f.SetField("Nazwa","słupek 2")
f.SetField("Wysokość",1.64)
layer.CreateFeature(f)
f = None

file = None


x = np.array([1,2,3])
y = np.array([4,5,6])
t = np.array([x,y])

for k in t.T:
    print(*k)

addPoint(layer,k):
    ......
    return ?

for k in t.T:
    addPoint(layer,k)

file = None


#funkcje    

def scale(x,mx,mn):
    x = (x-x.min())/(x.max()-x.min())
    return (x*(mx-mn))+mn


def addPoint(layer,point):
    ld = layer.GetLayerDefn()
    f = ogr.Feature(ld)
    geom = ogr.Geometry(ogr.wkbPoint)
    geom.AddPoint(*point)
    f.SetGeometry(geom)
    layer.CreateFeature(f)
    f = None

#dane

w=500000
e=501000
n=306000
s=305000
npoints = 100
x = np.random.lognormal(size=npoints)
y = np.random.uniform(size=npoints)
data = np.array([scale(x,e,w),scale(y,n,s)])

# rozwiązanie
driver = ogr.GetDriverByName("GPKG")
proj = osr.SpatialReference()
proj.ImportFromEPSG(2180)
file = driver.CreateDataSource("deszcz.gpkg")
layer = file.CreateLayer("deszcz z wiatrem",proj,ogr.wkbPoint)

for point in data.T:
    addPoint(layer,point)

file = None

########
def createCircle(x,y,radius,res=36):
    alpha = np.linspace(0,2*np.pi,res)
    ya = np.sin(alpha)*radius+y
    xa = np.cos(alpha)*radius+x
    return np.array([xa,ya])

driver = ogr.GetDriverByName("GPKG")
proj = osr.SpatialReference()
proj.ImportFromEPSG(2180)
file = driver.CreateDataSource("kolko.gpkg")
layer = file.CreateLayer("kolko z dziurką",proj,ogr.wkbPolygon)
ld = layer.GetLayerDefn()

######## Otuer ring
x=500100
y=350500
polygon = ogr.Geometry(ogr.wkbPolygon)

outer_ring_dane = createCircle(x,y,10000)
outer_ring = ogr.Geometry(ogr.wkbLinearRing)
for point in outer_ring_dane.T:
    outer_ring.AddPoint(*point)
polygon.AddGeometry(outer_ring)

inner_ring_dane = createCircle(x,y,3000)
inner_ring = ogr.Geometry(ogr.wkbLinearRing)
for point in inner_ring_dane.T:
    inner_ring.AddPoint(*point)
polygon.AddGeometry(inner_ring)
    
f = ogr.Feature(ld)
f.SetGeometry(polygon)
layer.CreateFeature(f)
f = None
file = None
