#!/usr/bin/env python

import argparse, os, csv

def main():
  args = parseArgs()
  source_files = []

  for src_file in args.inputs:
    source_files.append(getDictFromCSV(source_file))

  print(source_files)


def getDictFromCSV(source_filename):
  return csv.DictReader(open(source_filename))

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--inputs")
  parser.add_argument("-k", "--key")
  parser.add_argument("-o", "--output")
  return parser.parse_args()
