########################## Base Parameters ##########################

DEFAULT_PIXELS_PER_MM = 20
ROD_LENGTH = 18
X_POS_DIR = 'LEFT'
Y_POS_DIR = 'UP'
Z_POS_DIR = 'DOWN'
PIN_ALIGN_Y_UP = True
PIN_ALIGN_Z_UP = False

X_CENTER = 409
Y_CENTER = 487

########################## pin,body,base ##########################
# slice(offset, offset)
# offset = Y + height
DEFAULT_ROI_Y1 = 362
DEFAULT_ROI_Y2 = 612

DEFAULT_HEIGHT = slice(DEFAULT_ROI_Y1, DEFAULT_ROI_Y2)

# Pin tip
# offset = X + width
PIN_TIP_X1 = 369
PIN_TIP_X2 = 467

PIN_TIP = slice(PIN_TIP_X1, PIN_TIP_X2)

# Pin body
PIN_BODY_X1 = 467
PIN_BODY_X2 = 565

PIN_BODY = slice(PIN_BODY_X1, PIN_BODY_X2)

# Pin base
PIN_BASE_X1 = 565
PIN_BASE_X2 = 664

PIN_BASE = slice(PIN_BASE_X1, PIN_BASE_X2)

########################## Tilt check  parameters ##########################
# Setting the width = -10 the width of the image
TILT_CHECK_X1 = 614
TILT_CHECK_X2 = 664

TILT_CHECK_ROI_WIDTH = slice(TILT_CHECK_X1, TILT_CHECK_X2)

# Top crop
TILT_CHECK_TOP_Y1 = 382
TILT_CHECK_TOP_Y2 = 452

TILT_CHECK_TOP = slice(TILT_CHECK_TOP_Y1, TILT_CHECK_TOP_Y2)

# Bottom crop
TILT_CHECK_BOTTOM_Y1 = 522
TILT_CHECK_BOTTOM_Y2 = 592

TILT_CHECK_BOTTOM = slice(TILT_CHECK_BOTTOM_Y1, TILT_CHECK_BOTTOM_Y2)

########################## Pin check parameters ##########################

# Top crop
PIN_CHECK_TOP_Y1 = 362
PIN_CHECK_TOP_Y2 = 452

PIN_CHECK_TOP = slice(PIN_CHECK_TOP_Y1, PIN_CHECK_TOP_Y2)

# Bottom crop
PIN_CHECK_BOTTOM_Y1 = 522
PIN_CHECK_BOTTOM_Y2 = 612

PIN_CHECK_BOTTOM = slice(PIN_CHECK_BOTTOM_Y1, PIN_CHECK_BOTTOM_Y2)

TOTAL_WIDTH = slice(PIN_TIP_X1, PIN_BASE_X2)

########################## X,Y,Z check parameters ##########################
MIN_X = -2
MAX_X = 2

MIN_Y = -2
MAX_Y = 2

MIN_Z = -2
MAX_Z = 2

########################## Small & Big Box parameters ##########################
BOX_X_IN = 409
BOX_Y_IN = 487

SMALL_BOX_X1 = BOX_X_IN + (MIN_Z * DEFAULT_PIXELS_PER_MM)
SMALL_BOX_X2 = BOX_X_IN + (MAX_Z * DEFAULT_PIXELS_PER_MM)

SMALL_BOX_WIDTH = slice(SMALL_BOX_X1, SMALL_BOX_X2)

SMALL_BOX_Y1 = BOX_Y_IN + (MIN_Y * DEFAULT_PIXELS_PER_MM)
SMALL_BOX_Y2 = BOX_Y_IN + (MAX_Y * DEFAULT_PIXELS_PER_MM)

SMALL_BOX_HEIGHT = slice(SMALL_BOX_Y1, SMALL_BOX_Y2)

BIG_BOX_X1 = 369
BIG_BOX_X2 = 664

BIG_BOX_WIDTH = slice(BIG_BOX_X1, BIG_BOX_X2)

BIG_BOX_Y1 = 362
BIG_BOX_Y2 = 612

BIG_BOX_HEIGHT = slice(BIG_BOX_Y1, BIG_BOX_Y2)

########################## ROI W/H parameters ##########################
INPUT_ROI_WIDTH = 295
INPUT_ROI_HEIGHT = 250
