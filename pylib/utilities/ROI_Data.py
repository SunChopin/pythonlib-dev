'''
Script name: Image_Data
Author:@Mingrui
Created:2020/11/20
Last modified: 2020/11/20
Version:1
Description: ROI_Data Class, whitch is used to represent cubes.
'''

class ROI_Base:
    def __init__(self):
        '''
        Input:
        Output:
        Description: Constructor. Need to be initialized afterwards.
        '''
        self._type = ''
        self._name = ''
        self._color = [0, 0, 0]
        self._range = [0, 0, 0, 0, 0, 0] #

    def get_type(self):
        return self._type

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_color(self, color):
        self._color[0] = color[0]
        self._color[1] = color[1]
        self._color[2] = color[2]

    def get_color(self):
        return self._color


class Cube_Data(ROI_Base):
    '''
    Description: This class is used to represent cube data
    '''
    def __init__(self):
        super(Cube_Data, self).__init__()
        self._type = 'Cube'

    def set_range(self, range):
        self._range[0] = range[0]
        self._range[1] = range[1]
        self._range[2] = range[2]
        self._range[3] = range[3]
        self._range[4] = range[4]
        self._range[5] = range[5]

    def get_range(self):
        return self._range


class ROI_Data:
    '''
    Description: This class is used to represent ROI data
    '''

    def __init__(self):
        '''
        Input:
        Output:
        Description: Constructor. Need to be initialized afterwards.
        '''
        self._ROI_list = []

    def append_ROI(self, roi):
        if roi[0] is 'Cube':
            cube = Cube_Data()
            cube.set_name(roi[1])
            cube.set_color(roi[2])
            cube.set_range(roi[3])
            self._ROI_list.append(cube)

    def get_ROIs(self):
        return self._ROI_list

    def get_Cubes(self):
        cube_list = []
        for roi in self._ROI_list:
            if roi.get_type() is 'Cube':
                cube_list.append(roi)
        return cube_list
