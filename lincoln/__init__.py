'''
Top-level package for lincoln dam and watershed game.
'''

__app_name__ = 'lincoln games'
__version__  = '0.1.0'

# Return and Error Codes (integer codes assigned using range)
(
    SUCCESS, 
    DIR_ERROR, 
    FILE_ERROR,
    TOML_ERROR, 
    SYSTEM_ERROR,
    # DB_READ_ERROR, 
    # DB_WRITE_ERROR, 
    # JSON_ERROR,
    NOT_IMPLEMENTED_ERROR
) = range(6) # [0,7]

# Error desciptions
ERRORS = {
    DIR_ERROR: 'configuration directory error',
    FILE_ERROR: 'configuration file error',
    TOML_ERROR: 'TOML decode error',
    SYSTEM_ERROR: 'system object configuration error',
    # DB_READ_ERROR: 'database read error',
    # DB_WRITE_ERROR: 'database write error',
    NOT_IMPLEMENTED_ERROR: 'not implemented error'
}