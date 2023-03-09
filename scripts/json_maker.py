from dataclasses import dataclass, asdict, field
from enum import StrEnum, auto
import json
from pathlib import Path

import frontmatter


class TicketType(StrEnum):
    EPIC = auto()
    STORY = auto()
    TASK = auto()
    ISSUE = auto()
    BUG = auto()


class Priority(StrEnum):
    BLOCKER = auto()
    CRITICAL = auto()
    MAJOR = auto()
    MINOR = auto()


class Project(StrEnum):
    PHAE = auto()


class Resolution(StrEnum):
    UNRESOLVED = auto()


@dataclass
class Avatar:
    uri: str = ""


@dataclass
class User:
    uid: int
    name: str
    shortname: str
    avatar: Avatar = field(default_factory=Avatar)


@dataclass
class Comment:
    user: User
    created_on: str = None
    content: str = None


@dataclass
class People:
    assignee: User
    reporter: User


@dataclass
class Ticket:
    title: str
    project: Project
    t_num: int
    resolution: str
    tickettype: TicketType
    priority: Priority
    assignee: User
    reporter: User
    status: str = "cool"
    labels: list[str] = field(default_factory=list)
    comments: list[Comment] = field(default_factory=list)
    related: list["Ticket"] = field(default_factory=list)
    content: str = None
    t_url: str = field(init=False)
    people: dict = field(init=False)

    def __post_init__(self):
        self.t_url = "PHAEDRUS-" + str(self.t_num)
        self.people = {"assignee": self.assignee, "reporter": self.reporter}


def dump_tickets(fpath, tickets):
    t = [asdict(ticket) for ticket in tickets]

    with open(fpath, "w") as f:
        f.write(json.dumps(t))


def handle_username(name):
    soc = User(1, "Socrates", "sock")
    phae = User(2, "Phaedrus", "fey")

    if name in ("Socrates.", "Soc.", "socrates", "Soc"):
        return soc

    if name in ("Phaedrus.", "Phaedr.", "phaedrus", "Phaedr"):
        return phae

    return None


def handle_resolution(res):
    match res:
        case "unresolved":
            return Resolution.UNRESOLVED


def handle_ticket_type(ttype):
    match ttype:
        case "epic":
            return TicketType.EPIC
        case "story":
            return TicketType.STORY
        case "task":
            return TicketType.TASK
        case "issue":
            return TicketType.ISSUE
        case "bug":
            return TicketType.BUG


def handle_priority(priority):
    match priority:
        case "blocker":
            return Priority.BLOCKER
        case "critical":
            return Priority.CRITICAL
        case "major":
            return Priority.MAJOR
        case "minor":
            return Priority.MINOR


def ticket_test():
    soc = User(1, "Socrates", "sock")
    phae = User(2, "Phaedrus", "fey")

    tick_com = [
        Comment(
            phae,
            content="""I thought that you were only halfway and were going to make
a similar speech about all the advantages of accepting the non-lover.
Why do you not proceed? """,
        ),
        Comment(
            soc,
            content="""Does not your simplicity observe that I have got out of 
dithyrambics
into heroics, when only uttering a censure on the lover? And if I
am to add the praises of the non-lover, what will become of me? Do
you not perceive that I am already overtaken by the Nymphs to whom
you have mischievously exposed me? And therefore will only add that
the non-lover has all the advantages in which the lover is accused
of being deficient. And now I will say no more; there has been enough
of both of them. Leaving the tale to its fate, I will cross the river
and make the best of my way home, lest a worse thing be inflicted
upon me by you. 
            """,
        ),
    ]

    return Ticket(
        "Socrates having finished, proposes to return home",
        Project.PHAE,
        1,
        Resolution.UNRESOLVED,
        TicketType.ISSUE,
        Priority.BLOCKER,
        phae,
        soc,
        comments=tick_com,
        content="I propose to return home.",
    )


def comments_from_lines(lines, initial_date=None):
    # takes a list of strings

    user = None
    comments = []

    for line in lines:
        match line.split():
            case [("Socrates." | "Soc." | "Phaedrus." | "Phaedr.") as name, *spl]:
                user = handle_username(name)
                content = " ".join(spl)
                new_comment = Comment(user, content=content)
                comments.append(new_comment)
            case [*spl]:
                content = " ".join(spl)
                comments[-1].content = comments[-1].content + " " + content
            case _:
                tcontent = []
                user = None

    return comments


def make_ticket_from_frontmatter(md):
    with open(md, "r") as f:
        post = frontmatter.load(f)

    lines = post.content.split("\n")
    try:
        comments = comments_from_lines(lines)
    except IndexError:
        comments = []

    return Ticket(
        post.get("title", default="needs a title"),
        Project.PHAE,
        post["t_num"],
        handle_resolution(post["resolution"]),
        handle_ticket_type(post["tickettype"]),
        handle_priority(post["priority"]),
        handle_username(post["assignee"]),
        handle_username(post["reporter"]),
        comments=comments,
        content=post["tbody"],
    )


def from_dir(fpath):
    return [make_ticket_from_frontmatter(f) for f in fpath.iterdir()]


if __name__ == "__main__":
    # fpath = Path("scripts\\raw_tickets\\test.txt")
    fdir = Path("scripts\\raw_tickets")

    # tick = ticket_test()
    # post = make_ticket_from_frontmatter(fpath)

    tickets = from_dir(fdir)
    outpath = Path("prebuild\\assets\\jira\\ticket_details.json")
    dump_tickets(outpath, tickets)
