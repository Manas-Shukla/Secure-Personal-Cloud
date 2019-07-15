import magic

audio=['.aif','.cda','mid','.midi','.mp3','.mpa','.ogg','.wav','.wma','.wpl']
compressed=['.7z','.arj','.deb',',pkg','.rar','..rpm','.gz','.z','.zip','.iso']
database=['.csv','.dat','.db','.dbf','.log','.mdb','.sav','.sql','.tar','.xml']
exectables=['.apk','.bat','.exe','.cgi','.com','.gadget','.jar','.py','.wsf']
images=['.ai','.bmp','.gif','.ico','.jpeg','.jpg','.png','.ps','.psd','.svg','.tif','.tiff']
videos=['.3g2','.3gp','.avi','.flv','.h264','.m4v','.mkv','.mov','.mp4','.mpg','.mpeg','.rm','.swf','.vob','.wmv']


def get_type(ext):
    if ext in audio:
        return "audio"
    elif ext in compressed:
        return "compressed"
    elif ext in database:
        return "database"
    elif ext in exectables:
        return "executable"
    elif ext in images:
        return "images"
    elif ext in videos:
        return "videos"
    else:
        return "Text/PDF"

def detect_type(filepath):
    extension=""
    str=filepath[::-1]
    for c in str:
        if(c == '.'):
            break
        extension=extension+c
    extension=extension+"."
    extension=extension[::-1]
    info=magic.from_file(filepath)
    type=get_type(extension)
    return (type, info)
