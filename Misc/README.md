# pin_align
Scripts for detecting pin alignment issues from top view camera

Designed by Edwin Lazo, Jean Jakoncic, Herbert J. Bernstein
Copyright 29 Jan 2019, Herbert J. Bernstein
as a copyleft for the GPL and LGPL
Revised 14 Feb 2019, Herbert J. Bernstein, Edwin Lazo
  improve base tilt detection
  use pgm instead of jpg
Revised 12 Mar 2019, Edwin Lazo, Herbert J. Bernstein
  Extended configuration after camera realignment

 YOU MAY REDISTRIBUTE THE PIN_ALIGN PACKAGE UNDER THE TERMS OF THE GPL
                     
 ALTERNATIVELY YOU MAY REDISTRIBUTE THE PIN_ALIGN API UNDER THE TERMS
 OF THE LGPL

/*************************** GPL NOTICES ******************************
 *                                                                    *
 * This program is free software; you can redistribute it and/or      *
 * modify it under the terms of the GNU General Public License as     *
 * published by the Free Software Foundation; either version 2 of     *
 * (the License, or (at your option) any later version.               *
 *                                                                    *
 * This program is distributed in the hope that it will be useful,    *
 * but WITHOUT ANY WARRANTY; without even the implied warranty of     *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the      *
 * GNU General Public License for more details.                       *
 *                                                                    *
 * You should have received a copy of the GNU General Public License  *
 * along with this program; if not, write to the Free Software        *
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA           *
 * 02111-1307  USA                                                    *
 *                                                                    *
 **********************************************************************/

/************************* LGPL NOTICES *******************************
 *                                                                    *
 * This library is free software; you can redistribute it and/or      *
 * modify it under the terms of the GNU Lesser General Public         *
 * License as published by the Free Software Foundation; either       *
 * version 2.1 of the License, or (at your option) any later version. *
 *                                                                    *
 * This library is distributed in the hope that it will be useful,    *
 * but WITHOUT ANY WARRANTY; without even the implied warranty of     *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU  *
 * Lesser General Public License for more details.                    *
 *                                                                    *
 * You should have received a copy of the GNU Lesser General Public   *
 * License along with this library; if not, write to the Free         *
 * Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,    *
 * MA  02110-1301  USA                                                *
 *                                                                    *
 **********************************************************************/

 The pin_align package is a set of scripts the process images from
a comera looking down on a mounted pin (with sample) and try to detect
issues with the pin and report them before a tilted or bent pin causes
collisions.

  The approach followed is to take two images, one at omega=0 viewing the
X-Z plane, and one at omega=90 viewing the X-Y plane.  If the pin is
perfectly straight and centered, the two images should superimpose.

  The scripts are


  pin_align_config.sh -- configurable pin_align settings to be
      incoroprated in the pin_align scripts
  all_pin.sh -- a top level example of a script using pin_align.sh
  pin_align.sh -- the main service script for the run
  pin_align_prep.sh -- a script to convert a single image into enchanced
      sub-images showing the tip of the pin, hopefully with sample,
      the base of the pin, and the cap below the pin.
  pin_align_split_info.sh -- a script to make the imagemagick image info
      and populate a list of variable descibing the image geometry

