pyTiVo-Utilities
================

pytivo_metadata.py
------------------

When streaming videos to a TiVo with pyTivo, metadata files are used to supply metadata so the TiVo can show information like the movie description and the year it came out.  pytivo_metadata.py generates those files based on the filename of the video.

Here's an example of a filename:

    The Family Man.m4v

This is the movie "The Family Man," starring Nicolas Cage.  pytivo_metadata.py will query The Open Movie Database API for the movie "The Family Man" and save as much metadata as it can to the file

    The Family Man.m4v.txt

Here's the metadata that pytivo_metadata.py generates:

    title : The Family Man
    vProgramGenre : Comedy
    vProgramGenre : Drama
    vProgramGenre : Romance
    isEpisode : false
    year : 2000
    movieYear : 2000
    description : A fast-lane investment broker, offered the opportunity to see how the other half lives, wakes up to find that his sports car and girlfriend have become a mini-van and wife.  3 commentary tracks available.
    mpaaRating : P3
    vActor : Nicolas Cage
    vActor : Téa Leoni
    vActor : Don Cheadle
    vActor : Jeremy Piven
    vDirector : Brett Ratner
    vWriter : David Diamond
    vWriter : David Weissman

This file will automatically be picked up by pyTivo to push the metadata to TiVo.

See http://pytivo.sourceforge.net/wiki/index.php/Metadata for more info on the metadata file format.

No guarantees are made regarding the correct movie being returned from the API, so maybe do a cursory check of that after running the script. Or don't. Whatever

pytivo_commentary.py
--------------------

If you rip a DVD and include multiple audio tracks in the stream, you can stream each of those tracks via pyTivo by using pytivo_commentary.py.

To denote a commentary track in a video, name the file like so:

    The Family Man (Commentary).m4v

If the movie has more than one commentary, name it like this:

    The Family Man (Commentary x 3).m4v

(Yes, The Family Man, starring Nicolas Cage, does have three commentary tracks.)

pytivo_commentary.py will then generate multiple copies of the video and metadata file (one for each commentary) and add "Commentary #1/2/3" to each title.  The additional video files are only hardlinks to the original, so no additional disk space is needed.

Before using pytivo_commentary.py, add this line to the [Server] section of your pyTivo.conf (and restart the pyTivo service):

    audio_lang=commentary

These scripts were tested with the version of pyTivo: https://github.com/wmcbrine/pytivo/ (as of https://github.com/wmcbrine/pytivo/commit/97c858d64726f9c6c1b117429c03a9f964411df1)