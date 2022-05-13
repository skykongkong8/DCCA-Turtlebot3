import pyrealsense2.pyrealsense2 as rs
import time
import json

DS5_product_ids = ["0AD1", "0AD2", "0AD3", "0AD4", "0AD5", "0AF6", "0AFE", "0AFF", "0B00", "0B01", "0B03", "0B07", "0B3A", "0B5C"]

def find_device_that_support_advanced_mode():
    ctx = rs.context()
    ds5_dev = rs.device()
    devices = ctx.query_devices()

    for dev in devices:
        if dev.supports(rs.camera_info.product_id) and str(dev.get_info(rs.camera_info.product_id)) in DS5_product_ids:
            if dev.supports(rs.camera_info.name):
                print(f"Found device that supports advanced mode : {dev.get_info(rs.camera_info.name)}")
            return dev
    raise Exception("No D400 prodyct line device that supports advanced mode was found")

try:
    dev = find_device_that_support_advanced_mode()
    advnc_mode = rs.rs400_advanced_mode(dev)
    print("Advanced mode is", "enabled" if advnc_mode.is_enabled() else "disabled")

    while not advnc_mode.is_enabled():
        print("Trying to enable advanced mode...")
        advnc_mode.toggle_advanced_mode(True)

        print("Sleeping for 5 seconds...")
        time.sleep(5)

        dev = find_device_that_support_advanced_mode()
        advnc_mode = rs.rs400_advanced_mode(dev)
        print("Advanced mode is", "enabled" if advnc_mode.is_enabled() else "disabled")

    # Current Values are :
    print(f"Depth Control : \n{advnc_mode.get_depth_control()}")
    print(f"RSM: \n{advnc_mode.get_rsm()}")
    print(f"RAU Support Vector Control: \n{advnc_mode.get_rau_support_vector_control()}")
    print(f"Color Control : \n{advnc_mode.get_color_control()}")
    print(f"RAU Thresholds Control : \n{advnc_mode.get_rau_thresholds_control()}")
    print(f"SLO Color Thresholds Control : \n{advnc_mode.get_slo_color_thresholds_control()}")
    print(f"SLO Penalty Control : \n{advnc_mode.get_slo_penalty_control()}")
    print(f"HDAD : \n{advnc_mode.get_hdad()}")
    print(f"Color Correction : \n{advnc_mode.get_color_correction()}")
    print(f"Depth Table : \n{advnc_mode.get_depth_table()}")
    print(f"Auto Exposure Control : \n{advnc_mode.get_ae_control()}")
    print(f"Census : \n{advnc_mode.get_census()}")

    
    # To get the minimum and the maximum value of each control use the mode value:
    query_min_values_mode = 1
    query_max_values_mode = 2
    current_std_depth_control_group = advnc_mode.get_depth_control()
    min_std_depth_control_group = advnc_mode.get_depth_control(query_min_values_mode)
    max_std_depth_control_group = advnc_mode.get_depth_control(query_max_values_mode)

    print(f"Depth Control Min Values : \n{min_std_depth_control_group}")
    print(f"Depth Control Max Values : \n{max_std_depth_control_group}")


    # set some control with new value (in this case, we used a median value for representation)

    # example : set new depth control threshold
    current_std_depth_control_group.scoreThreshA = int((max_std_depth_control_group.scoreThreshA - min_std_depth_control_group.scoreThreshA) / 2)
    advnc_mode.set_depth_control(current_std_depth_control_group)
    print(f"After Setting new value, Depth Control: \n{advnc_mode.get_depth_control()}")

    # Serialize all contros to a Json String : rather than doing it individually, we can set certain 'mode' with Json format
    serialized_string = advnc_mode.serialize_json()
    print(f"Controls as JSON : \n{serialized_string}")
    as_json_object = json.loads(serialized_string)

    # no need utf-8 unicode conversion since we are using python3.6

    # JSON parser requires double-quotes for the json object so we need to replace the single quote of the pythonic json to double-quotes
    json_string = str(as_json_object).replace("'", '\"')
    advnc_mode.load_json(json_string)


except Exception as e:
    print(e)
finally:
    pass