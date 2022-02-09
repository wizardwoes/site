from cgi import test
from pathlib import Path
from typing import OrderedDict
import sys

import frontmatter


def merge_citations(fdir):
    p = Path(fdir)
    fnames = [f for f in p.glob("*.md") if f.name not in ["index.md"]]

    fm = [frontmatter.load(f) for f in fnames]

    all_cite = [f.get("cite", None) for f in fm]
    return all_cite


def has_other_content(fdir):
    p = Path(fdir)
    fnames = [f for f in p.glob("*.md") if f.name not in ["index.md"]]
    return True if any(fnames) else False


def get_index(fdir):
    p = Path(fdir)
    index = p / "index.md"
    return index if index.exists() else None


def remove_null_citations(cites):
    cites = [cite for cite in cites if cite]
    return cites


def add_citations_to_index(index, cites):
    fm = frontmatter.load(index)
    fm["cite"] = cites
    return fm


if __name__ == "__main__":
    try:
        fdir = sys.argv[1]
    except IndexError:
        print("no directory given")
        exit(1)

    index = get_index(fdir)

    if not index:
        print("index.md not found in {0}".format(fdir))
        exit(1)

    if not has_other_content(fdir):
        print("No other content files found in {0}. Update not needed.".format(fdir))
        exit(1)

    cites = merge_citations(fdir)
    cites = remove_null_citations(cites)

    if not any(cites):
        print(
            "No citations found in other files at {0}. Update not needed.".format(fdir)
        )
        exit(1)

    fm = add_citations_to_index(index, cites)

    frontmatter.dump(fm, index)
    print("Citations in {0} index.md updated".format(fdir))
    exit(0)
