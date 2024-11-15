# Author   : Martin Užák <uzak+git@mailbox.org>
# Creation : 2021-04-28 09:39

"""
pytest autocompletion for ZSH. Extracts class/function/file names
that represent tests from all python files recursively found under `.`
"""

import re
import os


class_pat = re.compile(r'^\s*class\s+(Test\w+).*')
fn_pat = re.compile(r'^\s*def\s+(test_\w+).*')
file_pat = re.compile(r'^.*?/?test_\w+\.py$')


def parse_file(filename, result):
    if file_pat.match(filename):
        # remove common part of the name
        abs_pwd = os.path.abspath(".")
        filename = os.path.abspath(filename)
        common = os.path.commonpath([abs_pwd, filename])
        filename = filename[len(abs_pwd)+1:]
    else:
        return

    result.append(filename)
    with open(filename) as f:
        current_cls = None
        for line in f.readlines():
            cls_match = class_pat.match(line)
            if cls_match:
                cls_name = cls_match.group(1)
                cls_name = "%s::%s" % (filename, cls_name)
                current_cls = cls_name
                result.append(cls_name)
                continue

            fn_match = fn_pat.match(line)
            if fn_match:
                test_name = fn_match.group(1)
                if current_cls:
                    test_name = "%s::%s" % (current_cls, test_name)
                else:
                    test_name = "%s::%s" % (filename, test_name)
                result.append(test_name)
                continue

def parse_files(*files):
    result = []
    for filename in files:
        parse_file(filename, result)
    result.sort()
    return result


if __name__ == '__main__':
    import pathlib

    test_files = []
    for pat in ('test_*.py', '*_test.py'):
        for path in pathlib.Path(".").rglob('test_*.py'):
            test_files.append(str(path))

    for test in parse_files(*test_files):
        print(test)
