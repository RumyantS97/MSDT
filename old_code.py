import turtle as te
import time

WRITE_STEP = 15  # Sampling times of Bessel function
SPREED = 5
WIDTH = 600  # Interface width
HEIGHT = 500  # Interface height
XH = 0  # Record the handle of the previous Bessel function
YH = 0


def bezier(p1, p2, t):  # First order Bessel function
    return p1 * (1 - t) + p2 * t


def bezier_2(x1, y1, x2, y2, x3, y3):  # Second-order Bessel function
    te.goto(x1, y1)
    te.pendown()
    for t in range(0, WRITE_STEP + 1):
        x = bezier(bezier(x1, x2, t / WRITE_STEP),
                   bezier(x2, x3, t / WRITE_STEP), t / WRITE_STEP)
        y = bezier(bezier(y1, y2, t / WRITE_STEP),
                   bezier(y2, y3, t / WRITE_STEP), t / WRITE_STEP)
        te.goto(x, y)
    te.penup()


def bezier_3(x1, y1, x2, y2, x3, y3, x4, y4):  # Third-order Bessel function
    x1 = -WIDTH / 2 + x1
    y1 = HEIGHT / 2 - y1
    x2 = -WIDTH / 2 + x2
    y2 = HEIGHT / 2 - y2
    x3 = -WIDTH / 2 + x3
    y3 = HEIGHT / 2 - y3
    x4 = -WIDTH / 2 + x4
    y4 = HEIGHT / 2 - y4  # Coordinate transformation
    te.goto(x1, y1)
    te.pendown()
    for t in range(0, WRITE_STEP + 1):
        x = bezier(bezier(bezier(x1, x2, t / WRITE_STEP), bezier(x2, x3, t / WRITE_STEP), t / WRITE_STEP),
                   bezier(bezier(x2, x3, t / WRITE_STEP), bezier(x3, x4, t / WRITE_STEP), t / WRITE_STEP), t / WRITE_STEP)
        y = bezier(bezier(bezier(y1, y2, t / WRITE_STEP), bezier(y2, y3, t / WRITE_STEP), t / WRITE_STEP),
                   bezier(bezier(y2, y3, t / WRITE_STEP), bezier(y3, y4, t / WRITE_STEP), t / WRITE_STEP), t / WRITE_STEP)
        te.goto(x, y)
    te.penup()


def move_to(x, y):  # Move to svg coordinates (x, y)
    te.penup()
    te.goto(-WIDTH / 2 + x, HEIGHT / 2 - y)


def line(x1, y1, x2, y2):  # Connect two points under svg coordinates
    te.penup()
    te.goto(-WIDTH / 2 + x1, HEIGHT / 2 - y1)
    te.pendown()
    te.goto(-WIDTH / 2 + x2, HEIGHT / 2 - y2)
    te.penup()


def line_to(dx, dy):  # Connect the current point and the point with relative coordinates (dx, dy)
    te.pendown()
    te.goto(te.xcor() + dx, te.ycor() - dy)
    te.penup()


def line_to(x, y):  # Connect the current point and svg coordinates (x, y)
    te.pendown()
    te.goto(-WIDTH / 2 + x, HEIGHT / 2 - y)
    te.penup()


def horizontal(x):  # Make the horizontal line with the abscissa x in the svg coordinates
    te.pendown()
    te.setx(x - WIDTH / 2)
    te.penup()


def horizontal(dx):  # Make the horizontal line with relative abscissa dx
    te.seth(0)
    te.pendown()
    te.fd(dx)
    te.penup()


def vertical(dy):  # Make the vertical line with the relative ordinate dy
    te.seth(-90)
    te.pendown()
    te.fd(dy)
    te.penup()
    te.seth(0)


def polyline(x1, y1, x2, y2, x3, y3):  # Make a polyline under svg coordinates
    te.penup()
    te.goto(-WIDTH / 2 + x1, HEIGHT / 2 - y1)
    te.pendown()
    te.goto(-WIDTH / 2 + x2, HEIGHT / 2 - y2)
    te.goto(-WIDTH / 2 + x3, HEIGHT / 2 - y3)
    te.penup()


