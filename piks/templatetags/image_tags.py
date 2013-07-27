# my_apps/image/templatetags/image_tags.py
import os.path

from django import template
from django.conf import settings

FMT = 'JPEG'
EXT = 'jpg'
QUAL = 75

THUMBNAIL_SIZE = '260x180'
IMAGE_SIZE = '1280x960'

register = template.Library()


def resized_path(path, method):
	if method == 'crop':
		size = THUMBNAIL_SIZE
	elif method == 'scale':
		size = IMAGE_SIZE
		
	dir, name = os.path.split(path)
	image_name, ext = name.rsplit('.', 1)

	return os.path.join(dir, '%s_%s_%s.%s' % (image_name, method, size, EXT)).replace('\\', '/')


def scale(imagefield, method='scale'):
    """ 
    Template filter used to scale an image
    that will fit inside the defined area.

    Returns the url of the resized image.

    {% load image_tags %}
    {{ profile.picture|scale }}
    """

    if not imagefield:
		return None

    # imagefield can be a dict with "path" and "url" keys
    if imagefield.__class__.__name__ == 'dict':
        imagefield = type('imageobj', (object,), imagefield)

    image_path = resized_path(imagefield.path, method)

    #thumb_path = os.path.join(settings.MEDIA_ROOT, "%s_%s_%s.%s" % (imagefield.name.rsplit('.', 1)[0], method, EXT))
    #thumb_url = "%s_%s_%s.%s" % (imagefield.url.rsplit('.', 1)[0], method, EXT)

    #print thumb_path, thumb_url

    if not os.path.exists(image_path):
        try:
            import Image
        except ImportError:
            try:
                from PIL import Image
            except ImportError:
                raise ImportError('Cannot import the Python Image Library.')

        image = Image.open(imagefield.path)

        # normalize image mode
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # use PIL methods to edit images
        if method == 'scale':
            width, height = [int(i) for i in IMAGE_SIZE.split('x')]
            image.thumbnail((width, height), Image.ANTIALIAS)
            image.save(image_path, FMT, quality=QUAL)

        elif method == 'crop':
            try:
                import ImageOps
            except ImportError:
                from PIL import ImageOps

            width, height = [int(i) for i in THUMBNAIL_SIZE.split('x')]
            ImageOps.fit(image, (width, height), Image.ANTIALIAS
                        ).save(image_path, FMT, quality=QUAL)
       
    return resized_path(imagefield.url, method)

def crop(imagefield):
    """
    Template filter used to crop an image
    to make it fill the defined area.

    {% load image_tags %}
    {{ profile.picture|crop }}

    """
    return scale(imagefield, 'crop')


register.filter('scale', scale)
register.filter('crop', crop)
