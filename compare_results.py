#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Brian J Lovin"
__version__ = "0.1.0"
__license__ = "MIT"

import os
import argparse
import json

def main():
    """ Main entry point of the app """
    igt_results = {}

    parser = argparse.ArgumentParser(prog='gtax-results-compare')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    parser.add_argument('inputs', metavar='INPUTS', type=str, nargs="+",
                        help='directory containing results from gtax')

    args = parser.parse_args()
    #print(args.inputs)

    for subdir in os.listdir(args.inputs[0]):
        #print("subdir: ", subdir)
        with open(os.path.join(args.inputs[0], subdir, 'results', 'task_custom.json')) as taskfile:
            results = json.load(taskfile)
            for object in results:
                if "ci_bug_log@igt@" in object:
                    #print(object)
                    #print(results[object]['tests'])
                    for test in results[object]['tests']:
                        # print(test)
                        # print(results[object]['tests'][test]['err'])
                        if "SUCCESS" in results[object]['tests'][test]['err']:
                            igt_results[test] = "SUCCESS"
                        elif "SKIP" in results[object]['tests'][test]['err']:
                            igt_results[test] = "SKIP"
                        else:
                            igt_results[test] = results[object]['tests'][test]['err']

    for i in igt_results:
        print("igt_results[",i,"] = ", igt_results[i])

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
