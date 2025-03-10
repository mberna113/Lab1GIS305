import arcpy


def setup():
    workS = r"C:\Users\micha\Desktop\School\GIS_305_Programming_forGIS\Lab1\Lab1.gdb"
    arcpy.env.workspace = workS
    arcpy.env.overwriteOutput = True




def buffer(layer_name, buff_dist):
    #buffer the incoming layer by the buffer distance
    output_buffer_layer_name = f"buf_{layer_name}"
    print(f"Starting buffer on {layer_name}..........")

    arcpy.analysis.Buffer(layer_name, output_buffer_layer_name, buff_dist, "FULL", "ROUND", "ALL")

    print(f"Completed buffer on {output_buffer_layer_name}..........")


def intersect():

    print(f"Creating the {output_intersect_layer_name} layer..........")
    arcpy.analysis.Intersect(intersect_layer_list, output_intersect_layer_name)
    print(f"Created the {output_intersect_layer_name} layer..........")


def spatial_join():
    print("Starting spatial join..........")
    arcpy.analysis.SpatialJoin("Addresses", output_intersect_layer_name, output_spatial_join_layer_name)
    print("Completed spatial join..........")

def select_and_count():
    print("Starting selection of at-risk addresses..........")
    arcpy.analysis.Select(output_spatial_join_layer_name, at_risk, "Join_Count = 1")
    print("Completed selection of at-risk addresses..........")
    count = arcpy.GetCount_management(at_risk)
    print(f"\n\nThe number of addresses that are at-risk with this are: {count[0]}\n\n")


if __name__ == "__main__":
    # initiate setup
    setup()

    # buffer the four main features
    buffer_layer_list = ["Mosquito_Larval_Sites", "Wetlands", "Lakes_and_Reservoirs___Boulder_County", "OSMP_Properties"]
    for layer in buffer_layer_list:
        user_dist = input(f"Buffer distance in feet for {layer}: ")
        buff_dist = f"{user_dist} feet"
        buffer(layer, buff_dist)

    # intersect all buffered features
    intersect_layer_list = ["buf_Mosquito_Larval_Sites", "buf_Wetlands", "buf_Lakes_and_Reservoirs___Boulder_County", "buf_OSMP_Properties"]
    output_intersect_layer_name = input("Intersected Layer name: ")
    intersect()

    # spatial join to addresses
    output_spatial_join_layer_name = input("Joined Addresses Layer name: ")
    spatial_join()

    # Select and print the number of addresses
    at_risk = "At_Risk_Addresses"
    select_and_count()


    # Add the new address points to the map for analysis
    # add project C:\Users\micha\Desktop\School\GIS_305_Programming_forGIS\Lab1\Lab1.aprx
    proj_path = r"C:\Users\micha\Desktop\School\GIS_305_Programming_forGIS\Lab1"
    aprx = arcpy.mp.ArcGISProject(rf"{proj_path}\Lab1.aprx")

    map_doc = aprx.listMaps()[0]
    map_doc.addDataFromPath(rf"{proj_path}\Lab1.gdb\{output_spatial_join_layer_name}")
    aprx.save()





#Notes
# mosq = "Mosquito_Larval_Sites"
# wetl = "Wetlands"
# lakr = "Lakes_and_Reservoirs___Boulder_County"
# osp = "OSMP_Properties"
#"Join_Count = 1"