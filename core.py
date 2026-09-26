from dataclasses import dataclass, field

GRADES = {
    "Junior Open (Y9–10)": (5, 2.5),
    "Senior Open (Y11–12)": (6, 3),
    "Advanced Open (Y12–13)": (6, 3),
    "Premier Junior (up to Y11)": (6, 3),
    "Premier Advanced (up to Y13)": (8, 4),
}
MOOTS = [
    "This House would make public transport free for secondary school students.",
    "This House believes schools should start later in the morning.",
    "This House would ban single-use plastic packaging in school canteens.",
]

@dataclass(frozen=True)
class Turn:
    side: str
    role: str
    minutes: float

@dataclass
class Debate:
    moot: str
    grade: str
    student_side: str
    replies: bool = False
    turns: list[Turn] = field(init=False)
    speeches: list[str] = field(default_factory=list)

    def __post_init__(self):
        main, reply = GRADES[self.grade]
        self.turns = [Turn(side, f"{n} speaker", main)
                      for n in (1, 2, 3) for side in ("Affirmative", "Negative")]
        if self.replies:
            self.turns += [Turn("Negative", "Reply (first or second speaker)", reply),
                           Turn("Affirmative", "Reply (first or second speaker)", reply)]

    @property
    def current(self):
        return self.turns[len(self.speeches)] if len(self.speeches) < len(self.turns) else None

    def add(self, speech):
        if not self.current or not speech.strip():
            raise ValueError("An active turn needs a non-empty speech")
        self.speeches.append(speech.strip())

    def transcript(self):
        return "\n\n".join(f"{i+1}. {turn.side} {turn.role}: {speech}"
                           for i, (turn, speech) in enumerate(zip(self.turns, self.speeches)))
