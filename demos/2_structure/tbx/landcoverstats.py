import arcpy
import os

arcpy.env.overwriteOutput = True


def convert_to_array(table, fields):
    """Convert table (can be a feature class) to an array"""
    array1 = arcpy.da.TableToNumPyArray(table,
                                        ['SHAPE@AREA', 'gridcode'] + fields)
    return array1


def convert_to_features(raster, features=None, extent_features=None):
    """
    Convert raster to features, clipping it if an extent feature class
    is provided
    """
    arcpy.env.extent = extent_features
    feature_class = arcpy.RasterToPolygon_conversion(raster,
                                                     features,
                                                     raster_field='Class_name')
    arcpy.ClearEnvironment('extent')

    return feature_class[0]


def update_with_stats(table, arr, fields):
    """Update table with statistics"""
    total_area = arr['SHAPE@AREA'].sum()

    with arcpy.da.UpdateCursor(table, ['Shape_Area', 'gridcode'] + fields) as cursor:
        for row in cursor:
            total_class_area = arr[arr['gridcode'] == row[1]]['SHAPE@AREA'].sum()

            row[2] = round(row[0] / total_area * 100.0, 3)  # continuous_area
            row[3] = round(row[0] / total_class_area * 100.0, 3)  # area_compared_to_total
            row[4] = round(total_class_area / total_area * 100.0, 3)  # total_class_area

            cursor.updateRow(row)

    return


def add_fields(features, fields=None):
    """Add required fields to the output"""
    for field_name in fields:
        # Add fields, for alias, replace underscores with spaces, and
        # title all words
        arcpy.AddField_management(
            features, field_name, 'DOUBLE',
            field_alias=field_name.replace('_', ' ').title())

    return


if __name__ == '__main__':
    fields = ['continuous_area', 'area_compared_to_total', 'total_class_area']

    in_raster = arcpy.GetParameterAsText(0)
    aoi = arcpy.GetParameterAsText(1)  # converted from GetParameter
    output = arcpy.GetParameterAsText(2)

    convert_to_features(in_raster, output, extent_features=aoi)
    add_fields(output, fields)

    arr = convert_to_array(output, fields)

    update_with_stats(output, arr, fields)

