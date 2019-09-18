#!/usr/bin/env python3
'''
'  makeblog
'  Author: cpx741
'  Version 0.2.2
'  Date Updated: 2019-06-07
'  https://github.com/cpx741/makeblog.git

'  Sitebuilder converts markdown text to html for WEBSITENAME.net
'  Requirements: python3 with markdown module
'''
# TODO - back up edited files
# TODO - error checking
# TODO - check all files before publishing any (use tmp staging dir)
# TODO - make any occurances of WEBSITENAME.net a variable to make the script portable
# TODO - log files
# TODO make file output a function
# TODO make filename generation a function (this is commented in code somewhere)
# NEXT LEVEL STUFF
# TODO - build pw protected page on website for creating posts, etc
# 		 this could be a ver2.0 kind of thing!

import sys
import markdown
import datetime
from re import sub as sub_
from os import makedirs as makedirs_
from os.path import isdir as isdir_

# NOTE - UPDATE THESE FOR EACH DEPLOYMENT
DRAFT_DIR = "./"
TEST_DIR = "test/"
PROD_DIR = "staging/"
# TODO add url vars here

def display_help():
	# TODO make some help!
	print("Help goes here!")
	sys.exit(0)

def parse_header(header):
	if not header:
		print("Bad header (or no header) in input file.")
		sys.exit(0)
	# check header formatting
	if not (header[0] == "---\n" and header[5] == "---\n"):
		print("ERROR: invalid header")
	elif not (header[1].startswith("layout [")):
		print("ERROR: invalid layout line in header")
	elif not (header[2].startswith("title [")):
		print("ERROR: invalid title line in header")
	elif not (header[3].startswith("date [")):
		print("ERROR: invalid date line in header")
	elif not (header[4].startswith("tags [")):
		print("ERROR: invalid tag line in header")

	# get header vars
	# pulls everything between [ and ], tags are put into a list
	post_layout = header[1][header[1].find('[')+1 : header[1].find(']')]
	post_title = header[2][header[2].find('[')+1 : header[2].find(']')]
	post_date = header[3][header[3].find('[')+1 : header[3].find(']')]
	post_tags = header[4][header[4].find('[')+1 : header[4].find(']')].split(",")

	# print header vars for verification
	print("[+] Header format is valid")
	print("[+]     type is: ",post_layout)
	print("[+]     post name is: ",post_title)
	print("[+]     post date is: ",post_date)
	print("[+]     tags are: ",post_tags)
	# named tuple with header data
	header = (post_layout,post_title,post_date,post_tags)
	return header

def md2html(body):
	body =  ''.join(body)
	html = markdown.markdown(body)
	# this is unneccessary ~ change <code> to <pre><code> for highlight.js
	# html = html.replace("<code>","<pre><code>")
	# html = html.replace("</code>","</pre>,</code>")
	print("[+] Markdown converted to html")
	return html

def get_template(layout):
	if layout == "post":
		with open('templates/post-template.html', 'r') as template_f:
			template = template_f.read()
		print("[+] Post template imported")
		return template
	elif layout == "postlist":
		# this template is just the current posts.html file
		with open(SITE_DIR + 'posts.html', 'r') as template_f:
			template = template_f.read()
		print("[+] Postlist template imported")
		return template
	elif layout == "tags":
		with open('templates/tags-template.html', 'r') as template_f:
			template = template_f.read()
		print("[+] Tags list template imported")
		return template
	elif layout == "index":
		# this template is just the current index
		with open(SITE_DIR + 'index.html', 'r') as template_f:
			template = template_f.read()
		print("[+] Index template imported")
		return template
	else:
		print("[-] ERROR: invalid post layout type in header")

