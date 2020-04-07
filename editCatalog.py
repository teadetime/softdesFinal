def pickle_data(file_path, data, overwrite):
    """
    Pickle a specific piece of data in binary. Can be pickled at any directory, will not overwrite current data unless
        overwite is specified
    :param file_path: Npath to file to be pickled. Can contain just a file name to pickle in CWD
    :param data: The data that will be pickled
    :param overwrite: Boolean that indicates whether the file should be overwritten even if it exists
    :return: #TODO Nothing currently should return True if succesful
    """
    if not os.path.exists(file_path) or overwrite:
        f = open(file_path, "wb")
        dump(data, f)
        f.close()


def load_pickle_data(file_path):
    """
    Unpickles data stored at a given file path (or filename in CWD) and returns it
    :param file_path: path to file that is to be un-pickled (can be file name for items in CWD)
    :return: Returns None or that data that was stored in pickle form at the location
    """
    # Initialize data so that None is returned if file path doesn't work
    pickled_data = None
    if os.path.exists(file_path):
        f = open(file_path, "rb+")
        pickled_data = load(f)
        f.close()
    return pickled_data

catalog = load_pickle_data('catalog_picle')
print(catalog)