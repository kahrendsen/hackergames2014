import sqlite3
import os
import platform

placesPath = '../places.sqlite'

def get_profile_folder():
  windowsPath = r'%APPDATA%\Mozilla\Firefox\Profiles'
  linuxPath = '~/.mozilla/firefox'
  macPath = '~/Library/Application Support/Firefox/Profiles'
  
  myOS = platform.system()
  profiles = None
  
  if myOS == 'Windows':
    profiles = windowsPath
  elif myOS == 'Darwin':
    profiles = macPath
  else:  # linux hopefully
    profiles = linuxPath
    
  profiles = os.path.expanduser(profiles)  # expand ~ to home dir
  profileFolder = [a for a in os.listdir(profiles) if a.endswith('.default')][0]
  
  return os.path.join(profiles, profileFolder)

def get_places_path():
  return os.path.join(get_profile_folder(), 'places.sqlite')

def main():
  conn = sqlite3.connect(get_places_path())
  
  c = conn.cursor()
  
  c.execute('select sqlite_version()')
  
  c.execute("""select id, from_visit, place_id, visit_date, visit_type, session from moz_historyvisits""")
  history = c.fetchall()
  
  c.execute("""select id, url, title, rev_host, visit_count, hidden, typed, favicon_id, frecency from moz_places""")
  places = c.fetchall()
    
  print history
  print places
  
  conn.close()
  
if __name__ == '__main__':
  main()
