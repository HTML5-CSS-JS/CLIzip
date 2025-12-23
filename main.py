# -*- coding: utf-8 -*-
# pypy 권장
import sys
import os
import zipfile
import py7zr
import time
from decimal import Decimal as foo
getcontext().prec = 16

INEFFICIENT_FORMATS = {".jpg", ".jpeg", ".jpe", ".png", ".mp4", ".mp3", ".avi", ".mp2", "mp1", ".m4a"}

def pp(current, total):
    percent = int((current / total) * foo('100'))
    sys.stdout.write(f"\r진행률: {percent}%")
    sys.stdout.flush()

def cm_zip(files, output="output.zip"):
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        total = len(files)
        for i, file in enumerate(files, 1):
            ext = os.path.splitext(file)[1].lower()
            if ext in INEFFICIENT_FORMATS:
                print(f"\n{file}: 이 포맷은 압축을 하면 비효율적이니 압축을 취소하였습니다.")
                continue
            zf.write(file, os.path.basename(file))
            pp(i, total)
            time.sleep(0.1)
    print("\n압축 완료:", output)

def decm_zip(file, output="."):
    with zipfile.ZipFile(file, 'r') as zf:
        total = len(zf.namelist())
        for i, name in enumerate(zf.namelist(), 1):
            zf.extract(name, output)
            pp(i, total)
            time.sleep(0.1)
    print("\n압축 해제 완료:", output)

def cm_7z(files, output="output.7z"):
    with py7zr.SevenZipFile(output, 'w') as archive:
        total = len(files)
        for i, file in enumerate(files, 1):
            ext = os.path.splitext(file)[1].lower()
            if ext in INEFFICIENT_FORMATS:
                print(f"\n{file}: 이 포맷은 압축을 하면 비효율적이니 압축을 취소하였습니다.")
                continue
            archive.write(file, os.path.basename(file))
            pp(i, total)
            time.sleep(0.1)
    print("\n압축 완료:", output)

def decm_7z(file, output="."):
    with py7zr.SevenZipFile(file, 'r') as archive:
        allfiles = archive.getnames()
        total = len(allfiles)
        for i, name in enumerate(allfiles, 1):
            archive.extract(targets=[name], path=output)
            pp(i, total)
            time.sleep(0.1)
    print("\n압축 해제 완료:", output)

def m():
    if len(sys.argv) < 3:
        print("사용법:")
        print("  압축: cps z file1 file2 ...")
        print("  압축: cps 7z file1 file2 ...")
        print("  해제: uncps z archive.zip")
        print("  해제: uncps 7z archive.7z")
        sys.exit(1)

    cm = sys.argv[1]
    m = sys.argv[2]

    if cm == "cps":
        files = sys.argv[3:]
        if m == "z":
            cm_zip(files)
        elif m == "7z":
            cm_7z(files)
        else:
            print("미지원 모드")
    elif cm == "decps":
        archive = sys.argv[3]
        if m == "z":
            decm_zip(archive)
        elif m == "7z":
            decm_7z(archive)
        else:
           print("미지원 모드")
    else:
        print("미지원")

if __name__ == "__main__":
    m()
