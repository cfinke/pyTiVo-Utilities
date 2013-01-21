#!/usr/bin/env python

import sys
import os
import re
import pytivo_utilities

def generate_commentary_streams(video_dir):
	"""Create a second (hardlinked) video file for each commentary track."""
	initial_directory = os.getcwd()
	
	try:
		os.chdir(video_dir)
		
		for dirname, dirnames, filenames in os.walk('.'):
			for subdir in dirnames:
				generate_commentary_streams(subdir)
			
			for filename in filenames:
				# All non-text files are assumed to be videos.
				if filename.endswith(".txt"):
					continue
				
				extension = os.path.splitext(filename)[1]
				
				if not extension:
					continue
				
				if " - Commentary #" in filename:
					# Already generated by this tool.
					continue
				
				title, file_comments = pytivo_utilities.parse_filename(filename)
				
				if not file_comments:
					# No commentary tracks noted
					continue
				
				metadata_filename = filename + ".txt"
				
				if os.path.exists(metadata_filename):
					metadata = pytivo_utilities.parse_metadata_text(open(metadata_filename).read().decode("utf-8"))
				else:
					metadata = {}
				
				if 'title' not in metadata:
					metadata['title'] = [ title ]
				
				commentary_count = 0
				
				file_comments = file_comments.split(', ')
				
				for comment in file_comments:
					if comment.find("Commentary") == 0:
						if "Commentary" == comment:
							commentary_count = 1
						else:
							commentary_count = int(comment.split(' x ')[1])
				
				original_title = metadata['title'][0]
				
				for i in range(1, commentary_count + 1):
					commentary_filename = '%s - Commentary #%s%s' % (title, i, extension)
					
					if os.path.exists(commentary_filename):
						continue
					
					os.link(filename, commentary_filename)
					
					metadata['title'] = '%s - Commentary #%s' % (original_title, i)
					
					commentary_metadata_file_handle = open(commentary_filename + ".txt", 'w')
					commentary_metadata_file_handle.write((u"%sOverride_mapAudio 0.%s : commentary\n" % (pytivo_utilities.metadata_dict_to_string(metadata), i + 1)).encode('utf8'))
					commentary_metadata_file_handle.close()
	finally: 
		os.chdir(initial_directory)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print "Usage: pytivo_commentary.py dir1 dir2 dir3..."
		sys.exit()
	
	dirs = sys.argv[1:]

	for video_dir in dirs:
		generate_commentary_streams(video_dir)