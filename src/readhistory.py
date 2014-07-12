import sqlite3

placesPath = '../places.sqlite'

def main():
	conn = sqlite3.connect(placesPath)
	
	c = conn.cursor()
	
	c.execute('select sqlite_version()')
	
	c.execute("""select * from moz_historyvisits""")
	
	history = c.fetchall()
	print history
	
	conn.close()
	
if __name__ == '__main__':
	main()
