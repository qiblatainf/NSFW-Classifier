# script to download the dataset from GoogleDrive; when asked directory name enter: data

# echo "Enter Directory Name!"
# read dirname
dirname = "data"

# if [ ! -d ./$dirname]
# then
#     echo "Folder doesn't exist! Creating now..."
#     mkdir ./$dirname
#     echo "Folder Created!"
# else
#     echo "Folder Exists!"
# fi
mkdir ./$dirname
gdown --id 1rHcOExB5A1zoO-accdvPxZH15OlB39WS
bsdtar --strip-components=1 -xvf data.zip -C data
