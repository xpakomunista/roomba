import glob
ports=glob.glob('/dev/tty[A-Za-z]*')
for port in ports:
        print(port)
