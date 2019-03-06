"""
 swisshs.py
 Based on model developed by Eduard Imhof and a previous model
 built by Esri

 Originally by Linda Beale, Esri
 Updates by Dave Wynne, Esri

 Swiss-style hillshading as described by Imhof, E (2007)
 Cartographic Relief Presentation, Esri Press
"""

import os
import sys
import arcpy
from arcpy.sa import *


class SwissHillshade(object):
    """Swiss Hillshade Tool class"""
    
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Swiss Hillshade"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        in_dem = arcpy.Parameter(
            name='input_dem',
            displayName='Input DEM',
            datatype='GPRasterLayer',
            direction='Input',
            parameterType='Required')

        out_workspace = arcpy.Parameter(
            name='out_workspace',
            displayName='Output Workspace',
            datatype='DEWorkspace',
            direction='Input',
            parameterType='Required')
        
        out_workspace.defaultEnvironmentName = 'workspace'
        out_workspace.filter.list = ['Local Database', 'Remote Database']

        prefix = arcpy.Parameter(
            name='prefix_name',
            displayName='Output hillshade prefix name',
            datatype='GPString',
            direction='Input',
            parameterType='Optional')

        prefix.value = 'swiss'  # default

        z_factor = arcpy.Parameter(
            name='z_factor',
            displayName='Z Factor',
            datatype='GPLong',
            direction='Input',
            parameterType='Optional')

        z_factor.value = 1  # default

        out_perspective = arcpy.Parameter(
            name='out_perspective',
            displayName='Output Perspective',
            datatype='DERasterDataset',
            direction='Output',
            parameterType='Derived')

        out_perspective.parameterDependencies = [in_dem.name]

        # Use __file__ attribute to find the .lyr file
        out_perspective.symbology = \
            os.path.join(os.path.dirname(os.path.dirname(__file__)),
                         'LayerFiles', 
                         'Swiss_Aerial.lyr')

        out_shade = arcpy.Parameter(
            name='out_shade',
            displayName='Output Shade',
            datatype='DERasterDataset',
            direction='Output',
            parameterType='Derived')

        out_shade.parameterDependencies = [in_dem.name]

        # Use __file__ attribute to find the .lyr file
        out_shade.symbology = \
            os.path.join(os.path.dirname(os.path.dirname(__file__)),
                         'LayerFiles', 
                         'Swiss_Filtered.lyr')

        params = [in_dem, out_workspace, prefix, z_factor, out_perspective,
                  out_shade]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        try:
            if arcpy.CheckExtension("spatial") != "Available":
                raise Exception
        except Exception:
            return False  # tool cannot be executed

        return True  # tool can be executed

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
            
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        
        if parameters[3].value <= 0:
            parameters[3].setErrorMessage('Z Factor must be greater than 0')
        
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        param_values = (p.valueAsText for p in parameters[0:4])

        try:
            perspective, shade = swiss_hillshade(*param_values)
        except Exception as err:
            arcpy.AddError(err)
            sys.exit(1)

        parameters[4].value = perspective
        parameters[5].value = shade

        return


def create_output_name(workspace, suffix, prefix=None):
    """
    Create path from components

    arguments:
    workspace -- directory component
    suffix -- second part of output name
    prefix -- first part of output name
    """

    if prefix:
        name = '{}_{}'.format(prefix, suffix)
    else:
        name = suffix

    return os.path.join(workspace, name)


def swiss_hillshade(in_DEM, out_workspace, r_name='swiss', Z_factor=1):
    """
    Calculates Swiss hillshade

    arguments:
    in_DEM -- Input DEM
    out_workspace -- Output workspace
    r_name -- Partial output name
    Z_factor -- Input elevation z factor
    """
    # Check out the Spatial Analyst license
    arcpy.CheckOutExtension('Spatial')

    divVal = 5
    azimuth = 315
    altitude = 45
    modelShadows = 'NO_SHADOWS'

    # Z_factor can be passed as a string (but should be safe either way)
    Z_factor = int(Z_factor)

    # Process: Hillshade
    outHillshade = Hillshade(in_DEM, azimuth, altitude, modelShadows, Z_factor)
    filterHillshade = FocalStatistics(outHillshade, 'Rectangle 4 4 CELL', 'MEDIAN', 'DATA')

    # Process: Combine rasters
    outDivide = Divide(in_DEM, divVal)
    # outPlus = outDivide + outHillshade
    outPlus = outDivide + filterHillshade

    # Process: Save outputs
    out_shade = create_output_name(out_workspace, 'filter', r_name)
    outHillshade.save(out_shade)

    out_perspective = create_output_name(out_workspace, 'aerial', r_name)
    outPlus.save(out_perspective)

    return out_perspective, out_shade


#if __name__ == '__main__':
    #args = tuple(arcpy.GetParameterAsText(i) for i in range(arcpy.GetArgumentCount()))

    #args = args[0:4]  # Only pass through non-derived parameters

    #try:
        #perspective, shade = swiss_hillshade(*args)
    #except Exception as err:
        #arcpy.AddError(err)
        #sys.exit(1)

    ## Set derived outputs
    #arcpy.SetParameterAsText(4, perspective)
    #arcpy.SetParameterAsText(5, shade)