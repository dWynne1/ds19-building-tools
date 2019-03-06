import arcpy
import os
import sys

# Find folder holding swisshs.py and import
scripts_folder = os.path.join(os.path.dirname(__file__), 'Scripts')
sys.path.append(scripts_folder)

import swisshs
import historicdots


class SwissHillshade(object):
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

        # For symbology, use __file__ attribute to find the .lyr file
        out_perspective.symbology = os.path.join(os.path.dirname(__file__),
                                                 'LayerFiles\\Swiss_Aerial.lyr')

        out_shade = arcpy.Parameter(
            name='out_shade',
            displayName='Output Shade',
            datatype='DERasterDataset',
            direction='Output',
            parameterType='Derived')

        out_shade.parameterDependencies = [in_dem.name]

        # For symbology, use __file__ attribute to find the .lyr file
        out_shade.symbology = os.path.join(os.path.dirname(__file__),
                                           'LayerFiles\\Swiss_Filtered.lyr')

        params = [in_dem, out_workspace, prefix, z_factor, out_perspective,
                  out_shade]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        param_values = (p.valueAsText for p in parameters[0:4])

        try:
            perspective, shade = swisshs.swiss_hillshade(*param_values)
        except Exception as err:
            arcpy.AddError(err)
            sys.exit(1)

        parameters[4].value = perspective
        parameters[5].value = shade

        return


class HistoricDots(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Historic Dots"
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

        out_feature_class = arcpy.Parameter(
            name='out_feature_class ',
            displayName='Output Feature Class',
            datatype='DEFeatureClass',
            direction='Output',
            parameterType='Required')
        
        # For symbology, use __file__ attribute to find the .lyr file
        out_feature_class.symbology = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'LayerFiles', 
            'contour_dot.lyr')
        
        contour_interval = arcpy.Parameter(
            name='contour_interval',
            displayName='Contour Interval',
            datatype='GPLong',
            direction='Input',
            parameterType='Required')        
        
        base_contour = arcpy.Parameter(
            name='base_contour',
            displayName='Base Contour',
            datatype='GPLong',
            direction='Input',
            parameterType='Optional')       
        
        base_contour.value = 0  # default

        z_factor = arcpy.Parameter(
            name='z_factor',
            displayName='Z Factor',
            datatype='GPLong',
            direction='Input',
            parameterType='Optional')

        z_factor.value = 1  # default

        params = [in_dem, out_feature_class, contour_interval, base_contour,
                  z_factor]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        parameters[0].setWarningMessage(parameters[1].symbology)
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        param_values = (p.valueAsText for p in parameters)

        try:
            historicdots.historic_dots(*param_values)
        except Exception as err:
            arcpy.AddError(err)
            sys.exit(1)

        return
