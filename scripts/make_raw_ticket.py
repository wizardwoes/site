from csv import DictReader
from pathlib import Path

import frontmatter


def from_csv(fpath):
    rows = []
    with open(fpath, "r") as csvfile:
        reader = DictReader(csvfile)
        rows = [row for row in reader]
    return rows


def to_post(d):
    cont = d.pop('content', "")
    return frontmatter.Post(cont, **d)


def to_file(p, opath):
    with open(opath, "w") as f:
        f.write(frontmatter.dumps(p))


if __name__ == "__main__":
    fpath = Path("scripts/ticket_tracker - Sheet1.csv")
    odir = Path("scripts/raw_tickets")
    tickets = from_csv(fpath)
    for t in tickets:
        if t["t_num"]:
            p = to_post(t)
            outname = "phaedrus-" + t["t_num"] + ".txt"
            to_file(p, (odir / outname))
