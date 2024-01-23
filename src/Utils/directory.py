import os


class Directory:

    """
    Instantiate Directories in Project
    """

    def __init__(self):
        self.path_src = os.path.dirname(os.path.dirname(__file__))
        self.path_base = os.path.dirname(self.path_src)

        path_data = os.path.join(self.path_base, "data")
        self.path_excel = os.path.join(path_data, "excel")
        self.path_prass = os.path.join(path_data, "prass")

        path_images = os.path.join(self.path_base, "images")
        self.path_acc = os.path.join(path_images, "acc")
        self.path_block = os.path.join(path_images, "block")
        self.path_trouble = os.path.join(path_images, "trouble")


dire = Directory()
