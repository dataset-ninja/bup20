import csv
import os
import shutil
from collections import defaultdict
from urllib.parse import unquote, urlparse

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import get_file_name, get_file_name_with_ext
from supervisely.io.json import load_json_file
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    dataset_path = "/home/alex/DATASETS/TODO/BUP20/CKA_sweet_pepper_2020_summer"
    batch_size = 30
    ann_path = "/home/alex/DATASETS/TODO/BUP20/CKA_sweet_pepper_2020_summer/CKA_sweet_pepper_2020_summer.json"
    group_tag_name = "im id"
    depth_folder = "depth"
    odom_name = "odometry.csv"

    def create_ann(image_path):
        labels = []
        tags = []

        group_tag = sly.Tag(group_tag_meta, get_file_name(image_path))
        tags.append(group_tag)

        date_meta = date_to_meta.get(image_path.split("/")[-3])
        date = sly.Tag(date_meta)
        tags.append(date)

        row_meta = meta.get_tag_meta(image_path.split("/")[-2])
        row = sly.Tag(row_meta)
        tags.append(row)

        # image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = 1280
        img_wight = 720

        odom_value = name_to_odom[get_file_name(image_path)]
        odom = sly.Tag(odom_meta, value=odom_value)
        tags.append(odom)

        milliseconds_value = image_name_to_milliseconds.get(get_file_name_with_ext(image_path))
        if milliseconds_value is not None:
            milliseconds = sly.Tag(milliseconds_meta, value=int(milliseconds_value))
            tags.append(milliseconds)

        ann_data = image_name_to_ann_data[get_file_name_with_ext(image_path)]
        if len(ann_data) > 0:
            for curr_ann_data in ann_data:
                category_id = curr_ann_data[0]
                obj_class = idx_to_obj_class.get(category_id)
                if obj_class is not None:
                    creator_str = curr_ann_data[4]
                    creator_value = creator_to_value[creator_str]
                    creator = sly.Tag(creator_meta, value=creator_value)
                    milliseconds_value = int(curr_ann_data[3])
                    milliseconds = sly.Tag(milliseconds_meta, value=milliseconds_value)
                    polygons_coords = curr_ann_data[1]

                    exterior = []
                    for coords in polygons_coords:
                        for i in range(0, len(coords), 2):
                            exterior.append([int(coords[i + 1]), int(coords[i])])
                        if len(exterior) < 3:
                            continue
                    if len(exterior) > 3:
                        poligon = sly.Polygon(exterior)
                        label_poly = sly.Label(poligon, obj_class, tags=[milliseconds, creator])
                        labels.append(label_poly)

                    bbox_coord = curr_ann_data[2]
                    rectangle = sly.Rectangle(
                        top=int(bbox_coord[1]),
                        left=int(bbox_coord[0]),
                        bottom=int(bbox_coord[1] + bbox_coord[3]),
                        right=int(bbox_coord[0] + bbox_coord[2]),
                    )
                    label_rectangle = sly.Label(rectangle, obj_class, tags=[milliseconds, creator])
                    labels.append(label_rectangle)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    ann = load_json_file(ann_path)

    # pepper_kp = sly.ObjClass("pepper kp", sly.AnyGeometry, color=(0, 0, 255))
    red = sly.ObjClass("red", sly.AnyGeometry, color=(199, 33, 28))
    yellow = sly.ObjClass("yellow", sly.AnyGeometry, color=(255, 247, 0))
    green = sly.ObjClass("green", sly.AnyGeometry, color=(0, 255, 0))
    # mixed = sly.ObjClass("mixed", sly.AnyGeometry, color=(255, 0, 255))
    mixed_red = sly.ObjClass("mixed red", sly.AnyGeometry, color=(255, 102, 0))
    mixed_yellow = sly.ObjClass("mixed yellow", sly.AnyGeometry, color=(209, 196, 21))

    idx_to_obj_class = {
        # 11: pepper_kp,
        12: red,
        13: yellow,
        14: green,
        # 15: mixed,
        17: mixed_red,
        18: mixed_yellow,
    }

    row2_meta = sly.TagMeta("row2", sly.TagValueType.NONE)
    row3_meta = sly.TagMeta("row3", sly.TagValueType.NONE)
    row4_meta = sly.TagMeta("row4", sly.TagValueType.NONE)
    row5_meta = sly.TagMeta("row5", sly.TagValueType.NONE)
    row6_meta = sly.TagMeta("row6", sly.TagValueType.NONE)
    date09_meta = sly.TagMeta("2020-09-24", sly.TagValueType.NONE)
    date10_meta = sly.TagMeta("2020-10-01", sly.TagValueType.NONE)
    milliseconds_meta = sly.TagMeta("milliseconds", sly.TagValueType.ANY_NUMBER)
    odom_meta = sly.TagMeta("odometry", sly.TagValueType.ANY_STRING)
    creator_meta = sly.TagMeta("labeller", sly.TagValueType.ANY_STRING)
    # claussmitt_meta = sly.TagMeta("claus smitt", sly.TagValueType.NONE)
    # ramsay_meta = sly.TagMeta("ramsay", sly.TagValueType.NONE)
    # chris_mccool_meta = sly.TagMeta("chris mccool", sly.TagValueType.NONE)
    # agr_meta = sly.TagMeta("agr user1", sly.TagValueType.NONE)
    # michallhal_meta = sly.TagMeta("michallhal", sly.TagValueType.NONE)
    group_tag_meta = sly.TagMeta(group_tag_name, sly.TagValueType.ANY_STRING)

    date_to_meta = {"20200924": date09_meta, "20201001": date10_meta}

    creator_to_value = {
        "claussmitt": "claus smitt",
        "ramsay": "ramsay",
        "chris_mccool": "chris mccool",
        "AgR_User_1": "agr user1",
        "michallhal": "michallhal",
    }

    meta = sly.ProjectMeta(
        tag_metas=[
            row2_meta,
            row3_meta,
            row4_meta,
            row5_meta,
            row6_meta,
            date09_meta,
            date10_meta,
            milliseconds_meta,
            odom_meta,
            creator_meta,
            # claussmitt_meta,
            # ramsay_meta,
            # chris_mccool_meta,
            # agr_meta,
            # michallhal_meta,
            group_tag_meta,
        ],
        obj_classes=list(idx_to_obj_class.values()),
    )
    api.project.update_meta(project.id, meta.to_json())
    api.project.images_grouping(id=project.id, enable=True, tag_name=group_tag_name)

    image_id_to_name = {}
    image_name_to_milliseconds = {}
    image_name_to_ann_data = defaultdict(list)
    for curr_image_info in ann["images"]:
        image_id_to_name[curr_image_info["id"]] = curr_image_info["file_name"]
        image_name_to_milliseconds[curr_image_info["file_name"]] = curr_image_info["milliseconds"]

    for curr_ann_data in ann["annotations"]:
        image_id = curr_ann_data["image_id"]
        image_name_to_ann_data[image_id_to_name[image_id]].append(
            [
                curr_ann_data["category_id"],
                curr_ann_data["segmentation"],
                curr_ann_data["bbox"],
                curr_ann_data["milliseconds"],
                curr_ann_data["creator"],
            ]
        )
    train_pathes = [
        "20200924/row2",
        "20200924/row3",
        "20201001/row2",
        "20201001/row3",
        "20200924/row1",
    ]
    val_pathes = ["20200924/row4", "20201001/row4"]
    test_pathes = ["20200924/row5", "20201001/row5", "20201001/row6"]

    ds_name_to_pathes = {"train": train_pathes, "val": val_pathes, "test": test_pathes}

    for ds_name, ds_pathes in ds_name_to_pathes.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        for ds_path in ds_pathes:
            rgb_images_path = os.path.join(dataset_path, ds_path)
            images_names = [
                im_name
                for im_name in os.listdir(rgb_images_path)
                if im_name in image_name_to_ann_data.keys()
            ]
            depth_images_path = os.path.join(rgb_images_path, depth_folder)
            odom_path = os.path.join(rgb_images_path, odom_name)
            name_to_odom = {}
            with open(odom_path, "r") as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    name_to_odom[row[0]] = row[3]

            progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

            for imgs_names_batch in sly.batched(images_names, batch_size=batch_size):
                images_pathes_batch = []
                images_names_batch = []
                for im_name in imgs_names_batch:
                    images_names_batch.append(im_name)
                    images_pathes_batch.append(os.path.join(rgb_images_path, im_name))

                    depth_name = "depth_" + im_name
                    images_names_batch.append(depth_name)  # for depth
                    images_pathes_batch.append(
                        os.path.join(depth_images_path, im_name)
                    )  # for depth

                img_infos = api.image.upload_paths(
                    dataset.id, images_names_batch, images_pathes_batch
                )
                img_ids = [im_info.id for im_info in img_infos]

                anns = []
                for i in range(0, len(images_pathes_batch), 2):
                    ann = create_ann(images_pathes_batch[i])
                    anns.extend([ann, ann])
                api.annotation.upload_anns(img_ids, anns)

                progress.iters_done_report(len(images_names_batch))

    return project
