import os, random, re, subprocess, shlex, atexit
TMP_DIR = os.popen('mktemp -d').read().replace('\n', '')

atexit.register(lambda: os.system('rm -r "%s"' % TMP_DIR))

def tmpfile_path():
	return TMP_DIR + '/' + ''.join([random.choice(list('0123456789abcdef')) for i in range(16)])

def system_(cmd):
    print(cmd)
    p = subprocess.Popen(shlex.split(cmd), stderr=subprocess.PIPE, shell=False, bufsize=-1)
    p.wait()
    if p.returncode is not 0:
        raise OSError('Command returned {}: `{}`\n\n{}'.format(p.returncode, cmd, p.stderr.read().decode('utf-8')))

class Download:
    @staticmethod
    def yt_url(video_url: str, quality: str = '7', search = False) -> bytes:
        filename = tmpfile_path()

        quality: int = int(quality)
        wide: bool = quality > 7
        quality = quality if not wide else quality - 8

        amr_ext = 'amr-nb' if not wide else 'amr-wb'

        # Download
        if search or re.match('^http(s?):\/\/(www.)?(youtube|youtu.be).[a-z.]{2,}\/', video_url):
        	system_('youtube-dl --extract-audio -o "{}.%(ext)s" "{}{}"'.format(filename, 'ytsearch1:' if search else '', video_url))
        	system_('mv {} {}'.format(TMP_DIR + '/' + next(f for f in os.listdir(TMP_DIR) if f.startswith(filename.split('/')[-1])), filename))       # Gets rid of extension. We can't use wildcards so we have to use this garbage.
        else:
        	system_('wget "{}" -O {}'.format(video_url, filename))

        # Convert
        system_('ffmpeg -i {0} -filter:a "volume=0.9" {0}.wav'.format(filename))
        system_('sox {0}.wav -C {qual} {0}.{amr_ext}'.format(filename, qual=quality, amr_ext=amr_ext))

        # Read AMR into memory
        data = open('{}.{}'.format(filename, amr_ext), 'rb').read()

        # Clean up
        system_('rm {}'.format(' '.join([TMP_DIR + '/' + f for f in os.listdir(TMP_DIR) if f.startswith(filename.split('/')[-1])])))	# AMR won't be deleted as it's in amr/ directory

        return data
