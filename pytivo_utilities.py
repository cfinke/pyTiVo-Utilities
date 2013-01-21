import os
import re

def metadata_dict_to_string(metadata):
	"""Convert a dict of key: value pairs to a string that follows TiVo's metadata format."""
	metadata_text = ""
	
	for (field, value) in metadata.items():
		if type(value) is list:
			for subvalue in value:
				metadata_text += "%s : %s\n" % (field, subvalue)
		else:
			metadata_text += "%s : %s\n" % (field, value.strip())

	return metadata_text

def movie_rating_code_from_rating(rating):
	"""Convert an Open Movie Database API rating code to a TiVo metadata rating code."""
	rating_codes = {
		'G' : 'G1',
		'PG' : 'P2',
		'PG-13' : 'P3',
		'R' : 'R4',
		'X' : 'X5',
		'NC-17' : 'N6',
		'NR' : 'N8'
	}
	
	if rating in rating_codes:
		return rating_codes[rating]
	else:
		return ''

def parse_metadata_text(metadata_text):
	"""Convert a metadata file's contents to a dict."""
	metadata_lines = metadata_text.split("\n")
	metadata_dict = {}
	
	for line in metadata_lines:
		if " : " not in line:
			continue
		
		key, value = line.split(" : ", 1)
		
		if key not in metadata_dict:
			metadata_dict[key] = []
		
		metadata_dict[key].append(value)
	
	return metadata_dict

def parse_filename(filename):
	"""Parse out the video title and any comments from a filename. Format: This is the Title (These are some comments).avi"""
	title = os.path.splitext(filename)[0]
	
	file_comments = re.search('\(([^\)]+)\)', filename)
	
	if file_comments:
		file_comments = file_comments.group(1)
		title = title.replace("(%s)" % file_comments, '')
	else:
		file_comments = None
	
	title = title.strip()
	
	return (title, file_comments)
