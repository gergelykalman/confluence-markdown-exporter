### A very simple Confluence to Markdown exporter.

This code is not written with security in mind, do NOT run it on a repository that can contain mailicious
page titles.


### Usage
1. Install requirements: <code>pip3 install -r requirements.txt</code>
2. Run the script: <code>python3.9 confluence-markdown-export.py url username token out_dir</code>
   providing URL e.g. https://YOUR_PROJECT.atlassian.net, login details - username and API Token,
   and output directory, e.g. ./output_dir

The secret token can be generated under Profile -> Security -> Manage API Tokens
