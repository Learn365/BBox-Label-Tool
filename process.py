import glob, os
import io

# Current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
obj='nlut_1'
cls='001'
current_dir = os.path.join(current_dir,obj,'images',cls)
# Directory where the data will reside, relative to 'darknet.exe'
path_data = './data/{0}/images/{1}/'.format(obj,cls)

# Percentage of images to be used for the test set
percentage_test = 10;

# Create and/or truncate train.txt and test.txt
file_train = io.open('{0}_train.txt'.format(obj), 'a+',newline="\n")  
file_test = io.open('{0}_test.txt'.format(obj), 'a+',newline="\n")

# Populate train.txt and test.txt
counter = 1  
index_test = round(100 / percentage_test)  
for pathAndFilename in glob.iglob(os.path.join(current_dir, "*.jpg")):  
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    if counter == index_test:
        counter = 1
        file_test.write(path_data + title + '.jpg' + "\n")
    else:
        file_train.write(path_data + title + '.jpg' + "\n")
        counter = counter + 1