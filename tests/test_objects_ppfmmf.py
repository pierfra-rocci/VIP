"""Test for the PostProc object dedicated to FMMF."""

__author__ = "Thomas Bédrine"

import copy

import numpy as np

from .helpers import fixture
from vip_hci.invprob import fmmf
from vip_hci.objects import FMMFBuilder


@fixture(scope="module")
def setup_dataset(example_dataset_adi):
    betapic = copy.copy(example_dataset_adi)

    return betapic


def test_fmmf_object(setup_dataset):
    """
    Compare frames obtained through procedural and object versions of FMMF.

    Generate a frame and a snr_map with both ``vip_hci.invprob.fmmf`` and
    ``vip_hci.objects.ppfmmf`` and ensure they match.

    """
    betapic = setup_dataset
    cube = betapic.cube
    angles = betapic.angles
    fwhm = betapic.fwhm
    psf = betapic.psf

    imlib_rot = "vip-fft"
    interpolation = None

    fr_fmmf, snr_fmmf = fmmf(
        cube=cube,
        angle_list=angles,
        fwhm=fwhm,
        psf=psf,
        model="LOCI",
        var="FR",
        nproc=None,
        min_r=int(2 * fwhm),
        max_r=int(6 * fwhm),
        param={"ncomp": 10, "tolerance": 0.005, "delta_rot": 0.5},
        crop=5,
        imlib=imlib_rot,
        interpolation=interpolation,
    )

    fmmf_obj = FMMFBuilder(
        dataset=betapic,
        model="LOCI",
        var="FR",
        nproc=None,
        min_r=int(2 * fwhm),
        max_r=int(6 * fwhm),
        param={"ncomp": 10, "tolerance": 0.005, "delta_rot": 0.5},
        crop=5,
        imlib=imlib_rot,
        interpolation=interpolation,
        verbose=False,
    ).build()

    fmmf_obj.run()

    assert np.allclose(np.abs(fr_fmmf), np.abs(fmmf_obj.frame_final), atol=1.0e-2)
    assert np.allclose(np.abs(snr_fmmf), np.abs(fmmf_obj.snr_map), atol=1.0e-2)
