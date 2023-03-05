import re
import shutil
import sys
from pathlib import Path

# function of translate


def normalize(name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    new_name = name.stem
    new_name = new_name.translate(TRANS)
    f_name = re.sub(r"[\s+\W]", "_", new_name)
    new_name = f_name + name.suffix  # new name of file

    return new_name

# function of move file


def move(el_suf, name, path):
    suffix = el_suf.suffix
    if suffix in [".jpg", ".png", ".jpeg", ".svg"]:
        images = path/"images"
        if not images.exists():
            images.mkdir()    # create folder images
        el_suf = el_suf.rename(el_suf.parent / name)
        file_in_target = el_suf.replace(images/el_suf.name)
    elif suffix in [".avi", ".mp4", ".mov", ".mkv"]:
        videos = path/"video"
        if not videos.exists():
            videos.mkdir()    # create folder video
        el_suf = el_suf.rename(el_suf.parent / name)
        file_in_target = el_suf.replace(videos/el_suf.name)
    elif suffix in [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx", ".xls"]:
        document = path / "documents"
        if not document.exists():
            document.mkdir()  # create folder documents
        el_suf = el_suf.rename(el_suf.parent / name)
        file_in_target = el_suf.replace(document/el_suf.name)
    elif suffix in [".mp3", ".ogg", ".wav", ".amr"]:
        audios = path/"audio"
        if not audios.exists():
            audios.mkdir()    # create folder audio
        el_suf = el_suf.rename(el_suf.parent/name)
        file_in_target = el_suf.replace(audios/el_suf.name)
    elif suffix in [".zip", ".gz", ".tar"]:
        archives = path/"archives"
        if not archives.exists():
            archives.mkdir()    # create folder archives
        file_in_target = el_suf.replace(archives/el_suf.name)
        new_folder = archives/el_suf.stem
        if not new_folder.exists():
            new_folder.mkdir()  # create folder with name archives
        shutil.unpack_archive(file_in_target, new_folder)
        for item in new_folder.glob("**/*"):
            new_file = normalize(item)  # translate name of file in archives
            file_in_target = item.rename(new_folder/new_file)
    else:
        file_in_target = el_suf.replace(path / el_suf.name)
    return file_in_target


def main(path):
    path = Path(path)
    for i in path.iterdir():
        if i.is_file():
            new_name = normalize(i)
            new_way = move(i, new_name, path)
        # ignore special folder
        elif i.is_dir() and i.name in ["audio", "video", "images", "documents", "archives"]:
            continue
        else:
            main(path / i)
            i.rmdir()
    return new_way


if __name__ == "__main__":
    main("C:\\Users\\m.fursa\\Documents\\Python\\Chlam")
