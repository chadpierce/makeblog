'''
' update_pages.py
'
' A WEBSITENAME.net built from makeblog.py is all static html pages. 
' this script takes input from 2 text files
' and changes matching strings recursively across the entire site.
'
' ex: orig: <tag>thsi has soem misteaks</tag>
'     changes: <tag>this has some mistakes</tag>
'
' -the input will need to obviously be unique
' -changes will be made recursively to entire
'  directory structure where the
'  script is run
'
' this is quick and dirty maybe i should make it better or more pythonistic or something /shrug
'
'''

import os
import sys
# import codecs
# reload(sys)
# sys.setdefaultencoding("utf-8")

# !! THIS PATH MUST BE SET !!
rootDir = './test'

def get_html_file(fname,dname):
    with open(dname + '/' + fname, 'r') as f:
        file_contents = f.read()
    #print("[+] - got " + fname)
    return file_contents

def get_original():
    with open('original.txt', 'r') as f:
        original = f.read()
        original = original.rstrip()
    print("[+] got original.txt")
    return original

def get_changes():
    with open('changes.txt', 'r') as f:
        changes = f.read()
        changes = changes.rstrip()
    print("[+] got changes.txt")
    #print(repr(changes))
    #print(changes)
    return changes

def make_new_html(fname, dname, fhtml):
    with open(dname + '/' + fname, 'w') as f:
        f.write(fhtml)

def confirm_change():
	yes = {'yes', 'YES'}
	no = {'no', 'NO'}
	while 1==1:
		confirm = input("Please confirm by entering 'yes' (or no to exit): ")
		if confirm in yes:
			print("[+] Confirmed. Script will proceed...")
			break
		elif confirm in no:
			print("Goodbye.")
			sys.exit(0)
		else:
			print("Please enter 'yes' or 'no'.")

if not (os.path.isfile('original.txt') and os.path.isfile('changes.txt')):
    print("ERROR: original.txt and changes.txt must exist!")
    sys.exit()

original = get_original()
changes = get_changes()

print('----------------------------------------------------------------------')
print('[-] comfirm settings:')
print(' - original strings:')
print('   ' + original)
print(' - new strings:')
print('   ' + changes)
print(' - root directory is: ' + rootDir)
print('----------------------------------------------------------------------')
confirm_change()

for dirName, subdirList, fileList in os.walk(rootDir):
    print('[+] found directory: %s' % dirName)
    for fname in fileList:
        if fname.endswith(".html"):
            fhtml = get_html_file(fname, dirName)
            # this is where the actual work is done vv
            if original in fhtml:
                fhtml = fhtml.replace(original,changes)
                make_new_html(fname, dirName, fhtml)
                print('[*] - updated file: %s' % fname)
            else:
                print('[-] - no changes made: %s' % fname)
        else:
            print("[-] - not html: " + fname)
