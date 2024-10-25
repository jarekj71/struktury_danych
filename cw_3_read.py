import os
path = "/home/jarekj/Dropbox/DYDAKTYKA/struktury_danych/dane"
os.chdir(path)


class c_vectorLayer:
    def __init__(self,fileName):
        file = QgsVectorLayer(fileName)
        if not file.isValid():
            raise ValueError("Plik nie znaleziony lub błędny typ danych")
        self.__file = file

    def describe_layer(self):
        print(self.__file.featureCount())
        print(self.__file.geometryType())
        print(self.__file.fields().count())
        
    def print_fields(self):
        for field in self.__file.fields():
            field_desc = "{}:{}".format(field.name(),field.typeName())
            print(field_desc)
    
    def list_fields_names(self):
        return [field.name() for field in self.__file.fields()]
        
    def print_attributes_values(self,geometry=False):
        features = self.__file.getFeatures()
        for feature in features:
            id = feature.id()
            attr = feature.attributes()
            if geometry:
                geom = feature.geometry().asWkt()
                print("ID: {} attrs: {} coords: {} ".format(id, attr, geom))
            else:
                print("ID: {} attrs: {}".format(id, attr))

o = c_vectorLayer("punkty.gpkg")
p = o.print_attributes_values(geometry=True)


