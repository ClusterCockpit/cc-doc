#!/usr/bin/env python3


import os, sys
import re
import glob
import subprocess
import tempfile
import argparse
import shutil
from locale import getpreferredencoding

ENCODING = getpreferredencoding()
VERBOSITY = False

regex_html_comment_open = re.compile("<!--")
regex_html_comment_close = re.compile("-->")
regex_reference = re.compile("\[(.+?)\]\((.+?)\)")
regex_github_url_repo_name = re.compile(".+/(.+)\.git")
hugo_reference_format = '[{}]({{{{< ref "{}" >}}}})'
regex_url_cc_lib = re.compile("https://github.com/ClusterCockpit/cc\-lib/blob/main/(.+)\.md")
replace_url_cc_lib = r'{{{{< ref "docs/reference/cc-lib/{}" >}}}}'
regex_url_cc_collector = re.compile("https://github.com/ClusterCockpit/cc\-metric\-collector/blob/main/(.+)\.md")
replace_url_cc_collector = r'{{{{< ref "docs/reference/cc-metric-collector/{}" >}}}}'
regex_url_cc_collector_main = re.compile("https://github.com/ClusterCockpit/cc\-metric\-collector(.*)")
replace_url_cc_collector_main = r'{{{{< ref "docs/reference/cc-metric-collector/" >}}}}'
to_404 = '[{}]({{{{< ref "404" >}}}})'

url_replacers = {
    regex_url_cc_lib : replace_url_cc_lib,
    regex_url_cc_collector : replace_url_cc_collector,
    regex_url_cc_collector_main : replace_url_cc_collector_main,
}

def get_github_repo(url, folder=".", branch="main"):
    p = None
    if not branch or len(branch) == 0:
        branch = "main"
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        p = subprocess.run("git clone -b {} {}".format(branch, url), shell=True, check=True, cwd=folder)
    except subprocess.CalledProcessError as e:
        print("Clone of {} failed with error {}".format(url, e.returncode))
        return False
    return True

def ignore_copy(folder, entries):
    out = []
    for f in entries:
        if not os.access(os.path.join(folder, f), os.R_OK):
            out.append(f)
    return out

def get_github_repo_local(source, folder=""):
    if os.path.exists(source) and os.path.isdir(source):
        dest = folder
        shutil.copytree(source, dest, symlinks=True, ignore=ignore_copy)
        return True
    return False

def get_cliargs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", help="Increase output verbosity", action="store_true")
    parser.add_argument("-d", "--destination", help="Destination folder")
    parser.add_argument("-l", "--local", help="Local source folder with github repo")
    parser.add_argument("-r", "--remote", help="Remote URL to github repo")
    parser.add_argument("-b", "--branch", help="Use a specific branch instead of 'main'")
    return parser.parse_args(argv)

def get_header(filename):
    head = {}
    hregex = re.compile("^(.+)\s*:\s*[\"']*(.+)[\"']*\s*$")
    with open(filename) as fp:
        lines = fp.read().split("\n")
        parse = False
        for l in lines:
            if l.strip() == "---":
                if not parse:
                    parse = True
                    continue
                else:
                    break
            if parse:
                m = hregex.match(l)
                if m:
                    head[m.group(1)] = m.group(2)
    return head

def get_docu_pages(folder):
    return glob.glob(os.path.join(folder, "*.md"), recursive=True) + glob.glob(os.path.join(folder, "**", "*.md"), recursive=True)

args = get_cliargs(sys.argv[1:])

if not args.destination:
    print("Destination folder required")
    sys.exit(1)

if args.verbosity:
    VERBOSITY = True

if not os.path.exists(args.destination):
    if VERBOSITY:
        print("Creating destination directory {}".format(args.destination))
    os.makedirs(args.destination)


tmp = tempfile.TemporaryDirectory()
if VERBOSITY:
    print("Creating temporary directory {}".format(tmp.name))

repo_name = ""
if args.local:
    repo_name = os.path.basename(args.local)
    if VERBOSITY:
        print("Copying local repository {} to {}".format(args.local, os.path.join(tmp.name, repo_name)))
    ret = get_github_repo_local(args.local, folder=os.path.join(tmp.name, repo_name))
    if not ret:
        sys.exit(1)
elif args.remote:
    m = regex_github_url_repo_name.match(args.remote)
    if m:
        repo_name = m.group(1)
    if VERBOSITY:
        print("Cloning repository {} to {}".format(args.remote, os.path.join(tmp.name, repo_name)))
    ret = get_github_repo(args.remote, folder=tmp.name, branch=args.branch)
    if not ret:
        sys.exit(1)

repo_dir = os.path.join(tmp.name, repo_name)
files = {}
for doc in get_docu_pages(repo_dir):
    header = get_header(doc)
    if len(header) == 0: continue
    header["relpath"] = os.path.relpath(doc, repo_dir)
    files[doc] = header


for doc, header in files.items():
    #print(header)
    outfile = os.path.join(args.destination, header["hugo_path"])

    with open(doc) as infp:
        doclines = infp.read().split("\n")
        if not os.path.exists(os.path.dirname(outfile)):
            os.makedirs(os.path.dirname(outfile))
        with open(outfile, "w") as outfp:
            if VERBOSITY:
                print("Converting {} to {}".format(doc, outfile))
            for l in doclines:
                lm = l
                if regex_html_comment_open.match(l) or regex_html_comment_close.match(l):
                    continue
                m = regex_reference.search(l)
                if m:
                    key, value = m.groups()
                    for regex in url_replacers:
                        rm = regex.search(value)
                        if rm:
                            if len(m.groups()) > 1:
                                print(regex, rm.groups())
                                
                                value = rm.group(1).replace(".md", "").replace("README", "")
                                lm = re.sub(regex_reference, "[{}]({})".format(key, url_replacers[regex].format(value)), lm)
                            else:
                                lm = re.sub(regex_reference, "[{}]({})".format(key, url_replacers[regex]), lm)

                    if value.startswith("./docs"):
                        lm = re.sub(regex_reference, hugo_reference_format.format(key, "404"), lm)
                    elif value.startswith(".") and "md" in value:
                        vparts = value.split("#")
                        f = os.path.realpath(os.path.join(os.path.dirname(doc), vparts[0]))
                        fh = files.get(f, None)
                        print(f, fh)
                        if fh:
                            v = fh["hugo_path"].replace(".md", "").replace("/_index","")
                            if len(vparts) > 1:
                                v += "#"+vparts[1]
                            value = v
                        #print(hugo_reference_format.format(key, value))
                        lm = re.sub(regex_reference, hugo_reference_format.format(key, value), lm)
                    
                outfp.write(lm + "\n")

