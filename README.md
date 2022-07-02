Creation of a weighted graph G = (V,E) based on OS MasterMap data to run the
Steiner Tree alogrithm using the NetworkX python library. 

DESCRIPTION
This script constructs a weighted graph of a given resolution within a user
defined area in QGIS. Edge weights are calculated based on intersections
with Ordnance Survey MasterMap topologicalarea features and a corresponding
cost lookup sheet. The weighted graph is fed into the networkx pythton library
to conduct a Steiner Tree analysis. The resulting sub-graph is then returned
for plotting within QGIS. 

PREREQUISITES
MODULE PREREQUISITES
The script was designed for use on Windows OS and tested in windows10.

Most recent stable version of QGIS (v.3.22 at the time of writing).
    downloadable from:
    https://www.qgis.org/en/site/forusers/download.html

networkx python library. this can be downloaded from the command line using
'pip install networkx'
to make the module available from within QGIS, the networkx folder location
can be found by running the below code at the command line.

>python
>import networkx
>networkx.__file__


The parent folder of this __init__ file (called networkx) can then be copied
and pasted into the site_packages folder of the path tree which can be found by
searching for the matplotlib folder wihtin the QGIS python environment as
matplotlib is included with all python versions as standard.

>>> import matplotlib
>>> matplotlib.path


discord_webhooks module
    this module is not mandatory but can be utilised to update a discord server 
    at various points throughout processing for both logging time taken and
    to allow progress updates from a distance or if QGIS becomes non-responsive.
    this can be installed into QGIS in a similar manner to networkx as listed above.
    to use this, you will have to have a discord account and have created a
    webhook URL from within discord. A guide to completing this is shown here:
    https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
    this URL should be added to the script on line XXXX as shown below.
    webhook = DiscordWebhook(url='[WEBHOOKADDRESS]', content=to_message, rate_limit_retry=True)
    
>pip install discord_webhooks
>python
>import discord_webhooks
>discord_webhooks.__file__
#find module folder and copy
#below code in QGIS to find QGIS pythin environment file path
>>>import matplotlib
>>>matplotlib.path
#paste discord_webhooks folder into site-packages folder in sub path


DATA PREREQUISITES
layers required
design_area:
    geometry type: polygon
    Attributes: no mandatory attributes
    this shape is used to define the outer boundaries of the created
    weighted graph G = (V,E). If any connection_point features are external to 
    the design_area, the script will be broken
    
osopenuprn:
    geometry type: Point
    Attributes: no mandatory attributes.
    This data is used to assign indicative privacy attributes to the 
    Land_Registry_Cadastral_Parcels layer. It is STRONGLY recomended that a 
    subset of this data is used to reduce processing times.
    free opensource UPRN data available from:https://osdatahub.os.uk/downloads/open/OpenUPRN?_gl=1*1nxqvym*_ga*Mzg4OTY4MzkyLjE2NTY2OTAwMjc.*_ga_59ZBN7DVBG*MTY1Njc1MjE1NC4xLjAuMTY1Njc1MjE1NC4w&_ga=2.177230501.1677767200.1656690027-388968392.1656690027
    
Land_Registry_Cadastral_Parcels:
    geometry type: Polygon
    Attributes: no mandatory attributes. "Private" attribute will be added
        automatically by script
    free opensource land registry data is available by area here. It is STRONGLY 
    recomended that a subset of this data is used to reduce processing times.
    layers will need to be converted from .gml files to any common, editable
    geospatial file format (geopackage, shapefile etc.) and renamed to remove
    '--PREDEFINED' from layer name.
    layers available from: https://use-land-property-data.service.gov.uk/datasets/inspire/download
    
connection_point:
    geometry type: Point
    Attributes: no mandatory attributes
    these will be the main input features for the terminal points in the 
    steiner tree algorithm. In a fibre network context, these will typify
    toby box apparatus and a terminal drop node.

Topographicarea:
    geometry type: polygon
    attributes: "theme", "descriptivegroup", "descriptiveterm" are concatenated to give a surface type which is then
    used as a lookup index for the cost_grid. It is STRONGLY recomended that a 
    subset of this data is used to reduce processing times.

cost_sheet.csv:
    cost_sheet derived by the user. Once surface_type has been derived within 
    Topographicarea layer, this can be exported as a CSV from within the 
    QGIS GUI. Duplicate values within the cost_sheet can then be removed and
    cost/m weightings can be added. This is easiest completed within
    Microsoft Excel or other spreadsheet software packages.
    
    


