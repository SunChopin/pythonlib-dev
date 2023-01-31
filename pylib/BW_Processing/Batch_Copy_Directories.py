# author Chao Chen
# version 0.1
# update date 2019-12-30
# mod date record 2019-12-30


import os


def Batch_Copy_Directories(path_in, path_out):
    """
    Copy the directory hierarchy of the input folder to the target folder and create an empty folder.

    Args:
        path_in : the directory to be searched
        path_out : the directory to be copied to

    Return:
        None

    Example::
            # import os
            # path_in = r"Target address"
            # path_out = r"Copy address"
            # Batch_Copy_Directories(path_in,path_out)

    """
    for f in os.listdir(path_in):
        path_in_f = os.path.join(path_in, f)
        path_out_f = os.path.join(path_out, f)
        if not os.path.isfile(path_in_f):
            if not os.path.exists(path_out_f):
                os.makedirs(path_out_f)
                print(u"%s 目录层次已创建" % path_out_f)
            else:
                print(u"%s 目录层次已存在" % path_out_f)
            if os.path.isdir(path_in_f):
                Batch_Copy_Directories(path_in_f, path_out_f)

