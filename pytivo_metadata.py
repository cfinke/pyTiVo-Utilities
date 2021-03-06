#!/usr/bin/env python

# pytivo_metadata.py utilizes the Open Movie Database API, by Brian Fritz. http://www.omdbapi.com/

import sys
import os
import re
import urllib, urllib2
import json
import pytivo_utilities

def generate_metadata_files(video_dir):
	"""Generate TiVo metadata files for all videos in a directory."""
	
	for dirname, dirnames, filenames in os.walk(video_dir):
		for filename in filenames:
			# All non-text files are assumed to be videos.
			if filename.endswith(".txt"):
				continue
			
			extension = os.path.splitext(filename)[1]
			
			if not extension:
				continue
			
			metadata_filename = filename + ".txt"
			
			if os.path.exists(os.path.join(dirname, metadata_filename)):
				continue
			
			title, file_comments = pytivo_utilities.parse_filename(filename)
			
			metadata = {}
			metadata['title'] = title
			metadata['vProgramGenre'] = 'Movies'
			metadata['isEpisode'] = 'false'
			
			request = urllib2.Request("http://www.omdbapi.com/?%s" % urllib.urlencode( { 't' : title } ))
			opener = urllib2.build_opener()
			f = opener.open(request)
			api_data = json.load(f)
			
			if api_data and api_data['Response'] == 'True':
				metadata['title'] = api_data['Title']
				metadata['year'] = metadata['movieYear'] = api_data['Year']
				metadata['description'] = api_data['Plot']
				metadata['mpaaRating'] = pytivo_utilities.movie_rating_code_from_rating(api_data['Rated'])
				
				multiple_value_keys = { "Actors" : "vActor", "Director" : "vDirector", "Writer" : "vWriter", "Genre" : "vProgramGenre" }
				
				for (json_field, metadata_field) in multiple_value_keys.items():
					if json_field in api_data:
						metadata[metadata_field] = []
					
						for entry in api_data[json_field].split(', '):
							metadata[metadata_field].append(entry)
			
			metadata_file_handle = open(os.path.join(dirname, metadata_filename), 'w')
			metadata_file_handle.write(pytivo_utilities.metadata_dict_to_string(metadata).encode('utf8'))
			metadata_file_handle.close()

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print "Usage: pytivo_metadata.py dir1 dir2 dir3..."
		sys.exit()
	
	dirs = sys.argv[1:]

	for video_dir in dirs:
		generate_metadata_files(video_dir)