
import concurrent.futures
import logging
import multiprocessing
import os
import re
from multiprocessing import Pool
from functools import partial
from contextlib import contextmanager


def regularizeFilename(filename):
    '''
        remove space
    '''
    return filename.replace(' ', '_')


@contextmanager
def poolcontext(*args, **kwargs):
    pool = multiprocessing.Pool(*args, **kwargs)
    yield pool
    pool.close()
    pool.join()


def batchClean(parentdir, func):
    for currentDirectory, directories, filenames in os.walk(parentdir):
        for currentFile in filenames:
            relDir = os.path.relpath(currentDirectory, parentdir)
            relative_path = os.path.join(relDir, currentFile)

            func(os.path.join(currentDirectory, currentFile), relative_path=relative_path)


def batchCleanToOneFile(parentdir, outputFile, func):
    destinedir = os.path.dirname(outputFile)
    if not os.path.exists(destinedir):
        os.makedirs(destinedir)

    with open(outputFile, 'w') as f_out, open(outputFile + '_label', 'w') as f_out_label:
        for currentDirectory, directories, filenames in os.walk(parentdir):
            for currentFile in filenames:
                relDir = os.path.relpath(currentDirectory, parentdir)
                doc_id = os.path.join(relDir, currentFile)

                func(os.path.join(currentDirectory, currentFile), f_out, f_out_label, doc_id=doc_id)


def processEachFileInFolder_parallel(sourceDir, func, destineDir=None, output_file_suffix='', ignoreExisting=False, filename_pattern=None, test=False):
    threadCount = multiprocessing.cpu_count() * 2

    if test:
        threadCount = 1
        # processEachFileInFolder_sequential(sourceDir, func, destineDir, output_file_suffix, ignoreExisting, filename_pattern)
    '''
        clean each file in sourceDir, put it in destineDir with the same name, plus a suffix
        concurrency supported by concurrent.futures.ThreadPoolExecutor

        @param ignoreExisting: optional. ignore the current one if output file exists (good for resuming large operation)
        @param filename_pattern: optional. only process files matching filename_pattern
    '''
    if destineDir is None:
        # default to current directory
        destineDir = os.path.normpath(sourceDir) + '_processed'
    with concurrent.futures.ThreadPoolExecutor(max_workers=threadCount) as executor:
    # with poolcontext(processes=threadCount) as pool:
        for currentDirectory, directories, filenames in os.walk(sourceDir):
            for currentFile in filenames:
                try:
                    relDir = os.path.relpath(currentDirectory, sourceDir)
                    directory = os.path.join(destineDir, relDir)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    destinationFile = os.path.join(directory, regularizeFilename(currentFile) + output_file_suffix)
                    if filename_pattern and not filename_pattern.match(currentFile):
                        continue
                    if os.path.isfile(destinationFile) and ignoreExisting:
                        continue

                    executor.submit(func, os.path.join(currentDirectory, currentFile), destinationFile)
                    print "started processing: " + currentFile
                except Exception:
                    import ipdb;ipdb.set_trace()


def processEachFileInFolder_sequential(sourceDir, func, destineDir=None, output_file_suffix='', ignoreExisting=False, filename_pattern=None):
    if destineDir is None:
        destineDir = os.path.normpath(sourceDir) + '_processed'
    for currentDirectory, directories, filenames in os.walk(sourceDir):
        for currentFile in filenames:
                relDir = os.path.relpath(currentDirectory, sourceDir)
                directory = os.path.join(destineDir, relDir)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                destinationFile = os.path.join(directory, regularizeFilename(currentFile) + output_file_suffix)
                if filename_pattern and not filename_pattern.match(currentFile):
                    continue
                if os.path.isfile(destinationFile) and ignoreExisting:
                    continue
                else:
                    func(os.path.join(currentDirectory, currentFile), destinationFile)
                    print "started processing: "+currentFile


pdfTXTFileExtensions = re.compile('((\.txt)|(\.pdf))+$')


def listAllFiles(sourceDir):
    filenameWithRelDirList = []
    for currentDirectory, directories, filenames in os.walk(sourceDir):
        for currentFile in filenames:
            relDir = os.path.relpath(currentDirectory, sourceDir)
            filenameWithRelDir = os.path.join(relDir, currentFile)
            filenameWithRelDirList.append(filenameWithRelDir)

    filenameWithRelDirList = map(lambda x: pdfTXTFileExtensions.sub('', x), filenameWithRelDirList)
    return filenameWithRelDirList

if __name__ == '__main__':
    print 1
