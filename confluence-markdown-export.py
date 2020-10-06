import os
import argparse

import html2text
from atlassian import Confluence


class ExportException(Exception):
    pass


class Exporter:
    def __init__(self, url, username, token, out_dir):
        self.__out_dir = out_dir
        self.__confluence = Confluence(url=url, username=username, password=token)
        self.__seen = set()

    def __dump_page(self, src_id, parents):
        if src_id in self.__seen:
            # this could theoretically happen if Page IDs are not unique or there is a circle
            raise ExportException("Duplicate Page ID Found!")

        page = self.__confluence.get_page_by_id(src_id, expand="body.storage")
        page_title = page["title"]
        page_id = page["id"]
    
        # see if there are any children
        child_ids = self.__confluence.get_child_id_list(page_id)
    
        content = page["body"]["storage"]["value"]

        # save all files as .html for now, we will convert them later
        extension = ".html"
        if len(child_ids) > 0:
            document_name = "index" + extension
        else:
            document_name = page_title + extension

        # make some rudimentary checks, to prevent trivial errors
        for invalid in ["..", "/"]:
            if invalid in document_name:
                print("Dangerous page title: \"{}\", \"{}\" found, replacing it with \"_\"".format(document_name,
                                                                                                   invalid))
                document_name = document_name.replace(invalid, "_")

        page_location = parents + [document_name]
        filename = os.path.join(self.__out_dir, *page_location)

        dirname = os.path.dirname(filename)
        os.makedirs(dirname, exist_ok=True)
        print("Saving to {}".format(" / ".join(page_location)))
        with open(filename, "w") as f:
            f.write(content)

        self.__seen.add(page_id)
    
        # recurse to process child nodes
        for child_id in child_ids:
            self.__dump_page(child_id, parents=parents + [page_title])
    
    def dump(self):
        for space in self.__confluence.get_all_spaces(start=0, limit=500, expand='description.plain,homepage'):
            space_key = space["key"]
            print("Processing space", space_key)
            if space.get("homepage") is None:
                print("Skipping space: {}, no homepage found!".format(space_key))
                print("In order for this tool to work there has to be a root page!")
                raise ExportException("No homepage found")
            else:
                # homepage found, recurse from there
                homepage_id = space["homepage"]["id"]
                self.__dump_page(homepage_id, parents=[space_key])


class Converter:
    def __init__(self, out_dir):
        self.__out_dir = out_dir

    def recurse_findfiles(self, path):
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                yield from self.recurse_findfiles(entry.path)
            elif entry.is_file(follow_symlinks=False):
                yield entry
            else:
                raise NotImplemented()
    
    def convert(self):
        for entry in self.recurse_findfiles(self.__out_dir):
            path = entry.path
            
            if not path.endswith(".html"):
                continue

            print("Converting {}".format(path))
            with open(path) as f:
                data = f.read()

            md = html2text.html2text(data)
            newname = os.path.splitext(path)[0]
            with open(newname + ".md", "w") as f:
                f.write(md)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, help="The url to the confluence instance")
    parser.add_argument("username", type=str, help="The username")
    parser.add_argument("token", type=str, help="The access token to Confluence")
    parser.add_argument("out_dir", type=str, help="The directory to output the files to")
    parser.add_argument("--no-fetch", dest="no_fetch", type=bool, required=False, default=False,
                        help="This option only runs the markdown conversion")
    args = parser.parse_args()
    
    if not args.no_fetch:
        dumper = Exporter(url=args.url, username=args.username, token=args.token, out_dir=args.out_dir)
        dumper.dump()
    
    converter = Converter(out_dir=args.out_dir)
    converter.convert()
