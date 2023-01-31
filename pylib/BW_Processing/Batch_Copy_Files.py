# author Chao Chen
# version 0.1
# update date 2019-12-30
# mod date record 2019-12-30


import os


def Batch_Copy_Files(path_in, path_out):
    """
    Find the MHD and its corresponding raw file (.raw or.zraw) in the directory hierarchy, create the same directory hierarchy, and copy the file into the new hierarchy.

    Args:
        path_in : the directory to be searched
        path_out : the directory to be copied to

    Return:
        None

    Example::
            # import os
            # path_in = r"Search address"
            # path_out = r"Copy address"
            # Batch_Copy_Files(path_in,path_out)

    """
    exts = "mhd raw zraw"
    extss = exts.lower().split()

    # 搜索目录下的文件
    for f in os.listdir(path_in):
        path_in_f = os.path.join(path_in, f)
        path_out_f = os.path.join(path_out, f)

        if not os.path.isfile(path_in_f):
            # 创建目录
            if not os.path.exists(path_out_f):
                os.makedirs(path_out_f)
        else:
            if os.path.splitext(f.lower())[1][1:] in extss:  # 文件扩展名符合复制条件，则复制到指定文件夹
                # 文件不存在，或者存在但是大小不同，覆盖
                if not os.path.exists(path_out_f) or (os.path.exists(path_out_f) and (os.path.getsize(path_out_f) != os.path.getsize(path_in_f))):
                    # 2进制文件
                    open(path_out_f, "wb").write(open(path_in_f, "rb").read())
                    print(u"%s 复制完毕" % path_out_f)
                else:
                    print(u"%s 已存在，不重复复制" % path_out_f)

        if os.path.isdir(path_in_f):
            Batch_Copy_Files(path_in_f, path_out_f)


path_in = r"C:\work\data\ADNI\AD"
path_out = r"C:\work\data\ADNI\test"
Batch_Copy_Files(path_in,path_out)