def make_post_html(header, body):
	tags = ""
	template = get_template(header[0])
	template = template.replace("{{{TITLE}}}",header[1])
	formatted_date = datetime.datetime.strptime(header[2], "%Y-%m-%d").strftime("%d %B %Y")
	template = template.replace("{{{DATE}}}",formatted_date)
	# puts all tags into one line of links
	for tag in header[3]:
		tags += " <a href=\"/tags/" + tag + ".html\">" + tag +"</a>" + "  "
	template = template.replace("{{{TAGS}}}",tags)
	template = template.replace("{{{POST}}}",body)
	lowercase_title = header[1].lower()
	lowercase_title = lowercase_title.replace(" ","-")
	# remove all non alpha numeric (and dash) characters
	#TODO FIXME this is done several times...make a func
	lowercase_title = sub_('[^A-Za-z0-9-]+', '', lowercase_title)
	title_nospaces = header[1].replace(" ","%20") # for twitter link
	# TODO this should be made more generic with vars defined in the script
	post_url = "https://WEBSITENAME.net/blog/" + header[2].replace("-","/") + "/" + lowercase_title + ".html"
	twitter_link = "http://twitter.com/share?text=\"" + title_nospaces + "\"&url=" + post_url
	fb_link = "https://www.facebook.com/sharer/sharer.php?u=" + post_url
	template = template.replace("{{{TWITTER}}}",twitter_link)
	template = template.replace("{{{FACEBOOK}}}",fb_link)

	# post filename format: 2018-06-22_test-post.html
	# FIXME is this hacky? yes? fix!!!!
	if DEV_STAGE == 'DRAFT':
		html_filename = lowercase_title + "_DRAFT.html"
		with open(html_filename, 'w') as post_f:
			post_f.write(template)
			print("[+] DRAFT Blog Post HTML file was generated")
			print("[+]     filename: " + html_filename)
	else:
		html_filename = lowercase_title + ".html"
		html_path = "blog/" + datetime.datetime.strptime(header[2], "%Y-%m-%d").strftime("%Y/%m/%d/")
		if not isdir_(SITE_DIR + html_path):
			makedirs_(SITE_DIR + html_path)
		# TODO make file output a function
		with open(SITE_DIR + html_path + html_filename, 'w') as post_f:
			post_f.write(template)
		print("[+] Blog Post HTML file was generated")
		print("[+]     filename: " + html_path + html_filename)
		# TODO write_log(header)

def make_postlist_link(header):
		# makes link for posts.html and index.html
		# TODO make a title creation func
		lowercase_title = header[1].lower()
		lowercase_title = lowercase_title.replace(" ","-")
		# remove all non alpha numeric (and dash) characters
		lowercase_title = sub_('[^A-Za-z0-9-]+', '', lowercase_title)
		formatted_date = datetime.datetime.strptime(header[2], "%Y-%m-%d").strftime("%d %B %Y")

		tag_links = "    <td>"
		for tag in header[3]:
			tag_links = tag_links +  "<a href=/tags/" + tag + ".html>" + tag + "</a> "
		tag_links = tag_links + "</td>"

		# TODO remove | WEBSITENAME.net from main posts file
		new_post = "<!--{{{POST}}}-->\n" \
		"<tr>\n" \
		"    <td><a title=\"" + header[1] + "\" href=/blog/" + header[2].replace("-","/") + "/" + lowercase_title + ".html>" + header[1] + "</a></td>\n" \
		+ tag_links + "\n" \
		"    <td text-align=\"right\">" + formatted_date + "</td>\n" \
		"</tr>\n"

		return new_post

def make_postlist_html(header):
	template = get_template("postlist")
	new_post = make_postlist_link(header)

	template = template.replace("<!--{{{POST}}}-->",new_post)
	with open(SITE_DIR + "posts.html", 'w') as post_f:
		post_f.write(template)
	print("[+] Post list HTML file was generated")
	# TODO add postlist to write_log()

def make_taglist_link(header):
	lowercase_title = header[1].lower()
	lowercase_title = lowercase_title.replace(" ","-")
	# remove all non alpha numeric (and dash) characters
	lowercase_title = sub_('[^A-Za-z0-9-]+', '', lowercase_title)
	formatted_date = datetime.datetime.strptime(header[2], "%Y-%m-%d").strftime("%d %B %Y")

	taglist_link = "<!--{{{POST}}}-->\n" \
	"<tr>\n" \
	"    <td><a title=\"" + header[1] + "\" href=/blog/" + header[2].replace("-","/") + "/" + lowercase_title + ".html>" + header[1] + "</a></td>\n" \
	"    <td text-align=\"right\">" + formatted_date + "</td>\n" \
	"</tr>\n"

	return taglist_link

def update_tags(header):
	# get existing tags from tags.txt, get user input for desc of any new tags
	# create new tags.html and individual tagname.html files, and new tags.txt
	etags = get_existing_tags()
	# FIXME hacky thing here, make better way to track existing tags for individual tag files
	oldtags = etags
	# FIXME this is a dumb way to cycle through the existing tags
	a_etags, b_etags = zip(*etags)
	ntags = []
	ptags = header[3]
	for tag in ptags:
		if tag not in a_etags:
			new_tag = [[tag,input("    ENTER description for new tag - " + tag + ": ")]]
			etags = etags + new_tag
			ntags = ntags + new_tag
	etags.sort()

	if ntags:
		make_taglist_txt(etags)
		print("[+] Updated tags.txt")
		make_taglist_html(etags)
		print("[+] Updated tags.html")
	else:
		print("[+] No new tags (tags.txt and tags.html left unchanged)")

	make_ind_tag_html(oldtags[0], header)

def get_existing_tags():
	# TODO check file format ~ tag,description of tag ~ one per line
	with open('tags.txt', 'r') as etags_f:
  		etags = [line.rstrip('\n').split(',') for line in etags_f]
	return etags

def make_taglist_txt(etags):
	with open('tags.txt', 'w') as tags_f:
		for tag in etags:
			tags_f.write(tag[0] + ',' + tag[1] + '\n')

