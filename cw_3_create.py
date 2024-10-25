import os
import numpy as np
path = "/home/jarekj/Dropbox/DYDAKTYKA/struktury_danych/dane"
os.chdir(path)




class layerCreator:
    def __init__(self,type,name,epsg=4326):
        if epsg is not None:
            try:
                crs = QgsCoordinateReferenceSystem("EPSG:{}".format(epsg))
            except: 
                raise ValueError("Wrong epsg format")
        types=('point','polyline','polygon')
        if not any(type.lower()==t for t in types):
            raise ValueError("Unrecoginised geometry type")    
        layer = QgsVectorLayer(type,name,"memory")
        if not layer.isValid():
            raise RuntimeError("Cannot create layers")
        layer.setCrs(crs)
        self.__layer = layer
        self.__init_types()

    def __init_types(self):
        self.__types = {}
        types={}
        self.__types.update(dict.fromkeys(['Int','Integer','Long','Byte'],QVariant.Int))
        self.__types.update(dict.fromkeys(['Real','Double','Double Precision','Numeric'],QVariant.Double))
        self.__types.update(dict.fromkeys(['Date','Datetime','Time'],QVariant.Date))
        self.__types.update(dict.fromkeys(['Text','String','Char','Varchar'],QVariant.String))
        
        self.__qtypes = [QVariant.Int, QVariant.Double, QVariant.Date, QVariant.String]
    
    def add_attribute(self,name,type):
        
        if type not in self.__qtypes:
            try:
                type=self.__types[type.title()]
            except:
                raise: TypeError("Unrecoginzed type")
                return None
        
        layer.dataProvider().addAttribute(QgsField(name,type))
        layer.updateFields() 

    
    def __nested_level(self,geometry):
        try:
            geometry[0][0][0]
            return 2
        except:
            pass
        try:
            geometry[0][0]
            return 1
        except:
            pass
        try:
            geometry[0]
            return 0
        except:
            raise TypeError("Geometry is a sequence")
        
    
    def __point(self,geometry):
        if self.__nested_level(geometry) != 0:
            raise ValueError("Incorect geometry format")
        
        try:
            point = QgsPointXY(*geometry)
        except: 
            raise ValueError("Incorect point geometry")
        return point

    def __line(self,geometry):
        if self.__nested_level(geometry) != 1:
            raise ValueError("Incorect geometry format")
        try:
            line = [QgsPointXY(*point) for point in geometry]
        except: 
            raise ValueError("Incorect line geometry")
        return line
        
        return 

    def __parse_point(self,geometry):
            point = self.__point(geometry)
            return QgsGeometry.fromPointXY(point)
   
    def __parse_linestring(self,geometry):
        line = self.__line(geometry)
        return QgsGeometry.fromPolylineXY(line)
        
       
    def __parse_polygon(self,geometry):
        if self.__nested_level(geometry) = 0:
            raise "Not a polygon"
        
        polygon = []
        if self.__nested_level ==2:
            for rg in geometry:
                ring = self.__line(rg)
                polygon.append(ring)
        else:
            ring = self.__line(geometry)
            polygon.append(ring)
    
    def __parse_geometry(self,geometry):
        if self.layer.geometryType == QgsWkbTypes.PointGeometry:
            geometry = self.__parse_point(self,geometry)
        elif self.layer.geometryType == QgsWkbTypes.LineGeometry:
            geometry = self.__parse_line(self,geometry)
        elif self.layer.geometryType == QgsWkbTypes.LineGeometry:
            geometry = self.__parse_polygon(self,geometry)
        else:
            raise TypeError("Unknown geometry")
            return None
        return geometry
        
        
    def add_feature(self,geometry,**attributes):
         geometry = self.__parse_geometry(geometry)
        feature = QgsFeature()
        feature.setGeometry(geometry)
        fields=[field.name() for field in layer.fields()]
        attrValues=[] #2
        for field in fields:
            try: 
                value=attributes[field]
            except:
                value=None 
        attrValues.append(value)
        feature.setAttributes(attrValues)
        self.__layer.dataProvider().addFeature(feature)
        self.__layer.updateExtents()

    def write_layer(self,filename):
        write = QgsVectorFileWriter.writeAsVectorFormat(self.__layer, \
                    filename, "UTF-8",driverName="GPKG")
        return 0
