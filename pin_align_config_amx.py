########################## Base Parameters ##########################

DEFAULT_PIXELS_PER_MM = 13
ROD_LENGTH = 18
PIN_ALIGN_Y_UP = False
PIN_ALIGN_Z_UP = True

DEFAULT_IMAGE_WIDTH_CENTER = 439
DEFAULT_IMAGE_HEIGHT_CENTER = 511

########################## pin,body,base ##########################
# slice(offset, offset)
# offset = Y + height
DEFAULT_ROI_Y1 = 386
DEFAULT_ROI_Y2 = 636

DEFAULT_HEIGHT = slice(DEFAULT_ROI_Y1, DEFAULT_ROI_Y2)

# Pin tip
# offset = X + width
PIN_TIP_X1 = 419
PIN_TIP_X2 = 509

PIN_TIP = slice(PIN_TIP_X1, PIN_TIP_X2)

# Pin body
PIN_BODY_X1 = 509
PIN_BODY_X2 = 599

PIN_BODY = slice(PIN_BODY_X1, PIN_BODY_X2)

# Pin base
PIN_BASE_X1 = 599
PIN_BASE_X2 = 691

PIN_BASE = slice(PIN_BASE_X1, PIN_BASE_X2)

########################## Tilt check  parameters ##########################
# Setting the width = -10 the width of the image
TILT_CHECK_X1 = 641
TILT_CHECK_X2 = 691

TILT_CHECK_ROI_WIDTH = slice(TILT_CHECK_X1, TILT_CHECK_X2)

# Top crop
TILT_CHECK_TOP_Y1 = 411
TILT_CHECK_TOP_Y2 = 481

TILT_CHECK_TOP = slice(TILT_CHECK_TOP_Y1, TILT_CHECK_TOP_Y2)

# Bottom crop
TILT_CHECK_BOTTOM_Y1 = 541
TILT_CHECK_BOTTOM_Y2 = 611

TILT_CHECK_BOTTOM = slice(TILT_CHECK_BOTTOM_Y1, TILT_CHECK_BOTTOM_Y2)

########################## Pin check parameters ##########################

# Top crop
PIN_CHECK_TOP_Y1 = 386
PIN_CHECK_TOP_Y2 = 481

PIN_CHECK_TOP = slice(PIN_CHECK_TOP_Y1, PIN_CHECK_TOP_Y2)

# Bottom crop
PIN_CHECK_BOTTOM_Y1 = 541
PIN_CHECK_BOTTOM_Y2 = 636

PIN_CHECK_BOTTOM = slice(PIN_CHECK_BOTTOM_Y1, PIN_CHECK_BOTTOM_Y2)

TOTAL_WIDTH = slice(PIN_TIP_X1, PIN_BASE_X2)
########################## Small & Big Box parameters ##########################
BOX_X_IN = 439
BOX_Y_IN = 511

SMALL_BOX_X1 = BOX_X_IN - 15
SMALL_BOX_X2 = BOX_X_IN + 15

SMALL_BOX_WIDTH = slice(SMALL_BOX_X1, SMALL_BOX_X2)

SMALL_BOX_Y1 = BOX_Y_IN - 15
SMALL_BOX_Y2 = BOX_Y_IN + 15

SMALL_BOX_HEIGHT = slice(SMALL_BOX_Y1, SMALL_BOX_Y2)

BIG_BOX_X1 = 419
BIG_BOX_X2 = 691

BIG_BOX_WIDTH = slice(BIG_BOX_X1, BIG_BOX_X2)

BIG_BOX_Y1 = 386
BIG_BOX_Y2 = 636

BIG_BOX_HEIGHT = slice(BIG_BOX_Y1, BIG_BOX_Y2)

########################## X,Y,Z check parameters ##########################
MIN_X = -2
MAX_X = 2

MIN_Y = -2
MAX_Y = 2

MIN_Z = -2
MAX_Z = 2
# # Y motor axis is up if = 1
# # Y motor axis is down if = 0
# PIN_ALIGN_Y_UP = 1

# # Z motor axis is up if = 1
# # Z motor axis is down if = 0
# PIN_ALIGN_Z_UP = 0

# PIN_ALIGN_DEFAULT_ROI_WIDTH = 150
# PIN_ALIGN_DEFAULT_ROI_WIDTH_OFFSET = 410
# PIN_ALIGN_DEFAULT_PIXELS_PER_MM = 26
# PIN_ALIGN_DEFAULT_IMAGE_WIDTH_CENTER = 470
# PIN_ALIGN_DEFAULT_IMAGE_HEIGHT_CENTER = 453
