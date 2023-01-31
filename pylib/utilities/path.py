# author Ye Han
# version 0.1
# update date 2019-12-16
# mod date record 2019-12-16 version 0.1 Ye Han

import os

def Get_Abs_Dir_Names(input_path):
    r"""
    Get all the absolute file path and name in the folder.

    Args:
        input_path (str): The folder you want to operate.

    Return:
        file_name_list (list): a list including all the absolute file path and name.
    """
    file_name_list = []
    for root_name, dir_name, file_names in os.walk(input_path):
        for file_name in file_names:
            file_name_list.append(os.path.join(root_name, file_name))
    return file_name_list


def Count_File_Nums(input_path):
    r"""
    Count the numbers of the files in the folder.

    Args:
        input_path (str): The folder you want to count the numbers of the file. 

    Return:
        nums (int): the numbers of the files in the folder.
    """

    file_name_list = Get_Abs_Dir_Names(input_path)
    nums = len(file_name_list)
    return nums


def Get_File_Name(file_path):
    r"""
    Get the filename (without suffix) and filename (with suffix) from the file path.

    Args:
        file_path (str): file path 

    Return:
        name_without_suffix, name_with_suffix (str)
    """

    """
    从文件路径获取文件名（不带后缀）和文件名（带后缀）。
    :param path: 路径
    :return: list
    """
    path_name, file_name = os.path.split(file_path)  # 路径名，文件名（带后缀）
    name_without_suffix = file_name
    name_with_suffix = file_name.split('.')[0]  # 文件名（不带后缀）
    return name_without_suffix, name_with_suffix


if __name__ == '__main__':
    input_path = r'C:\Program Files'
    file_name_list = Get_Abs_Dir_Names(input_path)
    print(Count_File_Nums(input_path))
