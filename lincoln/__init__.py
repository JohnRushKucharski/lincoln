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
    DB_READ_ERROR, 
    DB_WRITE_ERROR, 
    JSON_ERROR
) = range(6) # [0,5]

# Error desciptions
ERRORS = {
    DIR_ERROR: 'configuration directory error',
    FILE_ERROR: 'configuration file error',
    DB_READ_ERROR: 'database read error',
    DB_WRITE_ERROR: 'database write error',
}