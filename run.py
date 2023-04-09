#!/usr/bin/python

import os
import time
import subprocess
import sys

def split_results(results):
    biggest_gap = results[1]['elapsed'] - results[0]['elapsed']
    split_point = -1
    for i in range(len(results) - 1):
        gap = results[i]['elapsed'] - results[i - 1]['elapsed']
        if gap > biggest_gap:
            split_point = i
            biggest_gap = gap

    
    return (results[:split_point], results[split_point:])

def print_results(results):
    for result in results:
        print("  - " + result['dir'] + ' (' + str(round(result['elapsed'] * 1000)) + 'ms)')

REPEAT = 1

command_generator = {
    'gcc': lambda dir: ['gcc', 'main.cpp', '-E', '-Iguards/' + dir, '-DINCLUDE_GUARD_ALREADY_DEFINED', '-DONCE="once"'],
    'clang': lambda dir: ['clang', 'main.cpp', '-E', '-Iguards/' + dir, '-DINCLUDE_GUARD_ALREADY_DEFINED', '-DONCE="once"'],
    'msvc': lambda dir: ['cl', 'main.cpp', '/E', '/Iguards/' + dir, '/DINCLUDE_GUARD_ALREADY_DEFINED', '/DONCE="once"', '>nul' '2>&1'],
}

if len(sys.argv) != 2:
    print("Usage: run.py gcc|clang|msvc")
    sys.exit(1)

if sys.argv[1] not in command_generator:
    print("Usage: run.py gcc|clang|msvc")
    sys.exit(1)

compiler = command_generator[sys.argv[1]]

directories = next(os.walk('./guards'))[1];
max_length = max(directories, key = len)
results = []
for directory in next(os.walk('./guards'))[1]:
    start = time.time()
    for _ in range(REPEAT):
        subprocess.run(compiler(directory), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elapsed = (time.time() - start)
    results.append({ 'dir': directory, 'elapsed': elapsed });

results.sort(key = lambda r: r['elapsed'])
guarded, unguarded = split_results(results)

print("Guarded (" + str(len(guarded)) + ")")
print_results(guarded)

print("Unguarded (" + str(len(unguarded)) + ")")
print_results(unguarded)
