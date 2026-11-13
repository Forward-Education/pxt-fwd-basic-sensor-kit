"""Build the micro:bit sensor tutorial worksheets and answer key as PDFs."""
import sys
from pathlib import Path

from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing, Line, PolyLine, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (Flowable, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

FONTS = "/System/Library/Fonts/Supplemental/"
pdfmetrics.registerFont(TTFont("Body", FONTS + "Arial.ttf"))
pdfmetrics.registerFont(TTFont("Body-Bold", FONTS + "Arial Bold.ttf"))
addMapping("Body", 0, 0, "Body")
addMapping("Body", 1, 0, "Body-Bold")

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

BASE = "https://makecode.microbit.org/#tutorial:github:Forward-Education/pxt-fwd-basic-sensor-kit/tutorials/"
INK = colors.HexColor("#1F2328")
QUIET = colors.HexColor("#59636E")
RULE = colors.HexColor("#C9CDD2")
TINT = colors.HexColor("#F1F2F4")
ACCENT = colors.HexColor("#2F6FB3")
POWER = colors.HexColor("#C8372D")
GROUND = colors.HexColor("#4A4F55")
SIGNAL = colors.HexColor("#2F6FB3")

H1 = ParagraphStyle("h1", fontName="Body-Bold", fontSize=22, leading=26, textColor=INK)
KICKER = ParagraphStyle("kicker", fontName="Body", fontSize=9.5, leading=12, textColor=QUIET)
SUB = ParagraphStyle("sub", fontName="Body", fontSize=11, leading=14, textColor=QUIET)
H2 = ParagraphStyle("h2", fontName="Body-Bold", fontSize=12.5, leading=16, textColor=ACCENT,
                    spaceBefore=10, spaceAfter=4)
BODY = ParagraphStyle("body", fontName="Body", fontSize=10.5, leading=14, textColor=INK)
SMALL = ParagraphStyle("small", fontName="Body", fontSize=9, leading=11.5, textColor=QUIET)
CELL = ParagraphStyle("cell", fontName="Body", fontSize=10, leading=12.5, textColor=INK)
CELL_HEAD = ParagraphStyle("cellhead", parent=CELL, fontName="Body-Bold")

PADS = {"0": 110, "1": 245, "2": 380, "3V": 515, "GND": 650}
KIND = {"power": POWER, "ground": GROUND, "signal": SIGNAL}


class WriteLines(Flowable):
    """Ruled lines for handwritten answers."""

    def __init__(self, n, gap=20):
        super().__init__()
        self.n, self.gap = n, gap

    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.n * self.gap + 4

    def draw(self):
        self.canv.setStrokeColor(RULE)
        self.canv.setLineWidth(0.6)
        for i in range(self.n):
            y = (self.n - i - 1) * self.gap + 2
            self.canv.line(14, y, self.width, y)


class CheckLine(Flowable):
    """A checklist line: an empty square to tick, then the text."""

    def __init__(self, text, style=BODY):
        super().__init__()
        self.para = Paragraph(text, style)

    def wrap(self, aw, ah):
        self.width = aw
        _, h = self.para.wrap(aw - 20, ah)
        self.height = max(h, 12) + 4
        return aw, self.height

    def draw(self):
        self.canv.setStrokeColor(QUIET)
        self.canv.setLineWidth(0.8)
        self.canv.rect(1, self.height - 13, 10, 10, stroke=1, fill=0)
        self.para.drawOn(self.canv, 20, self.height - self.para.height - 2)


def box(text, style=BODY):
    return CheckLine(text, style)


def wiring(module, note, pins, wires):
    """Wiring diagram: module pins on top, micro:bit pads below.

    pins:  [(label, x)]  in a 760-wide layout
    wires: [(pin_x, pad_name, elbow_y, kind)]
    """
    W, top, bottom = 760, 70, 316
    s = 500 / W
    d = Drawing(W * s, (bottom - top) * s)

    def Y(y):
        return (bottom - y) * s

    def X(x):
        return x * s

    # key
    kx = 24
    for label, kind in (("3V power", "power"), ("GND ground", "ground"), ("signal to a pin", "signal")):
        if not any(w[3] == kind for w in wires):
            continue
        d.add(Line(X(kx), Y(84), X(kx + 24), Y(84), strokeColor=KIND[kind], strokeWidth=2.2))
        d.add(String(X(kx + 30), Y(88), label, fontName="Body", fontSize=8.5, fillColor=QUIET))
        kx += 150

    # module
    d.add(Rect(X(220), Y(190), X(320), 96 * s, rx=6 * s, ry=6 * s, fillColor=None,
               strokeColor=GROUND, strokeWidth=0.9))
    d.add(String(X(380), Y(118), module, fontName="Body-Bold", fontSize=10.5,
                 fillColor=INK, textAnchor="middle"))
    if note:
        d.add(String(X(380), Y(134), note, fontName="Body", fontSize=8, fillColor=QUIET,
                     textAnchor="middle"))
    for label, x in pins:
        d.add(Rect(X(x - 7), Y(190), 14 * s, 14 * s, fillColor=RULE, strokeColor=None))
        d.add(String(X(x), Y(168), label, fontName="Body-Bold", fontSize=9.5, fillColor=INK,
                     textAnchor="middle"))

    # wires
    used = set()
    for pin_x, pad, ye, kind in wires:
        px = PADS[pad]
        used.add(pad)
        d.add(PolyLine([X(pin_x), Y(190), X(pin_x), Y(ye), X(px), Y(ye), X(px), Y(248)],
                       strokeColor=KIND[kind], strokeWidth=2.2, strokeLineJoin=1))

    # micro:bit edge
    d.add(Rect(X(24), Y(304), X(712), 64 * s, rx=6 * s, ry=6 * s, fillColor=None,
               strokeColor=GROUND, strokeWidth=0.9))
    for name, x in PADS.items():
        on = name in used
        d.add(Rect(X(x - 44), Y(292), 88 * s, 44 * s, rx=6 * s, ry=6 * s, fillColor=TINT,
                   strokeColor=GROUND if on else RULE, strokeWidth=0.9))
        d.add(String(X(x), Y(275), name, fontName="Body-Bold" if on else "Body",
                     fontSize=10, fillColor=INK if on else QUIET, textAnchor="middle"))
    return d


def qr(url, size=34 * mm):
    w = QrCodeWidget(url, barLevel="M")
    x1, y1, x2, y2 = w.getBounds()
    d = Drawing(size, size, transform=[size / (x2 - x1), 0, 0, size / (y2 - y1), 0, 0])
    d.add(w)
    return d


def grid(header, rows, widths, row_h=22):
    data = [[Paragraph(h, CELL_HEAD) for h in header]]
    data += [[Paragraph(c, CELL) for c in r] for r in rows]
    t = Table(data, colWidths=widths, rowHeights=[None] + [row_h] * len(rows))
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.6, RULE),
        ("BACKGROUND", (0, 0), (-1, 0), TINT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def footer(canv, doc):
    canv.saveState()
    canv.setFont("Body", 8)
    canv.setFillColor(QUIET)
    canv.drawString(doc.leftMargin, 12 * mm, "micro:bit Sensor Tutorials · Forward Education · forwardedu.com")
    canv.drawRightString(letter[0] - doc.rightMargin, 12 * mm, f"Page {doc.page}")
    canv.restoreState()


def header(num, title, part, slug):
    left = [Paragraph(f"WORKSHEET {num} · MAKECODE TUTORIAL", KICKER),
            Paragraph(title, H1),
            Paragraph(part, SUB),
            Spacer(1, 10)]
    name = Table([["Name", "", "Date", ""]], colWidths=[34, 170, 30, 80], rowHeights=[20])
    name.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Body", 10),
        ("TEXTCOLOR", (0, 0), (-1, -1), QUIET),
        ("LINEBELOW", (1, 0), (1, 0), 0.6, QUIET),
        ("LINEBELOW", (3, 0), (3, 0), 0.6, QUIET),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    left.append(name)
    right = [qr(BASE + slug), Paragraph("Scan to open the tutorial", SMALL)]
    t = Table([[left, right]], colWidths=[365, 125])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("ALIGN", (1, 0), (1, 0), "CENTER"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    return t


def worksheet(ws):
    path = OUT / ws["file"]
    doc = SimpleDocTemplate(str(path), pagesize=letter, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=15 * mm, bottomMargin=20 * mm,
                            title=f"Worksheet {ws['num']}: {ws['title']}", author="Forward Education")
    story = [header(ws["num"], ws["title"], ws["part"], ws["slug"])]
    story += [Paragraph("1. Wire it up", H2), Paragraph(ws["wire_intro"], BODY), Spacer(1, 4),
              wiring(*ws["diagram"]), Spacer(1, 4)]
    story += [box(c) for c in ws["checks"]]
    story += [KeepTogether([Paragraph("2. " + ws["test_title"], H2), Paragraph(ws["test_intro"], BODY),
                            Spacer(1, 6), grid(*ws["table"])])]
    story += [PageBreak(), Paragraph(f"WORKSHEET {ws['num']} · {ws['title'].upper()}", KICKER),
              Paragraph("3. Reflect", H2)]
    for i, q in enumerate(ws["reflect"], 1):
        story.append(KeepTogether([Paragraph(f"{i}. {q}", BODY), WriteLines(4, gap=24), Spacer(1, 10)]))
    story.append(KeepTogether([Paragraph("4. Challenge", H2),
                               Paragraph("Tick each challenge you tried.", BODY), Spacer(1, 3)]
                              + [box(c) for c in ws["challenges"]]))
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return path


W3 = [(300, "0", 222, "signal"), (380, "3V", 210, "power"), (460, "GND", 198, "ground")]

SHEETS = [
    dict(num=1, title="Night Light", part="Light sensor", slug="light-sensor",
         file="worksheet-1-night-light.pdf",
         wire_intro="Unplug the micro:bit first. Clip each pin to the pad shown, then plug it back in.",
         diagram=("Light sensor (photoresistor)", "", [("S", 300), ("middle", 380), ("-", 460)], W3),
         checks=["S is clipped to <b>0</b>", "The middle pin is clipped to <b>3V</b>",
                 "The - pin is clipped to <b>GND</b>", "No clips touch each other"],
         test_title="Predict, then test",
         test_intro="Guess the light level from 0 (dark) to 100 (bright), then measure it.",
         table=(["Where I tested", "My prediction", "Actual reading"],
                [["Covered by my hand", "", ""], ["Normal classroom light", "", ""],
                 ["Under a desk", "", ""], ["Near a window", "", ""], ["A place I chose:", "", ""]],
                [210, 140, 140]),
         reflect=["Which reading surprised you most? Why?",
                  "What threshold did you choose for your night light? Why that number?",
                  "Name one place where a light that switches on by itself would help."],
         challenges=["Show a sleepy face in the dark and a happy face in the light",
                     "Press A to see the exact light level",
                     "Find the brightest spot in the classroom"]),
    dict(num=2, title="Thirsty Plant Alarm", part="Soil moisture sensor", slug="soil-moisture",
         file="worksheet-2-thirsty-plant-alarm.pdf",
         wire_intro="Unplug the micro:bit first. Clip each pin to the pad shown, then plug it back in. "
                    "Only the prongs go in the soil.",
         diagram=("Soil moisture sensor", "prongs go in the soil, this end stays dry",
                  [("S", 300), ("+", 380), ("-", 460)], W3),
         checks=["S is clipped to <b>0</b>", "+ is clipped to <b>3V</b>", "- is clipped to <b>GND</b>",
                 "Only the prongs go in the soil; the clips stay dry"],
         test_title="Predict, then test",
         test_intro="Guess the moisture from 0 (dry) to 100 (wet), then measure it.",
         table=(["Sample", "My prediction", "Actual reading"],
                [["Held in the air", "", ""], ["Dry soil", "", ""], ["Damp soil", "", ""],
                 ["Freshly watered soil", "", ""], ["Wet paper towel", "", ""]],
                [210, 140, 140]),
         reflect=["How far apart were your dry soil and watered soil readings?",
                  "What threshold did you choose for the sad face? Why is it between those two readings?",
                  "Why must the micro:bit and the clips stay dry?",
                  "Which plant in the school was the thirstiest?"],
         challenges=["Add a third face for soil that is too wet",
                     "Make the sad face flash so it is easier to notice",
                     "Test plants around the school"]),
    dict(num=3, title="Touch Counter", part="Touch sensor", slug="touch-sensor",
         file="worksheet-3-touch-counter.pdf",
         wire_intro="Unplug the micro:bit first. Clip each pin to the pad shown, then plug it back in.",
         diagram=("Touch sensor", "touch the round pad on the front",
                  [("SIG", 300), ("VCC", 380), ("GND", 460)], W3),
         checks=["SIG is clipped to <b>0</b>", "VCC is clipped to <b>3V</b>", "GND is clipped to <b>GND</b>",
                 "No clips touch each other"],
         test_title="Predict, then test",
         test_intro="How many times can you tap in 10 seconds? My prediction: ______",
         table=(["Trial", "Taps counted in 10 seconds"],
                [["1", ""], ["2", ""], ["3", ""], ["My best", ""]], [140, 350]),
         reflect=["What does the variable <b>count</b> remember?",
                  "What would happen if the program never set <b>count</b> back to 0?",
                  "Name one other thing a counter like this could count."],
         challenges=["Count taps in 10 seconds with the running time block",
                     "Show a check mark when the count reaches 20",
                     "Show a picture only while a finger is on the pad"]),
    dict(num=4, title="Parking Sensor", part="Sonar (ultrasonic distance sensor)", slug="sonar",
         file="worksheet-4-parking-sensor.pdf",
         wire_intro="Unplug the micro:bit first. The sonar has four pins. Check TRIG and ECHO carefully: "
                    "swapping them is the most common mistake.",
         diagram=("Sonar module (HC-SR04)", "point the two round eyes at the object",
                  [("VCC", 290), ("TRIG", 350), ("ECHO", 410), ("GND", 470)],
                  [(410, "0", 198, "signal"), (350, "1", 210, "signal"), (290, "3V", 222, "power"),
                   (470, "GND", 198, "ground")]),
         checks=["VCC is clipped to <b>3V</b>", "TRIG is clipped to <b>1</b>", "ECHO is clipped to <b>0</b>",
                 "GND is clipped to <b>GND</b>"],
         test_title="Measure and compare",
         test_intro="Measure each distance with a ruler, then read the sonar distance with a show number block.",
         table=(["Object", "Ruler (cm)", "Sonar (cm)", "Difference (cm)"],
                [["A book", "", "", ""], ["A wall", "", "", ""], ["My hand", "", "", ""],
                 ["A sweater or soft toy", "", "", ""], ["An object I chose:", "", "", ""]],
                [170, 105, 105, 110]),
         reflect=["Which object did the sonar measure most accurately? Why do you think so?",
                  "Which object was hardest to measure? What made it hard?",
                  "Why does the program check that the distance is more than 0?"],
         challenges=["Add a middle warning between 10 and 30 cm",
                     "Build a visitor counter with the on object closer than block",
                     "Measure things around the room and check them with a ruler"]),
    dict(num=5, title="Mood Light", part="RGB LED", slug="rgb-led",
         file="worksheet-5-mood-light.pdf",
         wire_intro="Unplug the micro:bit first. The LED needs no 3V clip: the pins power it.",
         diagram=("RGB LED module", "red, green and blue lights in one LED",
                  [("R", 290), ("G", 350), ("B", 410), ("-", 470)],
                  [(290, "0", 198, "signal"), (350, "1", 210, "signal"), (410, "2", 222, "signal"),
                   (470, "GND", 210, "ground")]),
         checks=["R is clipped to <b>0</b>", "G is clipped to <b>1</b>", "B is clipped to <b>2</b>",
                 "The common pin (-) is clipped to <b>GND</b>"],
         test_title="Predict, then test",
         test_intro="Use <b>set RGB LED to red green blue</b> to try each mix.",
         table=(["Red", "Green", "Blue", "My prediction", "Colour I saw"],
                [["255", "0", "0", "", ""], ["0", "255", "0", "", ""], ["0", "0", "255", "", ""],
                 ["255", "255", "0", "", ""], ["255", "0", "255", "", ""], ["0", "255", "255", "", ""],
                 ["255", "255", "255", "", ""], ["", "", "", "My own mix:", ""]],
                [60, 60, 60, 155, 155], ),
         reflect=["Which two colours mixed together to make yellow?",
                  "Why does the random colour from button A disappear after a moment?",
                  "Choose a mood and a colour for it. What red, green and blue values make it?"],
         challenges=["Mix red 255, green 0, blue 255 and name the colour",
                     "Make yellow and orange",
                     "Build a traffic light that goes green, yellow, then red",
                     "Turn the LED off with button B"]),
]


def answer_key():
    path = OUT / "answer-key-and-teacher-notes.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=letter, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=15 * mm, bottomMargin=20 * mm,
                            title="Answer key and teacher notes", author="Forward Education")
    bullet = ParagraphStyle("bullet", parent=BODY, leftIndent=12, bulletIndent=0, spaceAfter=3)
    s = [Paragraph("FOR TEACHERS", KICKER), Paragraph("Answer key and teacher notes", H1),
         Paragraph("micro:bit Sensor Tutorials, worksheets 1 to 5", SUB), Spacer(1, 8),
         Paragraph("Readings vary from sensor to sensor and room to room, so judge measurements by their "
                   "direction and spread, not exact numbers.", BODY)]

    def section(title, items):
        s.append(Paragraph(title, H2))
        for it in items:
            s.append(Paragraph(it, bullet, bulletText="•"))

    section("Worksheet 1: Night Light", [
        "<b>Readings:</b> covered by a hand and under a desk read lowest, near a window highest. "
        "Light from a window changes with the weather, so groups will differ.",
        "<b>Threshold:</b> any number between the covered and classroom readings works. Look for a reason "
        "tied to their own measurements.",
        "<b>Places:</b> porches, hallways, street lights, phone screens that dim in the dark."])
    section("Worksheet 2: Thirsty Plant Alarm", [
        "<b>Readings:</b> air reads lowest, a wet paper towel or freshly watered soil highest. Damp soil sits between.",
        "<b>Threshold:</b> it should fall between the dry soil and watered soil readings, so the face changes "
        "between the two.",
        "<b>Dry:</b> water conducts electricity and can short the micro:bit pins or corrode the clips."])
    section("Worksheet 3: Touch Counter", [
        "<b>Taps:</b> expect wide variation. A count far lower than the tapping suggests a loose SIG clip.",
        "<b>Variable:</b> count remembers how many taps there have been since the start or the last reset.",
        "<b>No reset:</b> the count would carry on from where it was and never return to 0 when A is pressed.",
        "<b>Other counters:</b> visitors through a door, laps, steps, votes."])
    section("Worksheet 4: Parking Sensor", [
        "<b>Accuracy:</b> hard, flat objects facing the sensor (a book, a wall) match the ruler most closely.",
        "<b>Hard to measure:</b> soft or angled objects absorb or bounce the sound away, so readings jump or show 0.",
        "<b>Checking for 0:</b> the sensor reports 0 when no echo returns. Without the check, nothing there "
        "would count as very close and show the stop sign."])
    s.append(Paragraph("Worksheet 5: Mood Light", H2))
    s.append(grid(["Red", "Green", "Blue", "Colour"],
                  [["255", "0", "0", "Red"], ["0", "255", "0", "Green"], ["0", "0", "255", "Blue"],
                   ["255", "255", "0", "Yellow"], ["255", "0", "255", "Magenta (pink-purple)"],
                   ["0", "255", "255", "Cyan (light blue)"], ["255", "255", "255", "White, often slightly tinted"]],
                  [60, 60, 60, 310], row_h=18))
    s.append(Spacer(1, 6))
    for it in ["<b>Yellow:</b> red and green light together. This surprises students who mix paint, where red "
               "and green make brown.",
               "<b>Disappearing colour:</b> the forever loop keeps running and sets the next colour within a "
               "second. One fix is to remove the forever loop and change colours with buttons only.",
               "<b>Uneven colours:</b> the three small lights are not equally bright on some LEDs. That is normal."]:
        s.append(Paragraph(it, bullet, bulletText="•"))
    doc.build(s, onFirstPage=footer, onLaterPages=footer)
    return path


for ws in SHEETS:
    print(worksheet(ws))
print(answer_key())
