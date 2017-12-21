import os
import json
import requests
from time import sleep

print("\n=================")
print("Shadow Cat v1.0.0")
print("=================\n")

sleep(2)

#Laod Config
config_file = open("config.json", "r")
config = json.load(config_file)
config_file.close()

for video in os.listdir(config["input_folder"]):

	input_path = config["input_folder"] + "/" + video
	output_path = config["output_folder"] + "/" + os.path.splitext(video)[0] + "-compressed.mp4"
	quality = config["quality"]
	resolution = config["resolution"]

	#Skip if `video` is directory
	if(os.path.isdir(input_path)):
		continue

	#Skip if `video` is not a video file
	if(os.path.splitext(video)[1] not in (".mp4", ".mov", ".webm")):
		continue

	#Compress video
	print("Compressing " + video + "...")

	os.system("HandBrakeCLI -i \"%s\" -o \"%s\" -q %s -l %s" % (input_path, output_path, quality, resolution))

	sleep(1)

	#Upload to Streamable
	print("Uploading to Streamable...")

	r = requests.post("https://api.streamable.com/upload",
		auth=(config["username"], config["password"]),
		files={'file': open(output_path, 'rb')}
	)
	
	if(r.status_code != 200):
		continue

	#Delete original video
	if(config["delete_original_video"]):
		print("Deleting original video...")
		os.remove(input_path)

	#Delete compressed video
	if(config["delete_compressed_video"]):
		print("Deleting compressed video...")
		os.remove(output_path)

	print(video + " has completed")

print("\nAll done!")
input("Press ENTER key to exit...")
