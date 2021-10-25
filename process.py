import glob, os, sys
import argparse

# Catch arguments
parser = argparse.ArgumentParser(description='Get train/test images')
parser.add_argument('-d', '--data-folder', type=str, help='Data folder')
parser.add_argument('-i', '--imgs-folder', type=str, help='Images folder')
parser.add_argument('-f', '--image-format', type=str, help='Image format')

args = parser.parse_args()

data_folder = args.data_folder
imgs_folder = args.imgs_folder
img_format = args.image_format

print('Data folder: ', data_folder)
print('Imgs folder: ', imgs_folder)
print('Img format: ', img_format)

# Root directory
root_dir = os.path.dirname(os.path.abspath(__file__))
print(root_dir)

# Percentage of images to be used for the test set
percentage_test = 20;

# Create and/or truncate train.txt and test.txt
file_train = open(data_folder + '/train.txt', 'w')
file_test = open(data_folder + '/test.txt', 'w')

# Populate train.txt and test.txt
counter = 1
index_test = round(100 / percentage_test)

num_files = len(glob.glob(os.path.join(imgs_folder, "*."+img_format)))
print('Num files founded: ', num_files)

if not num_files:
  print('No files founded. Exit')
  sys.exit()

for pathAndFilename in glob.iglob(os.path.join(imgs_folder, "*."+img_format)):
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    if counter == index_test:
        counter = 1
        file_test.write(imgs_folder + "/" + title + '.'+ img_format + "\n")
    else:
        file_train.write(imgs_folder + "/" + title + '.' + img_format + "\n")
        counter = counter + 1