def make_taglist_html(etags):
	template = get_template("tags")
	tags = ""
	for i in range(len(etags)):
		tags = tags + \
		"<tr>\n" \
		"<td><a title=" + etags[i][0] + " href=\"/tags/" + etags[i][0] + ".html\">" + etags[i][0] + "</a></td>\n" \
		"<td>" + etags[i][1] + "</td>\n" \
		"</tr>\n"
	template = template.replace("{{{TAGS}}}",tags)
	with open(SITE_DIR + "tags.html", 'w') as post_f:
		post_f.write(template)

def make_ind_tag_html(oldtags, header):
	taglist_link = make_taglist_link(header)
	print("[+] Updating individual tag files:")
	for tag in header[3]:
		if tag not in oldtags:
			# process new tags
			with open('templates/individual-tag-template.html', 'r') as template_f:
				template = template_f.read()
			template = template.replace("{{{TAGNAME}}}",tag)
			template = template.replace("<!--{{{POST}}}-->",taglist_link)
			with open(SITE_DIR + 'tags/' + tag + '.html', 'w') as post_f:
				post_f.write(template)
				print("[+]     Created " + tag + " HTML file")
		else:
			# process existing tags
			with open(SITE_DIR + 'tags/' + tag + '.html', 'r') as template_f:
				template = template_f.read()
			template = template.replace("<!--{{{POST}}}-->",taglist_link)
			with open(SITE_DIR + 'tags/' + tag + '.html', 'w') as post_f:
				post_f.write(template)
				print("[+]     Updated " + tag + " HTML file")

def update_index_html(header):
	template = get_template("index")
	new_post = make_postlist_link(header)
	template = template.replace("<!--{{{POST}}}-->",new_post)
	with open(SITE_DIR + 'index.html', 'w') as post_f:
		post_f.write(template)
	print("[+] Updated index.html")

def confirm_prod_update():
	yes = {'yes', 'YES'}
	no = {'no', 'NO'}
	while 1==1:
		confirm = input("Please confirm by entering 'yes' (or no to exit): ")
		if confirm in yes:
			print("Confirmed. Sitebuilder will proceed.")
			break
		elif confirm in no:
			print("Goodbye.")
			sys.exit(0)
		else:
			print("Please enter 'yes' or 'no'.")

def write_log(header):
	# TODO actually use this
	if header[0] == "post":
		tags = ','.join(header[3])
		log_entry = "Post generated: name=" + header[1] + "; date=" + header[2] + "; post_tags=" + tags
		# print(log_entry)
		with open("dev/posts.log", 'a') as log_f:
			log_f.write(log_entry)

# Script starts here

# catches -h if its first (or only) arg
if (sys.argv[1] == "help" or sys.argv[1] == "-h"):
	display_help()
	sys.exit(0)

# check for 3 args (script name - mode - input file)
if not(len(sys.argv) == 3):
	print("wrong num of arguements")
	# TODO add proper systax message here and in next section
	# NOTE should this be exit(1)?
	sys.exit(0)

# check for second arg - mode
if (sys.argv[1] == "draft" or sys.argv[1] == "-d"):
	print("You selected draft.")
	DEV_STAGE = 'DRAFT'
elif (sys.argv[1] == "test" or sys.argv[1] == "-t"):
	print("You selected test.")
	DEV_STAGE = 'TEST'
elif (sys.argv[1] == "prod" or sys.argv[1] == "-p"):
	print("You selected prod...")
	DEV_STAGE = 'PROD'
elif (sys.argv[1] == "help" or sys.argv[1] == "-h"):
	print("help detected")
	display_help()
	sys.exit(0)
else:
	print("incorrect syntax")
	sys.exit(0)

# check input filename
if not(sys.argv[2].endswith('.md')):
	print("You must supply a valid markdown file!")
	sys.exit(0)

if(DEV_STAGE == 'DRAFT'):
	SITE_DIR = DRAFT_DIR
elif(DEV_STAGE == 'TEST'):
	SITE_DIR = TEST_DIR
elif(DEV_STAGE == 'PROD'):
	SITE_DIR = PROD_DIR
	confirm_prod_update()
else:
	print("Something has gone wrong.")
	sys.exit(0)

# TODO FIXME change this to use with open
# arguments are mode switch and filename
md_f = open(str(sys.argv[2]), "r")
md_contents = md_f.readlines()
md_f.close()
md_header = md_contents[0:6]
md_body = md_contents[6:]

post_header = parse_header(md_header)
post_body = md2html(md_body)

if DEV_STAGE == 'DRAFT':
	make_post_html(post_header, post_body)
	sys.exit(0)

if post_header[0] == 'post':
	make_post_html(post_header, post_body)
	make_postlist_html(post_header)
	update_tags(post_header)
	update_index_html(post_header)
