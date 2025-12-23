# -*- coding: utf-8 -*-
# pypy 권장
import sys
import os
import zipfile
import py7zr
import time
from decimal import Decimal as foo, getcontext
getcontext().prec = 16

INEFFICIENT_FORMATS = {".jpg", ".jpeg", ".jpe", ".png", ".mp4", ".mp3", ".avi", ".mp2", ".mp1", ".m4a"}

def pp(current, total):
    try:
        percent = int((current / total) * foo('100'))
        sys.stdout.write(f"\r{percent}%")
        sys.stdout.flush()
    except Exception as e:
        print("\n진행률 계산 오류:", e)

def cm_zip(files, output="output.zip"):
    try:
        with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            total = len(files)
            for i, file in enumerate(files, 1):
                ext = os.path.splitext(file)[1].lower()
                if ext in INEFFICIENT_FORMATS:
                    print(f"\n{file}: 압축하면 비효율적이니 압축 취소")
                    continue
                if not os.path.exists(file):
                    print(f"\n{file}: 파일이 존재하지 않아 건너뜀")
                    continue
                try:
                    zf.write(file, os.path.basename(file))
                except PermissionError:
                    print(f"\n{file}: 권한 오류로 건너뜀")
                    continue
                pp(i, total)
                time.sleep(0.1)
        print("\n압축 완:", output)
    except Exception as e:
        print("ZIP 압축 중 오류 발생:", e)

def decm_zip(file, output="."):
    try:
        with zipfile.ZipFile(file, 'r') as zf:
            total = len(zf.namelist())
            for i, name in enumerate(zf.namelist(), 1):
                try:
                    zf.extract(name, output)
                except PermissionError:
                    print(f"\n{name}: 권한 오류로 건너뜀")
                    continue
                pp(i, total)
                time.sleep(0.1)
        print("\n압축 해제 완:", output)
    except FileNotFoundError:
        print("ZIP 파일을 찾을 수 없습니다:", file)
    except zipfile.BadZipFile:
        print("잘못된 ZIP 파일입니다:", file)
    except Exception as e:
        print("ZIP 해제 중 오류 발생:", e)

def cm_7z(files, output="output.7z"):
    try:
        with py7zr.SevenZipFile(output, 'w') as archive:
            total = len(files)
            for i, file in enumerate(files, 1):
                ext = os.path.splitext(file)[1].lower()
                if ext in INEFFICIENT_FORMATS:
                    print(f"\n{file}: 압축하면 비효율적이니 압축 취소")
                    continue
                if not os.path.exists(file):
                    print(f"\n{file}: 파일이 존재하지 않아 건너뜀")
                    continue
                try:
                    archive.write(file, os.path.basename(file))
                except PermissionError:
                    print(f"\n{file}: 권한 오류로 건너뜀")
                    continue
                pp(i, total)
                time.sleep(0.1)
        print("\n압축 완:", output)
    except Exception as e:
        print("7Z 압축 중 오류 발생:", e)

def decm_7z(file, output="."):
    try:
        with py7zr.SevenZipFile(file, 'r') as archive:
            allfiles = archive.getnames()
            total = len(allfiles)
            for i, name in enumerate(allfiles, 1):
                try:
                    archive.extract(targets=[name], path=output)
                except PermissionError:
                    print(f"\n{name}: 권한 오류로 건너뜀")
                    continue
                pp(i, total)
                time.sleep(0.1)
        print("\n압축 해제 완:", output)
    except FileNotFoundError:
        print("7Z 파일을 찾을 수 없습니다:", file)
    except py7zr.ArchiveError:
        print("잘못된 7Z 파일입니다:", file)
    except Exception as e:
        print("7Z 해제 중 오류 발생:", e)

def m():
    if len(sys.argv) < 3:
        print("사용법:")
        print("압축: cps z file1 file2 ...")
        print("압축: cps 7z file1 file2 ...")
        print("해제: uncps z archive.zip")
        print("해제: uncps 7z archive.7z")
        sys.exit(1)

    cm = sys.argv[1]
    m = sys.argv[2]

    try:
        if cm == "cps":
            files = sys.argv[3:]
            if m == "z":
                cm_zip(files)
            elif m == "7z":
                cm_7z(files)
            else:
                print("미지원 모드")
        elif cm == "uncps":
            archive = sys.argv[3]
            if m == "z":
                decm_zip(archive)
            elif m == "7z":
                decm_7z(archive)
            else:
                print("미지원 모드")
        else:
            print("미지원")
    except IndexError:
        print("인자가 부족합니다.")
    except Exception as e:
        print("명령 실행 중 오류 발생:", e)

if __name__ == "__main__":
    m()