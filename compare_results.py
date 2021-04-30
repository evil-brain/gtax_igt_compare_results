#!/usr/bin/env python3
"""
Creates a CSV file comparing multiple runs of IGT in GTAX - using the downloaded results files.
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

    # Read results into igt_results and normalize test results.
    # End result is a dict: igt_results[dir1,dir2,...][test1,test2,...]=[result1,result2...]
    for result_dir in args.inputs:
        igt_results[result_dir] = {}
        #print(result_dir)
        for subdir in os.listdir(result_dir):
            #print("subdir: ", subdir)
            with open(os.path.join(result_dir, subdir, 'results', 'task_custom.json')) as taskfile:
                results = json.load(taskfile)
                for object in results:
                    if "ci_bug_log@igt@" in object:
                        #print(object)
                        #print(results[object]['tests'])
                        for test in results[object]['tests']:
                            # print(test)
                            # print(results[object]['tests'][test]['err'])
                            if "SUCCESS" in results[object]['tests'][test]['err']:
                                igt_results[result_dir][test] = "SUCCESS"
                            elif "SKIP" in results[object]['tests'][test]['err']:
                                igt_results[result_dir][test] = "SKIP"
                            elif "FAIL" in results[object]['tests'][test]['err']:
                                igt_results[result_dir][test] = "FAIL"
                            else:
                                igt_results[result_dir][test] = results[object]['tests'][test]['err']
            #break

    # Start printing the CSV, starting with headers
    print("test_name,", end='')
    for directory in igt_results:
        print(directory, end='')
        print(",", end='')
    print("")

    # Dict structure:
    # igt_results[directory_name][test_name]:test_result

    # Print results for test, search all other runs for the same test name and print result. Then remove from dict.
    # Anything left in the dict had no results for the first passed-in directory, print those results.
    for test in list(igt_results[args.inputs[0]].keys()):
        print(test, end='')
        print(",",end='')

        print(igt_results[args.inputs[0]][test], end='')
        print(",",end='')
        del igt_results[args.inputs[0]][test]

        for other_result in list(igt_results.keys()):
            if args.inputs[0] == other_result:
                continue

            for other_test in list(igt_results[other_result].keys()):
                if test == other_test:
                    print(igt_results[other_result][other_test], end='')
                    print(",", end='')
                    del igt_results[other_result][other_test]
                    break
            print(",", end='')
        print("")

    result_depth=0
    for directory in igt_results:
        result_depth+=1
        for test in igt_results[directory]:
            print(test, end='')
            for i in range(0, result_depth):
                print(",", end='')
            print(igt_results[directory][test])

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
