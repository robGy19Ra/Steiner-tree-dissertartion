# -*- coding: utf-8 -*-

from discord_webhook import DiscordWebhook
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import approximation as apx
import csv
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import approximation as apx
from qgis.utils import iface
from PyQt5.QtGui import *
from qgis.PyQt.QtCore import QVariant
from qgis.core import *
from qgis.core import (
   edit,
   QgsExpression,
   QgsExpressionContext,
   QgsFeature,
   QgsFeatureRequest,
   QgsField,
   QgsFields,
   QgsVectorLayer,
   QgsPointXY,
   QgsGeometry,
   QgsProject,
   QgsExpressionContextUtils,
   Qgis
)



def to_discord(to_message):     #function to push message variable to discord via webhook
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/991728785042972752/N0iWYwWjdPtQgMoXxTQR9mZu6jKpzuwj1QteJEbIl3H5uE0hoBfXlVDSOtwQW-fOko3G', content=to_message, rate_limit_retry=True)
    response = webhook.execute()


class HaltException(Exception):
    #script adapted from https://stackoverflow.com/questions/28413104/stop-python-script-without-killing-the-python-process
    pass

try:
    to_discord(to_message="start") #first message to discord
except:
    pass


try:            #majority of script within try: Except: HaltException() to exit script if required, without closing QGIS 
    class attributes():
        
        def concat(string_list):     #function to concat string attributes in list, skipping any null values
            for a in string_list:
                if a == None:
                    string_list.remove(a)
            b = ''.join(string_list)
            return b
        
        def unique_list(x):     #function to remove duplicates of a string by turning list items to dictionary keys and the converting back to a list.
            return list(dict.fromkeys(x))
        
        def headers(layer, fields):     #function to set attributes for a QGIS layer.
            _ = layer.startEditing()
            _ = dprov = layer.dataProvider()
            _ = dprov.addAttributes(fields)
            
            _ = layer.updateFields()
            _ = layer.commitChanges()
            _ = layer.triggerRepaint()
    
    
    class GUI():
        
        def infoBar(message):
            def showError():
                pass
            
            widget = iface.messageBar().createMessage(message, "Show Me")
            button.setText("Show Me")
            button.pressed.connect(showError)
            widget.layout().addWidget(button)
            iface.messageBar().pushWidget(widget, Qgis.Warning)
    
    class networkArc():
        
        def construct(layer_grid, feature, searchCrit):
            #function to take in: grid_layer, grid feature (from which arcs are
            #to be constructed), and the search neighbourhood figure. Each grid
            #feature iterates through all grid features and is tested to ensure
            #only one edge is created between a pair of nodes.
            #The aim of the function is to only draw to the same or a decreasing
            #latitute. if the line is to be drawn horizontal then only
            #draw to an increased longitude. If the search criteria
            #is >1 then no edge lines should overlap.
            
            featureList = []                #list of features to be populated by edges which pass all tests.
            features1 = layer_grid.getFeatures(QgsFeatureRequest())     #grid features to be iterated through
            row0 = feature.attribute(layer_grid.fields().indexFromName('row'))
            col0 = feature.attribute(layer_grid.fields().indexFromName('column'))
            for feature1 in features1:
                row1 = feature1.attribute(layer_grid.fields().indexFromName('row'))
                col1 = feature1.attribute(layer_grid.fields().indexFromName('column'))
                if feature1.attribute(layer_grid.fields().indexFromName('cost')) != 'NA':
                    #if the test feature has a cost then
                    if int(row0) != int(row1) or int(col0) != int(col1):
                        #if the row AND column are not the same (self connection) then
                        if int(row0) <= int(row1):
                            #if the line is drawn north to south OR horizontal then
                            if int(row0) != int(row1) or int(col0) <= int(col1):
                                #if the line is NOT horizontal OR the column is drawn vertically or is west to east then
                                if int(row0) - int(row1) <= int(searchCrit) and int(row1) - int(row0) <= int(searchCrit):
                                    #if the rows are equal to or less than the search criteria distance apart then
                                    if int(col0) - int(col1) <= int(searchCrit) and int(col1) - int(col0) <= int(searchCrit):
                                        #if the columns are equal to or less than the search criteria distance apart then
                                        r_check = (int(row1)-int(row0))/2       #used to find half the difference between rows
                                        c_check = (int(col1)-int(col0))/2       #used to find half the difference between columns
                                        if float(abs(r_check)) != int(abs(r_check)) or float(abs(c_check)) != int(abs(c_check)):
                                            #if the difference of either column OR row is not divisible by two to make a whole
                                            #number, then part of the edge is already covered by a smaller edge and should not
                                            #be constructed. When the search criteria is 1 then r_check AND c_check will never be an integer.
                                            #This only filters out non- vertical and non- horizontal edges.
                                            r_check = (int(row1)-int(row0))
                                            c_check = (int(col1)-int(col0))                          
                                            if abs(r_check) != abs(c_check) or (abs(r_check) == 1 and abs(c_check) == 1):
                                                #if not directly diagonal South East OR path is diagonal South East to the first node only.
                                                if not (abs(r_check) == 0 and abs(c_check) > 1):
                                                    #if the edge is NOT horizontal AND greater than order of 1 (overlapping) then
                                                    if not (abs(c_check) == 0 and abs(r_check) > 1):
                                                        #if the edge is NOT vertical AND greater than order of 1 (overlapping) then
                                                        line = QgsFeature()
                                                        startXY = geometry.getXY(feature)
                                                        endXY = geometry.getXY(feature1)
                                                        points = [startXY[0], endXY[0]]
                                                        line.setGeometry(QgsGeometry.fromPolylineXY(points))
                                                        line.setFields(fields)      #set fields in the edge feature for which nodes are at each end
                                                        line['A'] = feature.id()
                                                        line['B'] = feature1.id()
                                                        featureList.append(line)
                                                        nxGrid.add_edge(feature.id(), feature1.id())        #add edge to networkx grid
            return(featureList)
    
    
    class geometry():
        
        def relations(selectableLayer, targetFeature, relationList):
            n = 0
            #_ = selectableLayer.removeSelection()
            sFeatures = selectableLayer.getFeatures(QgsFeatureRequest())
            for sFeat in sFeatures:
                if "not within" in relationList:
                    if sFeat.geometry().within(targetFeature.geometry()):
                        pass
                    else:
                        n+=1
                        _ = selectableLayer.select(sFeat.id())
                
                
                if "within" in relationList:
                    if sFeat.geometry().within(targetFeature.geometry()):
                        n+=1
                        _ = selectableLayer.select(sFeat.id())
                    
                    else:
                        pass
                
                if "intersects" in relationList:
                    if sFeat.geometry().intersects(targetFeature.geometry()):
                        n+=1
                        _ = selectableLayer.select(sFeat.id())
                    else:
                        pass
                if "contains" in relationList:
                    if targetFeature.geometry().within(sFeat.geometry()):
                        _ = selectableLayer.select(sFeat.id())
                    else:
                        n+=1
                        pass
            
            return(n)
        
        
        def getXY(feature):   #function to return list of XY of each feature fed in.  
            geom = feature.geometry()
            geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
            
            if geom.type() == QgsWkbTypes.PointGeometry:
                if geomSingleType:
                    xy = geom.asPoint()
                    #print("point:")
                    return([xy]) #returned as a list to match Polyline and Polygon format
                else:
                    xy = geom.asMultiPoint()
                    #print("multipoint:")  
                    return([xy]) #returned as a list to match Polyline and Polygon format
            
            if geom.type() == QgsWkbTypes.LineGeometry:
                if geomSingleType:
                    xy = geom.asPolyline()
                    #print("line:")
                    return(xy)  #return list of XY vertices
                else:
                    xy = geom.asMultiPolyline()
                    #print("multiline:")
                    return(xy)  #return list of XY vertices
            
            if geom.type() == QgsWkbTypes.PolygonGeometry:
                if geomSingleType:
                    xy = geom.asPolygon()
                    #print("polygon:")
                    return(xy)  #return list of XY vertices
                else:
                    xy = geom.asMultiPolygon()
                    #print("multipolygon:")
                    return(xy)  #return list of XY vertices
        
        
        def multiLayerBoundingBox(feature, existingExtents):
            #inputs feature to be tested and existing extents.
            ext = feature.geometry().boundingBox()
            test_xmin = str(ext.xMinimum())
            test_xmax = str(ext.xMaximum())
            test_ymin = str(ext.yMinimum())
            test_ymax = str(ext.yMaximum())
            try:
                xmin = existingExtents[0]
                xmax = existingExtents[1]
                ymin = existingExtents[2]
                ymax = existingExtents[3]
            except IndexError:
                pass
            try:
                if test_xmin < xmin:
                    #if existing bounding extents exist then test against new extents
                    xmin = test_xmin
                else:
                    pass
            except NameError:
                xmin = test_xmin
                #if existing extents dont exist then test extent is assigned 
            try:
                if test_xmax > xmax:
                    #if existing bounding extents exist then test against new extents
                    xmax = test_xmax
                else:
                    pass
            except NameError:
                xmax = test_xmax
                #if existing extents dont exist then test extent is assigned
            try:
                if test_ymin < ymin:
                    #if existing bounding extents exist then test against new extents
                    ymin = test_ymin
                else:
                    pass
            except NameError:
                ymin = test_ymin
                #if existing extents dont exist then test extent is assigned
            try:
                if test_ymax > ymax:
                    #if existing bounding extents exist then test against new extents
                    ymax = test_ymax
                else:
                    pass
            except NameError:
                ymax = test_ymax
                #if existing extents dont exist then test extent is assigned
            extents = [xmin, xmax, ymin, ymax]
            return extents  #extents returned as list
    
    class dataInput():
        
        def costSheet (location):
            #read in the cost sheet csv and create dictionary of surface types
                f = open(location, newline = '')
                reader = csv.reader(f)
                data = []
                cost_dict = {}
                for row in reader:
                    cost_dict[row[0]] = row[1]
                return cost_dict 	    
                f.close()
    
    
    #test if layers exist and assign them to variables
    try:
        connection_point = QgsProject.instance().mapLayersByName("connection_point")[0]
    except(IndexError):
        message = "missing layer: connection_point"
        _ = GUI.infoBar(message)
        raise HaltException(message)
    
    try:
        design_area = QgsProject.instance().mapLayersByName("design_area")[0]
    except(IndexError):
        message = "missing layer: design_area"
        _ = GUI.infoBar(message)
        raise HaltException(message)
    
    try:
        wayleave = QgsProject.instance().mapLayersByName("Land_Registry_Cadastral_Parcels")[0]
    except(IndexError):
        message = "missing layer: Land_Registry_Cadastral_Parcels — PREDEFINED"
        _ = GUI.infoBar(message)
        raise HaltException(message)
    
    try:
        uprn = QgsProject.instance().mapLayersByName("osopenuprn")[0]
    except(IndexError):
        message = "missing layer: osopenuprn"
        _ = GUI.infoBar(message)
        raise HaltException(message)
    
    
    daFeatures = design_area.getFeatures(QgsFeatureRequest())        
    for daFeat in daFeatures:
        n = geometry.relations(connection_point, daFeat, ["not within"])
        if n > 0:
            raise HaltException("connection_points outside design area")        #used to break code as sys.exit() or exit() closes QGIS instance
    
    
    try:
        to_discord(to_message="libraries imported, functions declared, connection_points checked")
    except:
        pass
    
    ###
    #- Create grid within design_area extents
    ###
    try:
        design_area = QgsProject.instance().mapLayersByName("design_area")[0]
    except(IndexError):
        message = "missing layer: design_area"
        _ = GUI.infoBar(message)
        raise HaltException(message)
    daFeatures = design_area.getFeatures(QgsFeatureRequest())
    ext = []
    for daFeat in daFeatures:
            ext = geometry.multiLayerBoundingBox(daFeat, ext)
    else:
        pass
    
    ext = str(ext[0]) + "," + str(ext[1]) + "," + str(ext[2]) + "," + str(ext[3])
    
    cellsize = 1        #define eucledian distance between nodes (m)
    crs = "EPSG:27700"    
    #prepare the extent in a format the VectorGrid tool can interpret (xmin,xmax,ymin,ymax)
    crs = QgsProject().instance().crs().toWkt() #get layer crs from QGIS environment
    grid=str(QgsProject.instance().readPath("./")) + str(cellsize) + "m scale" + ".gpkg"
    #get path of QGIS instance and set parent folder as save location
    params = {
        'TYPE': 0,
        'EXTENT': ext,
        'HSPACING': cellsize,
        'VSPACING': cellsize,
        'CRS': crs,
        'OUTPUT': grid
        }
    output = processing.run('native:creategrid', params)
    layer = QgsVectorLayer(grid, "area_grid", "ogr")
    _ = QgsProject().instance().addMapLayer(layer)
    
    try:
        to_discord(to_message="grid created")
    except:
        pass
    
    ###
    #- assign column and row attributes to area_grid
    ###
    try:
        grid = QgsProject.instance().mapLayersByName("area_grid")[0]
    except(IndexError):
        raise HaltException(message)
    
    _ = attributes.headers(grid, [QgsField('column', QVariant.String),QgsField('row', QVariant.String)] )
    #create two new attributes for column and row
    
    gridFeatures = grid.getFeatures(QgsFeatureRequest())
    
    column_values_all = []
    row_values_all = []
    
    for gridFeat in gridFeatures:
        _ = column_values_all.append(gridFeat.attribute(grid.fields().indexFromName('left')))
        _ = row_values_all.append(gridFeat.attribute(grid.fields().indexFromName('top')))
    #append X and Y coordinate of top left corner for later reference 
    
    unique_columns = attributes.unique_list(column_values_all)
    unique_rows = attributes.unique_list(row_values_all)
    #create unique list of all X and Y co-ordinates
    
    _ = unique_columns.sort(reverse=False)
    _ = unique_rows.sort(reverse=True)
    #sort column and row numbers so iterations will start at top left.
    
    columns_dict = dict.fromkeys(unique_columns)
    rows_dict = dict.fromkeys(unique_rows)
    
    n=0
    for c in range(len(unique_columns)):
        columns_dict[unique_columns[c]] = n
        n+=1
    
    n=0
    for r in range(len(unique_rows)):
        rows_dict[unique_rows[r]] = n
        n+=1
    
    grid = QgsProject.instance().mapLayersByName("area_grid")[0]
    _ = grid.startEditing()
    
    gridFeatures = grid.getFeatures(QgsFeatureRequest())
    for gridFeat in gridFeatures:
        columnNum = columns_dict[gridFeat.attribute(grid.fields().indexFromName('left'))]
        rowNum = rows_dict[gridFeat.attribute(grid.fields().indexFromName('top'))]
        attrIndex_column = grid.fields().indexFromName('column')
        attrIndex_row = grid.fields().indexFromName('row')
        _ = grid.changeAttributeValue(gridFeat.id(), attrIndex_column, columnNum)
        _ = grid.updateFields()
        _ = grid.changeAttributeValue(gridFeat.id(), attrIndex_row, rowNum)
        _ = grid.updateFields()
    
    _ = grid.commitChanges()
    _ = grid.triggerRepaint()
    
    try:
        to_discord(to_message="column and row attributes created and assigned for area_grid")
    except:
        pass
    ###
    #- extract cost attributes to grid
    ###
    costSheet = dataInput.costSheet("cost_sheet.csv")
    
    grid = QgsProject.instance().mapLayersByName("area_grid")[0]
    topo = QgsProject.instance().mapLayersByName("Topographicarea")[0]
    #assign layers to variables
    
    _ = attributes.headers(topo, [QgsField('concat', QVariant.String),QgsField('cost', QVariant.Double)] )
    #add two new atributes to topo layer
    
    layer = topo
    layer.startEditing()
    features = layer.getFeatures(QgsFeatureRequest())
    costAttrIndex = layer.fields().indexFromName('cost')
    concatAttrIndex = layer.fields().indexFromName('concat')
    test_break = 0
    for feature in features:
        themeAttr = feature.attribute(layer.fields().indexFromName('theme'))
        descgroupAttr = feature.attribute(layer.fields().indexFromName('descriptivegroup'))
        desctermAttr = feature.attribute(layer.fields().indexFromName('descriptiveterm'))
        #for each topo feature assign atribute values to variables
        surface_string = attributes.concat([themeAttr, descgroupAttr, desctermAttr])
        #concat attributes into single string, removing any blanks
        _ = layer.changeAttributeValue(feature.id(), concatAttrIndex, surface_string)
        _ = layer.updateFields()
        #update layer feature with surface_string
        try:
            _ = layer.changeAttributeValue(feature.id(), costAttrIndex, costSheet[feature.attribute(concatAttrIndex)])
        except:
            test_break +=1
        _ = layer.updateFields()
        #update layer feature with cost
    
    _ = layer.commitChanges()
    _ = layer.triggerRepaint()
    if test_break > 0:
        message = "add surface type and cost attributes to cost_sheet.csv"
        raise HaltException(message)
        
    _ = attributes.headers(grid, [QgsField('surface', QVariant.String),QgsField('cost', QVariant.Double)] )
    #add surface and cost attributes to grid layer
    
    _ = grid.startEditing()
    features = grid.getFeatures(QgsFeatureRequest())                             #re-getFeatures to assign new attributes to features variable
    for feature in features:
        _ = grid.changeAttributeValue(feature.id(), grid.fields().indexFromName('cost'), '') 
        surfaceAttrIndex = grid.fields().indexFromName('surface')
        costAttrIndex = grid.fields().indexFromName('cost')
        centroid = feature.geometry().centroid().asPoint()
        centroid = QgsGeometry.fromPointXY(centroid)
        topoFeatures = topo.getFeatures(QgsFeatureRequest())
        for tFeature in topoFeatures:
            if centroid.intersects(tFeature.geometry()):
                #if grid feature centroid (point) intersects with topo feature 
                _ = grid.changeAttributeValue(feature.id(), grid.fields().indexFromName('surface'), tFeature.attribute(topo.fields().indexFromName('concat')))
                _ = grid.changeAttributeValue(feature.id(), grid.fields().indexFromName('cost'), tFeature.attribute(topo.fields().indexFromName('cost')))
                #take topofeature concat and cost attributes and assign them to the grid feature surface and cost attributes.
    
    _ = grid.commitChanges()
    
    try:
        to_discord(to_message="cost attributes spatially joined from Topographicarea to area_grid")
    except:
        pass
    
    ###
    #- find indicative private wayleaves
    ###
    
    _ = wayleave.startEditing()
    _ = attributes.headers(wayleave,[QgsField('private', QVariant.String)])
    _ = wayleave.commitChanges()
    #add "private" attribute to layer
    uprnFeatures = uprn.getFeatures(QgsFeatureRequest())
    for uprnFeat in uprnFeatures:
        _ = geometry.relations(wayleave, uprnFeat, ["contains", "intersects"])
        #selects any wayleave features that contain or intersect a uprn feature
    
    _ = wayleave.startEditing()
    privFeatures = wayleave.selectedFeatures()
    for privFeat in privFeatures:
        _ = wayleave.changeAttributeValue(privFeat.id(), wayleave.fields().indexFromName('private'), 'y')  
        #with selected wayleave features set "private" attribute to 'y'
    
    _ = wayleave.commitChanges()
    
    try:
        to_discord(to_message="indicative private wayleaves found")
    except:
        pass
    
    ###
    #- Grid List
    ###
    
    gridList_cost = []
    gridList_surface = []
    
    for r in range(len(unique_rows)):
        _ = gridList_cost.append([])
        for c in range(len(unique_columns)):
            _ = gridList_cost[r].append([])
    
    layer = QgsProject.instance().mapLayersByName("area_grid")[0]
    features = layer.getFeatures(QgsFeatureRequest())
    for feature in features:
        gridRow = int(feature.attribute(layer.fields().indexFromName('row')))
        gridCol = int(feature.attribute(layer.fields().indexFromName('column')))   
        gridList_cost[gridRow][gridCol] = feature.attribute(layer.fields().indexFromName('cost'))
        #for each grid feature, take "row" and "column attribute and assign cost attribute to list item with corresponding nested list index 
    
    try:
        to_discord(to_message="area_grid features assigned to list")
    except:
        pass
    
    ###
    #- construct arcs
    ###
    
    _ = connection_point.startEditing()
    cpFeatures = connection_point.getFeatures(QgsFeatureRequest())
    
    for cpFeat in cpFeatures:
        gridFeatures = grid.getFeatures(QgsFeatureRequest())
        for gFeat in gridFeatures:
            if cpFeat.attribute(connection_point.fields().indexFromName('TL')) == str(gFeat.attribute(grid.fields().indexFromName('left'))) + ', ' + str(gFeat.attribute(grid.fields().indexFromName('top'))):
                #if connection_point XY == grid feature left + top attribute (XY) then
                connection_point.changeAttributeValue(cpFeat.id(), connection_point.fields().indexFromName('col'), gFeat.attribute(layer_grid.fields().indexFromName('column')))
                connection_point.changeAttributeValue(cpFeat.id(), connection_point.fields().indexFromName('row'), gFeat.attribute(layer_grid.fields().indexFromName('row')))
                #assign grid "column" and "row" to connection_point "col" and "row" attributes
    
    _ = connection_point.updateFields()
    _ = connection_point.commitChanges()
    
    
    file = str(QgsProject.instance().readPath("./"))
    file = file.replace("/", "\\")
    file = file + str("\\arc.gpkg")
    layer = QgsVectorLayer("LineString?crs=epsg:27700", "arc", "memory")
    pr = layer.dataProvider()
    _ = layer.startEditing()
    _ = pr.addAttributes(
        [
         QgsField("cost", QVariant.Double),
         QgsField("A", QVariant.Int),
         QgsField("B", QVariant.Int)
         ]    
        )
    
    _ = layer.updateFields()
    _ = layer.commitChanges()
    #create linestring arc layer with "cost", "A", and "B" attributes
    writer = QgsVectorFileWriter.writeAsVectorFormat(layer, file, "ogr")
    _ = iface.addVectorLayer(file, 'arc', 'ogr')
    
    searchCrit = 1  #set search criteria (number of neighbourhoods to be searched)
    
    nxGrid=nx.Graph()   #define netwrokx graph
    layer_grid = QgsProject.instance().mapLayersByName("area_grid")[0]
    layer = QgsProject.instance().mapLayersByName("arc")[0]
    features = layer_grid.getFeatures(QgsFeatureRequest())
    _ = layer.startEditing()
    for feature in features:
        if feature.attribute(layer_grid.fields().indexFromName('cost')) != 'NA':
            #if grid features != 'NA'
            _ = nxGrid.add_node(feature.id(), col=feature.attribute(layer_grid.fields().indexFromName('column')), row=feature.attribute(layer_grid.fields().indexFromName('row')))
            #add node to networkx grid with grid feature id, grid column and grid row attributes
            fields = layer.fields()
            featureList = networkArc.construct(layer_grid, feature, searchCrit)
            #run construct function for each feature
            pr = layer.dataProvider()
            _ = layer.startEditing()
            feat = QgsFeature()
            try:
                _ = pr.addFeatures(featureList)
            except(TypeError):
                print('no matching links')
                continue
    
    _ = layer.commitChanges()
    
    try:
        to_discord(to_message=("connecting arcs constructed with neighbour search area of: " + str(searchCrit)))
    except:
        pass
    
    ###
    #- terminal_points
    ###
    #determines which nodes in weighted graph are going to be terminal nodes based on proximity to connection_point features
    arc = QgsProject.instance().mapLayersByName('arc')[0]
    termPoints = []
    gridIDs = []
    fields = arc.fields()
    
    cpFeatures = connection_point.getFeatures(QgsFeatureRequest())
    for cpFeat in cpFeatures:
        _ = lp={}
        gridFeatures = grid.getFeatures(QgsFeatureRequest())
        for gridFeat in gridFeatures:
            if gridFeat.attribute(layer_grid.fields().indexFromName('cost')) != 'NA':
                if gridFeat.geometry() == cpFeat.geometry():
                    _ = termPoints.append(gridFeat.attribute(layer_grid.fields().indexFromName('fid')))
                elif gridFeat.geometry() != cpFeat.geometry():
                    dist = cpFeat.geometry().distance(gridFeat.geometry())
                    #get distance from connection point to grid feature (point)
                    if len(lp) == 1:
                        if dist < list(lp.values())[0]:
                            for key in list(lp.keys()):
                                if lp[key] == max(lp.values()):
                                    _ = lp.pop(key)
                                    _ = lp[gridFeat.attribute(layer_grid.fields().indexFromName('id'))] = dist
                    elif len(lp) < 1:
                        _ = lp[gridFeat.attribute(layer_grid.fields().indexFromName('id'))] = dist
                    elif len(lp) > 1:
                        print('lp error')
                        break
                    #create a dictionary with the grid node with the smallest distance to the connection point
        _ = termPoints.append(lp)
    
    terminal_nodes = {}
    for p in termPoints:
        _ = terminal_nodes.update(p)
    
    
    terminal_nodes = list(terminal_nodes.keys())
    #add shortest distance node keys to a list
    for n in terminal_nodes:
        _ = layer_grid.select(terminal_nodes)
    
    try:
        to_discord(to_message="terminal points found")
    except:
        pass
    
    ###
    #- assign arc costs (intersectPoint script)
    ###
    
    _ = arc.startEditing()
    arcFeatures = arc.getFeatures(QgsFeatureRequest())
    topoFeatures = topo.getFeatures(QgsFeatureRequest())
    
    for f in arcFeatures:
        arcCost = 0
        topo = QgsProject.instance().mapLayersByName("Topographicarea")[0]
        topoFeatures = topo.getFeatures(QgsFeatureRequest())
        
        for t in topoFeatures:
            if f.geometry().intersects(t.geometry()):
                intersection = f.geometry().intersection(t.geometry())
                arcCost = arcCost + (float(t.attribute(topo.fields().indexFromName('cost'))) * float(intersection.length()))
                #for each Topologicalarea feature, get distance each edge intersects it and multiply it by cost per m. for each edge feature add these together
            else:
                pass        
        
        _ = arc.changeAttributeValue(f.id(), arc.fields().indexFromName('cost'), arcCost)
    
    _ = arc.updateFields()
    _ = arc.commitChanges()
    
    try:
        to_discord(to_message="raw arc costs calculated and assigned")
    except:
        pass
    
    ###
    #- additional cost for private land
    ###
    _ = arc.removeSelection()
    _ = wayleave.removeSelection()
    wlvFeatures = wayleave.getFeatures(QgsFeatureRequest())
    for wlvFeat in wlvFeatures:
        if wlvFeat.attribute(wayleave.fields().indexFromName('private')) == 'y':
            _ = wayleave.select(wlvFeat.id())
            #select wayleave features which have been previously determined as private
        else:
            pass
    
    
    _ = arc.startEditing()
    privFeatures = wayleave.selectedFeatures()
    for feat in privFeatures:
        _ = geometry.relations(arc, feat, ["contains", "intersects"])
        #select edge features which cross private wayleave
    
    privArcFeatures = arc.selectedFeatures()
    for privArcFeat in privArcFeatures:
        surfaceCost = float(privArcFeat.attribute(arc.fields().indexFromName('cost')))
        _ = arc.changeAttributeValue(privArcFeat.id(), arc.fields().indexFromName('cost'), (surfaceCost * 10))
        #multiple raw cost to make private land less desirable for the steiner tree problem
    _ = arc.commitChanges()
    _ = arc.removeSelection()
    _ = wayleave.removeSelection()
    
    arc = QgsProject.instance().mapLayersByName("arc")[0]
    arcFeatures = arc.getFeatures(QgsFeatureRequest())
    for f in arcFeatures:
        arcCost = float(f.attribute(arc.fields().indexFromName('cost')))
        _ = nxGrid[int(f.attribute(arc.fields().indexFromName('A')))][int(f.attribute(arc.fields().indexFromName('B')))]['weight']=arcCost
        #input edges into networkx weighted graph
    
    try:
        to_discord(to_message="additonal weighting for private land assigned to arc features")
    except:
        pass
    
    ###
    #- steiner tree calculation
    ###
    
    st = apx.metric_closure(nxGrid, weight='weight')
    st = apx.steiner_tree(nxGrid, terminal_nodes, weight='weight')
    
    _ = nx.draw(st)
    _ = plt.show()
    to_discord(to_message="steiner tree calculated and MatPlotLib graph output")
    
    #reimport steinertree to QGIS
    layer = QgsProject.instance().mapLayersByName("area_grid")[0]
    grid_fields = layer.fields()
    #create steiner node layer for sub graph nodes in QGIS
    file = str(QgsProject.instance().readPath("./"))
    file = file.replace("/", "\\")
    file = file + str("\\steiner_point.gpkg")
    layer = QgsVectorLayer("Point?crs=epsg:27700", "steiner_point", "memory")
    pr = layer.dataProvider()
    _ = layer.startEditing()
    _ = pr.addAttributes(
        grid_fields
        )
    _ = layer.updateFields()
    _ = layer.commitChanges()
    writer = QgsVectorFileWriter.writeAsVectorFormat(layer, file, "ogr")
    _ = iface.addVectorLayer(file, 'steiner_point', 'ogr')
    
    
    layer = QgsProject.instance().mapLayersByName("arc")[0]
    arc_fields = layer.fields()
    #create steiner edge layer for sub graph edges in QGIS
    file= str(QgsProject.instance().readPath("./"))
    file = file.replace("/", "\\")
    file = file + str("\\steiner_arc.gpkg")
    layer = QgsVectorLayer("LineString?crs=epsg:27700", "arc", "memory")
    pr = layer.dataProvider()
    _ = layer.startEditing()
    _ = pr.addAttributes(
        arc_fields
        )
    _ = layer.updateFields()
    _ = layer.commitChanges()
    writer = QgsVectorFileWriter.writeAsVectorFormat(layer, file, "ogr")
    _ = iface.addVectorLayer(file, 'steiner_arc', 'ogr')
    
    
    addFeatures = []
    for a in st.nodes():
        layer = QgsProject.instance().mapLayersByName("area_grid")[0]
        features = layer.getFeatures(QgsFeatureRequest())
        for feat in features:
            b = feat.attribute(layer.fields().indexFromName('id'))
            if a == b:
                addFeatures.append(feat)
    #for each steiner node, if id matches grid feature id then copy grid feature into steiner_point layer
    
    layer = QgsProject.instance().mapLayersByName("steiner_point")[0]
    _ = layer.startEditing()
    dp = layer.dataProvider()
    _ = dp.addFeatures(addFeatures)
    _ = layer.commitChanges()
    
    
    addFeatures = []
    for a in st.edges():
        layer = QgsProject.instance().mapLayersByName("arc")[0]
        features = layer.getFeatures(QgsFeatureRequest())
        for feat in features:
            b = (feat.attribute(layer.fields().indexFromName('A')), feat.attribute(layer.fields().indexFromName('B')))
            c = (feat.attribute(layer.fields().indexFromName('B')), feat.attribute(layer.fields().indexFromName('A')))
            if a == b or a == c:
                _ = addFeatures.append(feat)
    #for each steiner edge, if end points match up to an arc layer end points then copy arc layer feature and paste into steiner_arc layer
    
    layer = QgsProject.instance().mapLayersByName("steiner_arc")[0]
    _ = layer.startEditing()
    dp = layer.dataProvider()
    _ = dp.addFeatures(addFeatures)
    _ = layer.commitChanges()
    
    try:
        to_discord(to_message="Steiner tree subgraph imported to QGIS and assigned to layer")
    except:
        pass

except HaltException as h:
    print(h)



