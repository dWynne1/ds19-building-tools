# -*- coding: utf-8 -*-
r""""""
__all__ = ['HistoricDots', 'SwissHillshade']
__alias__ = 'viztools'
from arcpy.geoprocessing._base import gptooldoc, gp, gp_fixargs
from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject

# Tools
@gptooldoc('HistoricDots_viztools', None)
def HistoricDots(input_dem=None, Output_Feature_Class=None, contour_interval=None, base_contour=None, z_factor=None):
    """HistoricDots_viztools(input_dem, Output_Feature_Class, contour_interval, {base_contour}, {z_factor})

     INPUTS:
      input_dem (Raster Layer)
      contour_interval (Long)
      base_contour {Long}
      z_factor {Long}

     OUTPUTS:
      out_feature_class  (Feature Class)"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.HistoricDots_viztools(*gp_fixargs((input_dem, Output_Feature_Class, contour_interval, base_contour, z_factor), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('SwissHillshade_viztools', None)
def SwissHillshade(input_dem=None, out_workspace=None, prefix_name=None, z_factor=None):
    """SwissHillshade_viztools(input_dem, out_workspace, {prefix_name}, {z_factor})

     INPUTS:
      input_dem (Raster Layer)
      out_workspace (Workspace)
      prefix_name {String}
      z_factor {Long}"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.SwissHillshade_viztools(*gp_fixargs((input_dem, out_workspace, prefix_name, z_factor), True)))
        return retval
    except Exception as e:
        raise e


# End of generated toolbox code
del gptooldoc, gp, gp_fixargs, convertArcObjectToPythonObject