'''
This is adapted from http://obswww.unige.ch/%7Etewes/alipy/tutorial.html
'''

import alipy
import glob

#images_to_align = sorted(glob.glob("images/*.fits"))
#ref_image = "ref.fits"


def identify_transform(ref_image, images_to_align,
                       rad= 5, nb=500,
                       verbose=False, visual=False):
    identifications = alipy.ident.run(ref_image, images_to_align,
                                      r=rad, n=nb, visu=visual)
    # That's it !
    # Put visu=True to get visualizations in form of png files
    #   (nice but much slower)
    # On multi-extension data, you will want to specify the hdu (see API doc).

    if verbose:
        # The output is a list of Identification objects,
        # which contain the transforms :
        for id in identifications:  # list of the same length as images_to_align.
            if id.ok is True:  # i.e., if it worked
                print("%20s : %20s, flux ratio %.2f" % (id.ukn.name,
                                                        id.trans,
                                                        id.medfluxratio))
                # id.trans is a alipy.star.SimpleTransform object.
                #    Instead of printing it out as a string,
                # you can directly access its parameters :
                # print id.trans.v # the raw data,
                #                  # [r*cos(theta)  r*sin(theta)
                #                  #  r*shift_x  r*shift_y]
                # print id.trans.matrixform()
                # print id.trans.inverse() # this returns a
                #                          # new SimpleTransform object

            else:
                print( "%20s : no transformation found !" % (id.ukn.name))

    return identifications



def align_images(ref_image, identifications, iraf=True, outdir='alipy_out'):
    # Minimal example of how to align images :
    outputshape = alipy.align.shape(ref_image)
    # This is simply a tuple (width, height)...
    # you could specify any other shape.
    for id in identifications:
            if id.ok is True:
                if iraf:
                    # Variant 2, using geomap/gregister,
                    # correcting also for distortions :
                    alipy.align.irafalign(id.ukn.filepath, id.uknmatchstars,
                                          id.refmatchstars, shape=outputshape,
                                          makepng=False, outdir=outdir)
                    # id.uknmatchstars and id.refmatchstars are simply lists of
                    # corresponding Star objects.
                else:
                    # Variant 1, using only scipy and the simple affine transorm :
                    alipy.align.affineremap(id.ukn.filepath, id.trans,
                                            shape=outputshape, makepng=True,
                                            outdir=outdir)
                # By default, the aligned images are written into a directory
                # "alipy_out".
