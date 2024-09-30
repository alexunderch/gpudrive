"""
Description: This script is used to process the data from the tfrecord files and mark the vehicles with unsolvable trajectories as static vehicles.
"""
import os
import json
from tqdm import tqdm

import logging

logging.basicConfig(level=logging.DEBUG)


def process_tfrecord_file(file_path, unsolvable_vehicle_ids=None):
    """
    Process the file (i.e. mark the vehicles with unsolvable trajectories as static).
    """
    with open(file_path, "r") as f:
        tfrecord_dict = json.load(f)

    # All goals are solvable, so we mark all vehicles as not static
    if unsolvable_vehicle_ids is None or len(unsolvable_vehicle_ids) == 0:
        for obj_idx, obj in enumerate(tfrecord_dict.get("objects", [])):
            if obj.get("type") in ["vehicle", "pedestrian", "bicycle"]:
                obj["mark_as_static"] = False
    else:
        logging.debug(
            f"File has {len(tfrecord_dict.get('objects', []))} agents, {len(unsolvable_vehicle_ids)} of which have unsolvable goals."
        )
        # Iterate through the objects in the file
        for obj_idx, obj in enumerate(tfrecord_dict.get("objects", [])):
            logging.debug(f"obj_idx: {obj_idx}")
            # Check if the object is something we can control
            if obj.get("type") in ["vehicle", "pedestrian", "bicycle"]:
                # TODO(dc): Check if this logic holds. This assumes that the vehicle order is deterministic
                if obj_idx in unsolvable_vehicle_ids:
                    obj["mark_as_static"] = True
                else:
                    obj["mark_as_static"] = False

    return tfrecord_dict


def mark_unsolvable_trajectories(
    tfrecord_files_path, unsolvable_vehicles_data_path, save_path
):

    # Sort and order the traffic scenes
    traffic_scenes = sorted(os.listdir(tfrecord_files_path))

    # Load the unsolvable vehicles data
    with open(unsolvable_vehicles_data_path, "r") as f:
        files_with_unsolvable_goals = json.load(f)

    for file_name in tqdm(traffic_scenes):

        if file_name.endswith(".json") and file_name.startswith("tfrecord"):

            file_path = os.path.join(tfrecord_files_path, file_name)

            # Check if we can find this file in the unsolvable vehicles data
            if file_name in files_with_unsolvable_goals:
                unsolvable_vehicle_ids = files_with_unsolvable_goals[file_name]
            else:  # All goals are solvable
                unsolvable_vehicle_ids = None

            processed_file = process_tfrecord_file(
                file_path, unsolvable_vehicle_ids
            )

            # Save the processed file
            output_file_path = os.path.join(save_path, file_name)
            with open(output_file_path, "w") as f:
                json.dump(processed_file, f, indent=4)


if __name__ == "__main__":

    data_path_vehs_with_unsolvable_trajectories = (
        "mark_as_static_json_no_tl_train.json"
    )
    tfrecord_files_path = "data/formatted_json_v2_no_tl_train"
    save_path = "data/formatted_json_v2_no_tl_train_processed"

    mark_unsolvable_trajectories(
        tfrecord_files_path=tfrecord_files_path,
        unsolvable_vehicles_data_path=data_path_vehs_with_unsolvable_trajectories,
        save_path=save_path,
    )