pin_align.sh
        See the text of the file for details.  The important settings
        are:

        #  *** UNCOMMENT THE FOLLOWING LINE TO ENABLE DEBUG MODE ***
        #  export PIN_ALIGN_DEBUG="yes"

        #  ***  EDIT THE FOLLOWING LINE TO CHANGE THE TILT LIMIT ***
        PIN_ALIGN_DEFAULT_TILT_LIMIT="25"

        # PIN_ALIGN_ROI_WIDTH, PIN_ALIGN_ROI_HEIGHT, in pixels, and
        # PIN_ALIGN_ROI_WIDTH_OFFSET and PIN_ALIGN_ROI_HEIGHT__OFFSET
        # define the region of interest within which the analysis of
        # pin alignment is done.  The full image within which the roi
        # is defined is implicitly assumed to be 1280x1024, but those
        # values are not explicitly used, but the centers 
        # PIN_ALIGN_IMAGE_WIDTH_CENTER and PIN_ALIGN_IMAGE_HEIGHT_CENTER
        # of the original image in pixels are given

        # The following six lines give the default values
        # *** EDIT THESE LINES TO CHANGE THESE PARAMETERS
        PIN_ALIGN_DEFAULT_ROI_WIDTH=$(( 325 ))
        PIN_ALIGN_DEFAULT_ROI_HEIGHT=$(( 400 ))
        PIN_ALIGN_DEFAULT_ROI_WIDTH_OFFSET=$(( 375 ))
        PIN_ALIGN_DEFAULT_ROI_HEIGHT_OFFSET=$(( 312 ))
        PIN_ALIGN_DEFAULT_IMAGE_WIDTH_CENTER=$(( 510 ))
        PIN_ALIGN_DEFAULT_IMAGE_HEIGHT_CENTER=$((445 ))
        #                         width x height
        #                                 + horizontal offset 
        #                                   + vertical offset 
        #          (offsets origin is top left corner) 
        #          Note: vertical offset must be the same for all.  
        PIN_ALIGN_PIN_TIP_WINDOW="266x400+375+295"
        PIN_ALIGN_BASE_WINDOW="50x400+650+295"
        PIN_ALIGN_SUB_BASE_WINDOW="80x400+765+295"

all_pin.sh
        If not in production environment takes no arguments.  Defines 
        PIN_ALIGN_ROOT as the directory from  which is has been run 
        and then runs pin_align.sh on the sample images in the kit.

        If in production enviroment, takes two arguments, the 0 and
        90 degree jpeg images
     

pin_align.sh image_0 image_90 image_out image_base_out image_sub_base_out [tilt_limit]
        needs PIN_AIGN_ROOT to have been defined

        compare 0 and 90 degree images
        writing the resulting pin tip image to image_out
        writing the resulting pin base image to image_base_out
        writing the resulting pin base cap image to image_sub_base_out
        assuming  1280x1024 images
        imagemagick convert called as convert
        imagemagick compare called as compare
        assuming a center at 515 460
        assuming 325x400+375+312 ROI
   
        tilt_limit is a limit on the image height in pixels
        default 50 
        nooutput = 1; if CAP TILTED or PIN MISSING
        export PIN_ALIGN_Y_UP=1; if Y motor axis is up
        export PIN_ALIGN_Z_UP=1; if Z motor axis is up

pin_align_prep.sh image_in image_out [base_image_out [sub_base_image_out]]
        prepare a pin alignment image, image_in, for
        comparison between omega=0 and 90 degree images
        writing a 325x400+375+312 sub-image to image_out
        and optionally a 100x400+650+312 sub-image to base_image_out
        and optionally a 100x400+750+312 sub-image to sub_base_image_out
        assuming a 1280x1024 image and imgagemagick convert
        in the PATH

pin_align_split_info.sh  info_string
        convert an ImgMagick info string in $1 to a set of variable
        assignments in stdout
            info_file_name=
            info_file_type=
            info_active_image_width=
            info_active_image_height=
            info_raw_image_width_offset=
            info_raw_image_height_offset=

the files  	
 	mitegenPins_omega_0_centered_001.jpg	mitegenPins_omega_90_centered_001.jpg 	
	omega_0_001.jpg	omega_0_002.jpg omega_0_003.jpg omega_0_004.jpg omega_0_006.jpg 
	omega_0_007.jpg omega_0_008.jpg omega_0_009.jpg omega_0_010.jpg omega_0_011.jpg
	omega_90_001.jpg omega_90_002.jpg omega_90_003.jpg omega_90_004.jpg
	omega_90_005.jpg omega_90_006.jpg omega_90_007.jpg omega_90_008.jpg
	omega_90_009.jpg omega_90_010.jpgmega_90_011.jpg

        are the test cases for pin_align, producing what is in all_pin.out
