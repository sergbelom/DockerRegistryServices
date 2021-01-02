#!/usr/bin/env python3

import getopt
import sys
import os
import time
import re
import subprocess

from optparse import OptionParser

# option and config handling
parser = OptionParser()
parser.add_option("-n", "--dry-run",
                  help="Run in non-change mode",
                  action="store_true", default=(True if os.environ.get('DRYRUN') else False))
parser.add_option("--root", dest="storage_root",
                  help="Set the storage root directory",
                  default=os.environ.get('REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY', '/var/lib/registry'))
parser.add_option("--no-registry", dest="run_registry",
                  help="Do not run the registry while cleaning up",
                  action="store_false", default=not (os.environ.get('RUN_REGISTRY', 'true') != 'true'))
(options, args) = parser.parse_args()

# environment for sub-processes
os.environ["REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY"] = options.storage_root
os.environ["REGISTRY_DATA_DIR"] = data_dir = options.storage_root + '/docker/registry/v2'

# read-only registry in background
if options.run_registry:
  print( "Running registry in in background (default read-only config)...")
  subprocess.Popen(["/bin/registry", "serve", "/etc/docker/registry/config.yml"]) #, stderr=subprocess.STDOUT)
  # python will kill it when exiting

# collect registry data and numbers
def build_index():
  global repositories, blobs, blobsize, tags, layers
  repositories = []
  blobs = 0
  blobsize = 0
  tags = 0
  layers = 0

  for dirname, dirnames, filenames in os.walk(data_dir + '/blobs'):
    if 'data' in filenames:
      blobs += 1
      data_stat = os.stat(dirname + '/data')
      blobsize += data_stat.st_size

  data_dir_len = len(data_dir)
  repositories_path = data_dir + '/repositories'
  repositories_path_len = len(repositories_path) + 1
  if not os.path.isdir(repositories_path):
    raise Exception("Could not open dir: " + repositories_path)

  for dirname, dirnames, filenames in os.walk(repositories_path):
    if dirname[-15:] == '_manifests/tags':
      tags += len(dirnames)
    if '_manifests' in dirnames:
      repositories.append(dirname[repositories_path_len:])
    if 'link' in filenames and re.search('/_manifests/revisions/', dirname):
      layers += 1
      