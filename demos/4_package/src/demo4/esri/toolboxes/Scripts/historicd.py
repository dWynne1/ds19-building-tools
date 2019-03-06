"""
 historicd.py
 This technique is an implementation by Ken Field of the historic technique

 Programmed by Linda Beale, Esri Inc

 Description:  Creates historic dots from an input elevation raster

"""
import os
import sys
import arcpy


class HistoricDots(object):
    """Historic Dots Tool class"""
    
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
        
        # Use __file__ attribute to find the .lyr file
        out_feature_class.symbology = \
            os.path.join(os.path.dirname(os.path.dirname(__file__)),
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
        
        if parameters[2].value and parameters[2].value <= 0:
            parameters[2].setErrorMessage('Contour Interval must be greater than 0')         
        
        if parameters[4].value <= 0:
            parameters[4].setErrorMessage('Z Factor must be greater than 0')        
        
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        param_values = (p.valueAsText for p in parameters)

        try:
            historic_dots(*param_values)
        except Exception as err:
            arcpy.AddError(err)
            sys.exit(1)

        return


def historic_dots(in_DEM, out_fc, contour_width, base_contour, z_factor):
    """
    historic_dots: calculates historic dots

    Required arguments:
    Inputs:
        in_DEM -- Input DEM.
        contour_width -- contour width.
        base_contour -- base contour value.
        z_factor -- z value.
    Outputs:
        out_fc -- output Feature Class.
    """
    # Check out the Spatial Analyst license
    arcpy.CheckOutExtension("Spatial")

    slope_in_degrees = arcpy.sa.Slope(in_DEM, "DEGREE")
    out_condition = arcpy.sa.Con(slope_in_degrees > 5, in_DEM)
    arcpy.sa.Contour(out_condition, out_fc, contour_width, base_contour,
                     z_factor)

    return
