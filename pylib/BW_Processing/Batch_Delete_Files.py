# author Chao Chen
# version 0.1
# update date 2019-12-30
# mod date record 2019-12-30


import os


def Batch_Delete_Files(path, suffix='mhd raw zraw'):
    """
    Batch deletes the file with the specified suffix.The default is '.mhd' and the corresponding original file (.raw or.zraw) is deleted.

    Args:
        path : the input folder path
        suffix(Optional) : File suffix name,default = 'mhd raw zraw'

    Return:
        None

    Example::
            # import os
            # Path = r"file_path"
            # Batch_Delete_Files(Path)

    """
    extss = suffix.lower().split()  # 默认以空格为分隔符将多个文件扩展名字符串分为单个扩展名字符串并小写
    for f in os.listdir(path):  # 搜索目录下的文件
        paths = os.path.join(path, f)
        if os.path.splitext(f.lower())[1][1:] in extss:  # 文件扩展名符合删除条件，则删除
            os.remove(paths)
            print(u"%s 删除完毕" % paths)
        if os.path.isdir(paths):
            Batch_Delete_Files(paths, suffix)




