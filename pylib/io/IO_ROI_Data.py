'''
Script name: IO_ROI_Data
Author:@Mingrui
Created:2020/11/20
Last modified: 2020/11/20
Version:1
Description: Read and write *.roi data for displaying data with Anatomy Sktech.
'''

from pylib.utilities.ROI_Data import ROI_Data

def Read_ROI_Data(filename):
    '''
    Input:
        path: string, full path of data to import. Support *.roi
    Output: Image_Data
    Description: Import ROI data in.
    '''


    with open(filename, 'r') as f:
        data = f.readlines()
    Output = ROI_Data()
    ncrntLine = 0
    # 0 检查文件头
    if data[ncrntLine] != '#Anatomy Sketch ROI File\n':
        return -1
    ncrntLine += 1
    # 1 ROI数量
    if data[ncrntLine] != '#NUMBER OF ROIs:\n':
        return -1
    ncrntLine += 1
    NumOfROI = int(data[ncrntLine])
    ncrntLine += 1
    # 2 ROI LIST
    if data[ncrntLine] != '#ROI LIST DEFINITION:\n':
        return -1
    ncrntLine += 1
    for ncrntROI in range(NumOfROI):
        # 2.1 DATA LIST NUMBER
        if data[ncrntLine] != '#ROI LIST NUMBER ' + str(ncrntROI) + ' DEFINITION:\n':
            return -1
        ncrntLine += 1
        # 2.2 data_list_index
        sublist = data[ncrntLine].split(' # ')
        ncrntLine += 1
        if sublist[1] != 'data_list_index\n':
            return -1
        if int(sublist[0]) != ncrntROI:
            return -1
        # 2.3 data_name
        sublist = data[ncrntLine].split(' # ')
        ncrntLine += 1
        if sublist[1] != 'roi_name\n':
            return -1
        roi_name = sublist[0]
        # 2.4 Color
        sublist = data[ncrntLine].split(' # ')
        ncrntLine += 1
        if sublist[1] != 'r_color g_color b_color\n':
            return -1
        subsublist = sublist[0].split(' ')
        cnrtColor = [int(subsublist[0]), int(subsublist[1]), int(subsublist[2])]
        # 2.5 Type
        sublist = data[ncrntLine].split(' # ')
        ncrntLine += 1
        if sublist[1] != 'roi_type\n':
            return -1
        CtrType = int(sublist[0])
        if CtrType == 1:
            # ROIType_Cube
            if data[ncrntLine] != '#ROI Cube DEFINITION:\n':
                return -1
            ncrntLine += 1
            # ROI Range
            sublist = data[ncrntLine].split(' # ')
            ncrntLine += 1
            if sublist[1] != 'Range\n':
                return -1
            subsublist = sublist[0].split(' ')
            crntRange = [float(subsublist[0]), float(subsublist[1]), float(subsublist[2]),
                         float(subsublist[3]), float(subsublist[4]), float(subsublist[5])]
            # Cube end
            if data[ncrntLine] != '#ROI Cube END:\n':
                return -1
            ncrntLine += 1

            crntROI = [CtrType, cnrtColor, crntRange]
            Output.append_ROI(['Cube', roi_name, cnrtColor, crntRange])
        else:
            return -1

    return Output

def Write_ROI_Data(roi_data:ROI_Data, path):
    '''
    Input:
        roi_data: ROI_Data, data to write.
        path: string, full path of data to write. Support *.roi
    Output:
    Description: Write ROI data in various formats.
    '''
    ROI_list = roi_data.get_ROIs()
    with open(path, 'w') as f:
        # 清空原有内容
        f.truncate()
        # 开始写入
        # 1 文件头
        # 1.1 版本
        f.write('#Anatomy Sketch ROI File\n')
        # 1.2 ROI数量
        f.write('#NUMBER OF ROIs:\n')
        f.write(str(len(ROI_list)) + '\n')
        f.write('#ROI LIST DEFINITION:\n')

        # 2 保存各个ROI文件
        for index, current_ROI in enumerate(ROI_list):
            # 2.1.1 文件头
            f.write('#ROI LIST NUMBER ' + str(index) + ' DEFINITION:\n')
            f.write(str(index) + ' # data_list_index\n')
            f.write(current_ROI.get_name() + ' # roi_name\n')
            color = current_ROI.get_color()
            f.write(str(color[0]) + ' ' + str(color[1]) + ' ' + str(color[2]) + ' # r_color g_color b_color\n')
            # 2.1.2 分类保存
            if current_ROI.get_type() is 'Cube':
                f.write('1' + ' # roi_type\n')  # 1表示Cube
                f.write('#ROI Cube DEFINITION:\n')
                range = current_ROI.get_range()
                f.write(str(range[0]) + ' ' + str(range[1]) + ' ' + str(range[2]) + ' ' + str(range[3]) + ' ' +
                        str(range[4]) + ' ' + str(range[5]) + ' # Range\n')
                f.write('#ROI Cube END:\n')

        # 3 写文件尾
        f.write('#\n')
        f.write('#END OF ROI DEFINITION\n')
