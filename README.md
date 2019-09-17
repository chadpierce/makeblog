# make-blog
 A set of hacky scripts that build a static html blog website

## what is this?

One time I had the bright idea that'd I'd start a blog, then wrote this and never really made one. Maybe I still will one day, but it probably won't use this now that I've played with Flask a little bit! In reality this was just a fun little project to kill some time. 

The idea is that you write blog posts in markdown files, then use the makeblog.py script to generate all of the html files necessary for the site in a staging folder, then push that to the prod website with another script. 

I need to upload some templates for the html pages. 

## File descriptions:

- bu_home_dir.sh - creates tarball of entire home directory for off-server backups
- bu.sh - creates tarball of live /var/www/html directory
- check_sshd_logs.sh - run as sudo to check server logs
- makeblog.py - creates html files based on markdown posts and html templates (this users a jinja type method - from before I knew what that was)
- sync_live_to_staging.sh - rsyncs live blog to stating directory
- sync_staging_to_live.sh - rsyncs staging directory to live blog (publishes)
- update_pages.py - the drawback for static pages is that sometimes you need to update something on all of them. this script does that