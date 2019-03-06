import arcpy


class ToolValidator(object):
    """Class for validating a tool's parameter values and controlling
    the behavior of the tool's dialog."""

    def __init__(self):
        """Setup arcpy and the list of tool parameters."""

        self.params = arcpy.GetParameterInfo()

    def initializeParameters(self):
        """Refine the properties of a tool's parameters.  This method is
        called when the tool is opened."""
        return

    def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        if self.params[0].valueAsText and self.params[1].valueAsText:
        
            input_boundary = arcpy.Describe(self.params[0]).extent.polygon
            clip_boundary = arcpy.Describe(self.params[1]).extent.polygon
            
            disjoint = input_boundary.disjoint(clip_boundary)

            #if disjoint:  # right
            if not disjoint:  # wrong
                self.params[1].setErrorMessage('Clip area outside raster boundary')
                
        return

