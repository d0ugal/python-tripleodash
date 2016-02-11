import pbr.version

_version_info = pbr.version.VersionInfo('python-tripleodash')
RELEASE_STRING = _version_info.semantic_version().release_string()
__version__ = _version_info.version_string()