def curve_to(x1, y1, x2, y2, x, y):  # Third-order Bezier curve to (x, y)
    te.penup()
    X_now = te.xcor() + WIDTH / 2
    Y_now = HEIGHT / 2 - te.ycor()
    bezier_3(X_now, Y_now, x1, y1, x2, y2, x, y)
    global XH
    global YH
    XH = x - x2
    YH = y - y2


def curve_to_r(x1, y1, x2, y2, x, y):  # Third-order Bezier curve to relative coordinates (x, y)
    te.penup()
    X_now = te.xcor() + WIDTH / 2
    Y_now = HEIGHT / 2 - te.ycor()
    bezier_3(X_now, Y_now, X_now + x1, Y_now + y1,
             X_now + x2, Y_now + y2, X_now + x, Y_now + y)
    global XH
    global YH
    XH = x - x2
    YH = y - y2


def smooth(x2, y2, x, y):  # Smooth the third-order Bezier curve to (x, y)
    global XH
    global YH
    te.penup()
    X_now = te.xcor() + WIDTH / 2
    Y_now = HEIGHT / 2 - te.ycor()
    bezier_3(X_now, Y_now, X_now + XH, Y_now + YH, x2, y2, x, y)
    XH = x - x2
    YH = y - y2


    def smooth_r(x2, y2, x, y):  # Smooth the third-order Bezier curve to relative coordinates (x, y)
        global XH
        global YH
        te.penup()
        X_now = te.xcor() + WIDTH / 2
        Y_now = HEIGHT / 2 - te.ycor()
        bezier_3(X_now, Y_now, X_now + XH, Y_now + YH,
                 X_now + x2, Y_now + y2, X_now + x, Y_now + y)
        XH = x - x2
        YH = y - y2

    te.tracer(10)
    te.setup(WIDTH, HEIGHT, 0, 0)
    te.pensize(1)
    te.speed(SPREED)
    te.penup()
    # Layer_2
    time.sleep(20)
    te.color("black", "#F2F2F2")  # Coat
    move_to(61, 462)
    te.begin_fill()
    smooth_r(12, -41, 27, -58)
    curve_to_r(-6, -36, 6, -118, 9, -132)
    curve_to_r(-15, -27, -23, -51, -26, -74)
    curve_to_r(4, -66, 38, -105, 65, -149)
    horizontal(486)
    curve_to_r(12, 24, 40, 99, 33, 114)
    curve_to_r(39, 82, 55, 129, 39, 144)
    smooth_r(-31, 23, -39, 28)
    smooth_r(-12, 37, -12, 37)
    line_to(50, 92)
    horizontal(445)
    smooth_r(-29, -38, -31, -46)
    smooth_r(78, -107, 72, -119)
    smooth(355, 178, 340, 176)
    smooth(272, 63, 264, 64)
    smooth_r(-29, 67, -27, 73)
    curve_to(99, 292, 174, 428, 173, 439)
    smooth_r(-8, 23, -8, 23)
    line_to(61, 462)
    te.end_fill()
    move_to(60.5, 461.5)  # Shadow
    te.color("black", "#D3DFF0")
    te.begin_fill()
    curve_to_r(0, 0, 17, -42, 27, -59)
    curve_to_r(-6, -33, 6, -128, 10, -133)
    curve_to_r(-15, -10, -27, -66, -27.285, -75)
    te.pencolor("#D3DFF0")
    curve_to_r(12.285, 11, 82.963, 156, 82.963, 156)
    te.pencolor("black")
    smooth_r(12.322, 75, 19.322, 86)
    curve_to_r(-1, 11, -8, 25, -8, 25)
    horizontal(60.5)
    te.end_fill()
    move_to(444.5, 464)
    te.begin_fill()
    curve_to_r(0, 0, -29, -36, -31, -46)
    smooth_r(53.59, -82.337, 53.59, -82.337)
    te.pencolor("#D3DFF0")
    smooth_r(86.41, -47.663, 96.072, -54.85)
    curve_to(563.5, 297.5, 570.5, 299.5, 518.5, 334)
    te.pencolor("black")
    curve_to_r(-2, 16, -12, 33, -12, 37)
    smooth_r(50, 92, 50, 93)
    horizontal(444.5)
    te.end_fill()
    move_to(195, 49)
    te.begin_fill()
    te.pencolor("#D3DFF0")
    polyline(195, 49, 175.5, 106.5, 202.522, 49)
    te.pencolor("black")
    horizontal(195)
    te.pencolor("#D3DFF0")
    te.end_fill()
    move_to(327.997, 49)
    te.begin_fill()
    te.pencolor("#D3DFF0")
    curve_to_r(0, 0, 11.503, 121.087, 13.503, 128.087)
    curve_to_r(11, 2, 54, 37, 54, 37)
    line_to(-40, -165.087)
    te.pencolor("black")
    horizontal(327.997)
    te.pencolor("#D3DFF0")
    te.end_fill()
    te.pencolor("black")
    line(94.5, 397.5, 107.5, 373.5)  # Wrinkles
    line(122.5, 317.5, 95.875, 274.699)
    line(122.5, 341.5, 141.5, 402.5)
    line(141.5, 409.5, 153.5, 431.5)
    # line(328,47.712,344,175.977)
    line(340.023, 49, 360.5, 144)
    # line(353.5,47.5,395.5,208.5)
    line(478.5, 95.5, 518.5, 161.5)
    line(518.5, 332.5, 460.5, 359.5)
    polyline(506.5, 369.5, 493.5, 402.5, 502.5, 443.5)
    move_to(530, 429)
    curve_to_r(4, 16, -5, 33, -5, 33)
    # Layer_3
    te.color("black", "#2b1d2a")  # Inside the jacket
    move_to(225, 462)
    te.begin_fill()
    horizontal(165)
    smooth_r(9, -15, 8, -25)
    curve_to_r(-47, -126, 6, -212, 12, -225)
    curve_to(185, 305, 202, 428, 225, 462)
    line_to(225, 462)
    te.end_fill()
    move_to(390, 462)
    te.begin_fill()
    curve_to_r(10, -23, 34, -180, 35, -222)  # !!!227
    curve_to_r(7, 4, 54, 45, 61, 61)  # 61
    smooth_r(-73, 101, -72, 118)
    curve_to_r(5, 15, 31, 46, 31, 45)
    line_to(390, 462)
    te.end_fill()
    # Layer_4
    te.color("black", "#2b1d29")  # Inside the jacket
    move_to(225, 462)
    te.begin_fill()
    curve_to_r(-28, -50, -40, -166, -40, -250)
    curve_to_r(6, 51, -6, 87, 45, 106)
    smooth_r(64, 27, 89, 24)
    smooth_r(49, -18, 56, -20)
    smooth_r(50, -10, 51, -85)
    curve_to_r(0, 29, -25, 201, -36, 225)
    line_to(225, 462)
    te.end_fill()
    # Layer_5
    te.color("black", "#3D3D3D")  # Clothes
    move_to(225, 462)
    te.begin_fill()
    curve_to_r(-5, -5, -22, -53, -23, -70)
    line_to(32, -13)
    curve_to_r(3, -25, 6, -28, 12, -36)
    smooth_r(13, -12, 16, -12)
    vertical(-2)
    curve_to_r(45, 20, 64, 14, 94, 1)
    vertical(2)
    curve_to_r(8, -2, 15, 2, 17, 4)
    smooth_r(0, 6, -2, 9)
    curve_to_r(10, 10, 10, 29, 11, 33)
    smooth_r(23, 4, 25, 6)
    smooth_r(-17, 83, -17, 78)
    line_to(225, 462)
    te.end_fill()
    # Layer_6
    te.color("black", "#968281")  # Neck
    move_to(262, 329)
    te.begin_fill()
    vertical(17)
    curve_to_r(1, 2, 44, 14, 45, 15)
    smooth_r(3, 12, 3, 12)
    horizontal(3)
    vertical(-5)
    curve_to_r(1, -3, 4, -6, 5, -7)
    line_to(36, -14)
    curve_to_r(1, -1, 3, -16, 2, -17)
    curve_to(318, 348, 296, 344, 262, 329)
    te.end_fill()
    # Layer_8
    te.color("black", "#E7F1FF")  # White folds
    move_to(225, 462)
    te.begin_fill()
    line_to(-3, -5)  # -3,-3,-3,-5
    curve_to_r(0, -2, 4, -4, 5, -6)
    smooth_r(16, 3, 19, -8)
    smooth_r(0, -7, 0, -11)
    smooth_r(5, -8, 9, -5)
    smooth_r(19, -8, 19, -11)
    smooth_r(6, -7, 6, -7)
    smooth_r(7, -2, 9, -4)
    line_to(41, -2)
    line_to(12, 9)
    smooth_r(3, 15, 7, 18)
    smooth_r(15, 4, 17, 4)
    smooth_r(4, -4, 6, -4)
    smooth_r(6, 4, 5, 9)
    smooth_r(0, 9, 0, 9)
    smooth_r(1, 7, 7, 6)
    smooth_r(8, 0, 8, 0)
    line_to(-2, 8)
    line_to(225, 462)
    te.end_fill()
    te.pensize(2)
    move_to(240, 450)
    smooth_r(0, 9, 3, 12)
    move_to(372, 462)
    curve_to_r(-2, -4, -5, -29, -7, -28)
    te.pensize(1)
    # Layer_7
    te.color("black", "#A2B8D6")  # Collar
    move_to(262, 331)
    te.begin_fill()
    curve_to_r(0, 8, -1, 13, 0, 15)
    smooth_r(43, 14, 45, 15)
    line_to(3, 12)
    horizontal(3)
    smooth_r(-1, -3, 0, -5)
    line_to(5, -7)
    line_to(36, -14)
    curve_to_r(1, -1, 2, -12, 2, -15)
    smooth_r(25, -2, 15, 13)
    curve_to_r(-2, 4, -7, 29, -7, 32)
    smooth_r(-35, 19, -41, 22)
    smooth_r(-9, 14, -12, 14)
    smooth_r(-7, -12, -14, -15)
    curve_to_r(-19, -2, -41, -25, -41, -25)
    smooth_r(-10, -26, -10, -30)
    smooth(255, 332, 262, 331)
    te.end_fill()
    move_to(262, 346)
    line_to(-12, -6)
    move_to(369, 333)
    curve_to_r(2, 4, -6, 10, -15, 14)
    # Layer_9
    te.color("black", "#151515")  # Tie
    move_to(247, 358)
    te.begin_fill()
    curve_to_r(-5, 3, -8, 20, -6, 23)
    curve_to_r(25, 21, 50, 17, 50, 17)
    line_to(-23, 64)
    horizontal(22)
    smooth_r(1, -13, 2, -16)
    line_to(13, -50)
    curve_to_r(2, 2, 7, 3, 10, 1)
    smooth_r(18, 65, 18, 65)
    horizontal(19)
    line_to(-24, -65)
    curve_to_r(21, 5, 39, -10, 44, -13)
    curve_to_r(5, -20, 1, -21, 0, -24)
    curve_to_r(-18, -2, -49, 15, -52, 17)
    smooth_r(-11, -3, -15, -1)
    smooth(252, 356, 247, 358)
    te.end_fill()
    # Layer_10
    te.color("black", "#A2B8D6")  # Collar (through bow tie)
    move_to(297, 387)
    te.begin_fill()
    line_to(-11, 6)
    curve_to_r(-1, 0, -20, -7, -30, -19)
    curve_to(259, 373, 297, 385, 297, 387)
    te.end_fill()
    move_to(323, 384)
    te.begin_fill()
    line_to(8, 7)
    line_to(30, -14)
    curve_to_r(1, -1, 5, -6, 4, -7)
    smooth(329, 379, 323, 384)
    te.end_fill()
    # Layer_11
    te.color("black", "#F3EEEB")  # Face
    move_to(185, 212)
    te.begin_fill()
    curve_to_r(4, -9, 46, -77, 52, -75)
    curve_to_r(-2, -17, 19, -68, 27, -73)
    curve_to_r(16, 15, 71, 108, 76, 112)
    smooth_r(76, 53, 86, 60)
    curve_to_r(0, 65, -27, 75, -31, 76)
    curve_to_r(-50, 28, -70, 30, -85, 30)
    smooth_r(-77, -22, -86, -26)
    curve_to(180, 302, 186, 228, 185, 212)
    te.end_fill()
    # Layer_12
    te.color("black", "#2B1D29")  # Hair
    move_to(189, 202)
    te.begin_fill()
    curve_to_r(-1, 22, 19, 51, 19, 51)
    smooth_r(-10, -42, 7, -92)
    curve_to(212, 168, 196, 189, 189, 202)
    te.end_fill()
    move_to(221, 155)
    te.begin_fill()
    curve_to_r(-2, 6, 5, 48, 5, 48)
    smooth_r(18, -28, 20, -48)
    curve_to_r(-5, 24, 4, 43, 7, 50)
    curve_to_r(-10, -49, 3, -72, 13, -106)
    curve_to_r(-2, -7, -3, -32, -3, -35)
    curve_to_r(-17, 18, -27, 71, -27, 71)
    line_to(221, 155)
    te.end_fill()
    move_to(264, 64)
    te.begin_fill()
    curve_to_r(-4, 5, 14, 100, 14, 100)
    smooth_r(-6, -79, -5, -85)
    curve_to_r(0, 98, 49, 139, 49, 139)
    smooth_r(8, -50, 3, -65)
    smooth(272, 64, 264, 64)
    te.end_fill()
    move_to(342, 176)
    te.begin_fill()
    curve_to_r(-1, 27, -10, 57, -10, 57)
    smooth_r(20, -33, 17, -54)
    line_to(342, 176)
    te.end_fill()
    te.penup()
    te.begin_fill()
    polyline(349, 180, 353, 203, 361, 203)
    polyline(361, 203, 362, 188, 349, 180)
    te.end_fill()
    # Layer_13
    te.pensize(2)
    move_to(210, 180)  # Eyebrows
    curve_to_r(5, -4, 63, 9, 63, 14)
    move_to(338, 193)
    curve_to_r(0, -3, 18, -6, 18, -6)
    te.pensize(1)
    # Layer_14
    te.color("black", "#D1D1D1")  # Eye 1
    te.pensize(2)
    move_to(206, 212)
    te.begin_fill()
    line_to(15, -7)
    curve_to_r(4, -1, 26, -2, 30, 0)
    smooth_r(10, 3, 12, 7)
    te.pencolor("#D1D1D1")
    te.pensize(1)
    smooth_r(2, 27, -1, 30)
    smooth_r(-39, 5, -44, 1)
    smooth(206, 212, 206, 212)
    te.end_fill()
    move_to(384, 204)
    te.begin_fill()
    te.pencolor("black")
    te.pensize(2)
    curve_to_r(-3, -1, -18, -1, -28, 1)
    smooth_r(-9, 6, -10, 9)
    te.pencolor("#D1D1D1")
    te.pensize(1)
    smooth_r(3, 18, 6, 23)
    smooth_r(38, 6, 40, 4)
    smooth_r(10, -9, 13, -22)
    te.pencolor("black")
    te.pensize(2)
    line_to(384, 204)
    te.end_fill()
    # Layer_15
    te.color("#0C1631", "#0C1631")  # Eye 2
    te.pensize(1)
    move_to(216, 206)
    te.begin_fill()
    curve_to_r(-1, 5, 0, 26, 7, 35)
    smooth_r(30, 2, 33, 0)
    smooth_r(5, -31, 2, -34)
    smooth(219, 203, 216, 206)
    te.end_fill()
    move_to(354, 207)
    te.begin_fill()
    curve_to_r(-2, 1, 2, 29, 4, 31)
    smooth_r(30, 3, 33, 1)
    smooth_r(6, -24, 4, -27)
    line_to(-11, -8)
    curve_to(382, 204, 357, 206, 354, 207)
    te.end_fill()
    # Layer_17
    te.color("#F5F5F5", "#F5F5F5")  # Eye 3
    move_to(253, 211)
    te.begin_fill()
    curve_to_r(-3, 0, -8, 8, 1, 10)
    smooth(258, 210, 253, 211)
    te.end_fill()
    move_to(392, 209)
    te.begin_fill()
    line_to(4, 3)
    vertical(4)
    line_to(-4, 2)
    curve_to(386, 214, 392, 209, 392, 209)
    te.end_fill()
    # Layer_18
    te.color("#352F53", "#352F53")  # Eye 4
    move_to(219, 229)
    te.begin_fill()
    smooth_r(2, -5, 6, -4)
    smooth_r(18, 13, 27, 1)
    curve_to_r(3, 0, 5, 3, 5, 3)
    vertical(13)
    horizontal(224)
    line_to(219, 229)
    te.end_fill()
    move_to(357, 227)
    te.begin_fill()
    smooth_r(4, -6, 10, -2)
    smooth_r(10, 13, 19, 1)
    curve_to_r(6, 0, 8, 6, 8, 6)
    line_to(-2, 9)
    curve_to_r(-12, 3, -29, 0, -32, -2)
    smooth(357, 227, 357, 227)
    te.end_fill()
    # Layer_19
    te.color("#9A90CB", "#9A90CB")  # Eye 5
    move_to(227, 231)
    te.begin_fill()
    curve_to_r(-6, 0, -5, 5, -3, 8)
    smooth_r(24, 2, 27, 0)
    smooth_r(0, -8, -1, -8)
    smooth(234, 231, 227, 231)
    te.end_fill()
    move_to(361, 227)
    te.begin_fill()
    curve_to_r(2, 18, 26, 14, 30, 6)
    smooth_r(-1, -3, -2, -4)
    smooth_r(-15, 9, -24, -4)
    curve_to(363, 224, 361, 225, 361, 227)
    te.end_fill()
    # Layer_16
    te.pencolor("black")  # Eyes (lines)
    te.pensize(3)
    # Moveto(206,213)
    # lineto(14,-8)
    # curveto_r(3,-1,30,0,33,1)
    # lineto(10,6)
    move_to(225, 215)
    curve_to_r(10, 28, 22, 16, 24, 6)
    move_to(365, 219)
    curve_to_r(4, 14, 18, 24, 22, -3)
    te.pensize(2)
    line(240.5, 207.5, 227.5, 211.5)
    line(245.5, 209.5, 227.5, 214.5)
    line(247.5, 211.5, 227.5, 217.5)
    line(247.5, 214.5, 229.5, 220.5)
    line(247.5, 218.5, 230.5, 223.5)
    line(246.5, 222.5, 232.5, 226.5)
    line(244.5, 225.5, 234.5, 228.5)
    line(377.5, 207.5, 367.5, 210.5)
    line(384.5, 207.5, 366.5, 212.5)
    line(385.5, 210.5, 366.5, 215.5)
    line(384.5, 213.5, 366.5, 218.5)
    line(384.5, 215.5, 367.5, 220.5)
    line(384.5, 218.5, 368.5, 223.5)
    # line(383.5,220.5,368.5,225.5)
    line(382.5, 223.5, 370.5, 227.5)
    # line(381.5,226.5,373.5,229.5)
    # Layer_20
    te.pencolor("black")
    move_to(309, 270)  # Nose, mouth
    curve_to_r(0, 0, 4, 7, 1, 9)
    line(296.5, 307.5, 303.5, 307.5)
    move_to(315, 307)
    smooth_r(10, -1, 10, 2)
    te.penup()
    te.hideturtle()
    te.update()
    te.done()
