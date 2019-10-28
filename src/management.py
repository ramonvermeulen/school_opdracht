import cgi
import cgitb

cgitb.enable()

data = cgi.FieldStorage()

name = data.getvalue('name')

print('Content-Type:text/html\r\n\r\n')
print('<html>')
print('<head><title>Test program</title></head>')
print('<body>')
print(f'<h2>Hello {name}!</h2>')
print('</body>')
print('</html>')
