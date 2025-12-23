# -*- coding: utf-8 -*-
import sys
import os
import zipfile
import py7zr
import time

INEFFICIENT_FORMATS = {".jpg", ".jpeg", ".jpe", ".png", ".mp4", ".mp3", ".avi", ".mp2", ".mp1", ".m4a"}
MAX_FILE_SIZE = 400 * 1024 * 1024  # 400MB 제한 (압축 해제 시)

def safe_path(base, target):
    """경로 탈출 방지"""
    abs_base = os.path.abspath(base)
    abs_target = os.path.abspath(os.path.join(base, target))
    if not abs_target.startswith(abs_base):
        raise Exception(f"경로 탈출 시도 감지: {target}")
    return abs_target

def safe_extract_zip(zf, output):
    for name in zf.namelist():
        target_path = safe_path(output, name)
        info = zf.getinfo(name)
        if info.file_size > MAX_FILE_SIZE:
            print(f"{name}: 파일 크기 초과로 해제 취소")
            continue
        zf.extract(name, output)

def safe_extract_7z(archive, output):
    for name in archive.getnames():
        target_path = safe_path(output, name)
        # py7zr은 파일 크기 정보를 직접 제공하지 않으므로 별도 검사 필요
        archive.extract(targets=[name], path=output)

def cm_zip(files, output="output.zip"):
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in INEFFICIENT_FORMATS:
                print(f"{file}: 비효율적 포맷이라 제외")
                continue
            if not os.path.exists(file):
                print(f"{file}: 없음")
                continue
            if os.path.getsize(file) > MAX_FILE_SIZE:
                print(f"{file}: 크기 초과로 제외")
                continue
            zf.write(file, os.path.basename(file))
    print("ZIP 압축 완료:", output)

def decm_zip(file, output="."):
    try:
        with zipfile.ZipFile(file, 'r') as zf:
            safe_extract_zip(zf, output)
        print("ZIP 해제 완료:", output)
    except Exception as e:
        print("ZIP 해제 오류:", e)

def cm_7z(files, output="output.7z"):
    with py7zr.SevenZipFile(output, 'w') as archive:
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in INEFFICIENT_FORMATS:
                print(f"{file}: 비효율적 포맷이라 제외")
                continue
            if not os.path.exists(file):
                print(f"{file}: 없음")
                continue
            if os.path.getsize(file) > MAX_FILE_SIZE:
                print(f"{file}: 크기 초과로 제외")
                continue
            archive.write(file, os.path.basename(file))
    print("7Z 압축 완료:", output)

def decm_7z(file, output="."):
    try:
        with py7zr.SevenZipFile(file, 'r') as archive:
            safe_extract_7z(archive, output)
        print("7Z 해제 완료:", output)
    except Exception as e:
        print("7Z 해제 오류:", e)

def m():
    if len(sys.argv) < 3:
        print("사용법: cps z file1 file2 ... | cps 7z file1 file2 ... | decps z archive.zip | decps 7z archive.7z")
        sys.exit(1)

    cm = sys.argv[1]
    m = sys.argv[2]

    if cm == "cps":
        files = sys.argv[3:]
        if not files:
            print("압축할 파일 없음")
            return
        if m == "z":
            cm_zip(files)
        elif m == "7z":
            cm_7z(files)
        else:
            print("미지원 모드")
    elif cm == "decps":
        if len(sys.argv) < 4:
            print("해제할 파일 없음")
            return
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
