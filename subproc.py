import subprocess

cmd="dir *.py"
result = subprocess.run(["perl", "..\WebInject-Framework\wif.pl", "--help"], stdout=subprocess.PIPE)
print (result.args)
print (result.stdout.decode())
