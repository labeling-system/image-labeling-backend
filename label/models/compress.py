import os
import sys
import cv2
from PIL import Image

def compressJPEG(file, verbose=False):
	filepath = os.path.join(os.getcwd(), file)
	oldsize = os.stat(filepath).st_size
	print(oldsize)
	picture = Image.open(filepath)
	dim = picture.size
	
	#set quality= to the preferred quality. 
	#I found that 85 has no difference in my 6-10mb files and that 65 is the lowest reasonable number
	print(file)
	picture.save("Compressed_"+file,"JPEG",optimize=True,quality=10) 
	# picture.save("Compressed_"+file,"PNG",optimize=True,compress_level=9) 
	
	newsize = os.stat(os.path.join(os.getcwd(),"Compressed_"+file)).st_size
	print(newsize)
	percent = (oldsize-newsize)/float(oldsize)*100
	if (verbose):
		print ("File compressed from {0} to {1} or {2}%".format(oldsize,newsize,percent))
	return percent

def compressPNG(file, verbose=False):
	filepath = os.path.join(os.getcwd(), file)
	oldsize = os.stat(filepath).st_size
	print(oldsize)
	picture = Image.open(filepath)
	dim = picture.size
	
	#set quality= to the preferred quality. 
	#I found that 85 has no difference in my 6-10mb files and that 65 is the lowest reasonable number
	print(file)
	picture.save("Compressed_"+file,"PNG",optimize=True) 
	# picture.save("Compressed_"+file,"PNG",optimize=True,compress_level=9) 
	
	newsize = os.stat(os.path.join(os.getcwd(),"Compressed_"+file)).st_size
	print(newsize)
	percent = (oldsize-newsize)/float(oldsize)*100
	if (verbose):
		print ("File compressed from {0} to {1} or {2}%".format(oldsize,newsize,percent))
	return percent

# def main():
# 	verbose = False
# 	#checks for verbose flag
# 	if (len(sys.argv)>1):
# 		if (sys.argv[1].lower()=="-v"):
# 			verbose = True

# 	#finds present working dir
# 	pwd = os.getcwd()

# 	tot = 0
# 	num = 0
# 	for file in os.listdir(pwd):
# 		print(os.path.splitext(file)[1].lower())

# 		if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg'):
# 			num += 1
# 			tot += compressJPEG(file, verbose)

# 		if os.path.splitext(file)[1].lower() in ('.png'):
# 			num += 1
# 			tot += compressPNG(file, verbose)

# 	print ("Average Compression: %d" % (float(tot)/num))
# 	print ("Done")

# if __name__ == "__main__":
# 	main()
