from . import confit

config = confit.LazyConfig('flinck', __name__)
config.add({
    'file_extensions': ['avi', 'm4v', 'mkv', 'mp4'],
    'file_min_size_mb': 20,
})
