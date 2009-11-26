#!/usr/bin/python
import os
import popen2, string
import re


def enumeratefiles(path):
    """Returns all the files in a directory as a list"""
    file_collection = []
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            file_collection.append(path+file)
    return file_collection

def collect_libs(dict, file):
    fin, fout = popen2.popen2("ldd "+file)
    fout.close()
    for line in fin.readlines():
        m=re.search("(\S*/lib/\S+)", line)
        if m:
            dict[m.group(1)]=""
    fin.close()


if __name__ == "__main__":
    libs={}
    for lib in ("/lib/libgcc_s.so.1","/lib/libnss_files.so.2","/lib/libnss_compat.so.2"):
        libs[lib]=""
    collect_libs(libs,"/lib/libnss_compat.so.2")
    for path in ("source/bin/", "source/sbin/"):
        for file in enumeratefiles(path):
            collect_libs(libs, file)
    for lib in libs.keys():
        print lib
        if not os.path.exists("source"+os.path.dirname(lib)):
            os.makedirs("source"+os.path.dirname(lib))
        os.system("cp -u -v -L "+lib+ " source"+lib)
