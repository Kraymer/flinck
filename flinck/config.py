from . import confit

FIELDS = ('country', 'director', 'decade', 'genre', 'rating', 'runtime',
    'title', 'year')

config = confit.LazyConfig('flinck', __name__)
config.add({
    'file_extensions': ['avi', 'm4v', 'mkv', 'mp4'],
    'file_min_size_mb': 20,
    'google_api_key': '',
    'link_root_dir': '',
    'verbose': False,
})
