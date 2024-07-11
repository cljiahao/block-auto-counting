import os


class Directory:
    """
    Instantiate Directories in Project
    """

    src_dir = os.path.dirname(os.path.dirname(__file__))
    base_dir = os.path.dirname(src_dir)

    log_dir = os.path.join(base_dir, "log")

    data_dir = os.path.join(base_dir, "data")
    excel_dir = os.path.join(data_dir, "excel")
    prass_dir = os.path.join(data_dir, "prass")

    images_dir = os.path.join(base_dir, "images")
    acc_dir = os.path.join(images_dir, "acc")
    block_dir = os.path.join(images_dir, "block")
    trouble_dir = os.path.join(images_dir, "trouble")


dire = Directory()
