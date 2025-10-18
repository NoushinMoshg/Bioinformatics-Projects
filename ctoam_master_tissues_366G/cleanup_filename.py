'''replace spaces in .xls filenames, with underscore:
    any files in subdirectory 20220320'''
import os
import sys
sep = os.path.sep

lines = [x.strip() for x in os.popen('find ./ -name "*.xls"').readlines()]
for x in lines:
    w = x.split(sep)

    f = w[-1]
    fn = f.replace(' ', '_')

    if f != fn:
        f = sep.join(w[:-1] + [f])
        fn = sep.join(w[:-1] + [fn])
        print(f, '-->', fn)
        os.rename(f, fn)
