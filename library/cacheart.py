import logging
import requests
from cachepath import CachePath, TempPath, Path
from shutil import copyfile, copyfileobj

class CacheArt():
    '''download and cache album artwork from lms server
    
    Args:
        app_name(`str`): name of application - used to create /tmp/`app_name` directory
        
    Properties:
        app_name(`str`): name of application
        cache_path(:obj:`CachePath`): path to store cached artwork
        '''
    def __init__(self, app_name):
        self.app_name = app_name
        
    @property
    def app_name(self):
        '''name of application
            this is used to set the path in /tmp/`app_name`
            
        Sets:
            app_name(`str`): name of application
            cache_path(obj:`CachePath`): path to store cached artwork'''
        return self._app_name
    
    @app_name.setter
    def app_name(self, app_name):
        self._app_name = app_name
        self.cache_path = CachePath(app_name, dir=True)
    
    def cache_artwork(self, artwork_url=None, album_id=None):
        '''download and cache artwork as needed from lms server
        
        Args:
            artwork_url(`str`): URL of artwork on LMS server
            album_id(`str`): unique string that identifies artwork on LMS server
            
        Returns:
            (obj:`pathlib.Path`): path to album artwork'''
        if not artwork_url or not album_id:
            raise TypeError(f'missing required value: artwork_url: {artwork_url}, album_id: {album_id}')
                
        album_id = str(album_id)
        
        artwork_path = self.cache_path/(album_id+'.jpg')
        
        if artwork_path.exists():
            logging.debug(f'artwork previously cached')
            return artwork_path
        
        r = False
        try:
            r = requests.get(artwork_url, stream=True)
        except requests.exceptions.RequestException as e:
            logging.error(f'failed to fetch artwork at: {artwork_url}: {e}')
        
        if r:
            try:
                with open(artwork_path, 'wb') as outFile:
                    copyfileobj(r.raw, outFile)
                    logging.debug(f'wrote ablum artwork to: {artwork_path}')
            except (OSError, FileExistsError, ValueError) as e:
                logging.error(f'failed to write {artwork_path}')
        else:
            logging.error('failed to download album art due to previous errors')
            return None
        
        return artwork_path

    def clear_cache(self, force=False):
        '''clear the contents of the cache folder or wipe entirely
        
        Args:
            force(`bool`): False (default) - delete the files, True - delete entire directory and contents
            '''
        logging.debug(f'clearing previously downloaded files in {self.cache_path}')
        if force:
            logging.info(f'removing cache directory: {self.cache_path}')
            try:
                self.cache_path.rm()
            except Exception as e:
                logging.error(f'Error removing cach directory: {e}')
                return False
        else:
            try:
                self.cache_path.clear()
            except Exception as e:
                logging.error(f'Error removing files in cache d directory: {e}')
                return False
            
        return True
