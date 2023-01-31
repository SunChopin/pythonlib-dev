import pylib
import SimpleITK as sitk
path = r'id1.nii.gz'
img, array = pylib.ReadImage(path)
img = pylib.downsample(img, [96, 96, 96]) 
output_path = r'downsampled.nii.gz'
sitk.WriteImage(img, output_path)