import os
import glob
import pytest
import sys
import ntpath

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/testing_modules/'))

from test_msh import mesh_file_test
from test_geo import geo_files_test

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../plugins/mesh_netcdf/'))

from modular_meshing import Modular_meshing


pwd = os.path.dirname(os.path.realpath(__file__))
test = pwd+"/output"
data = pwd+"/support"


def start() :

	if not os.path.exists(test +"/annulus_LY"):
	    os.makedirs(test +"/annulus_LY")

	Modular_meshing("--line LY -g "+test+"/annulus_LY/test_annulus_LY.geo "+data+"/annulus.shp --mesh --mval 10")
	Modular_meshing("--line LY -g "+test+"/annulus_LY/test_annulus_LY_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump.nc")
	Modular_meshing("--line LY -g "+test+"/annulus_LY/test_annulus_LY_medium_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump_medium.nc")
	Modular_meshing("--line LY -g "+test+"/annulus_LY/test_annulus_LY_coarse_metric.geo "+data+"/annulus.shp --mesh -m "+test+"/gaussian_bump_coarse.nc")

	print "......................................................"
	print '\033[1m' + " \nTesting: annulus, Bsplines = False Compounds = True\n " + '\033[0m'

start()

# used too pass arguments to the test function
def pytest_generate_tests(metafunc):
    # called once per each test function
    for funcargs in metafunc.cls.params[metafunc.function.__name__]:
        # schedule a new test function run with applied **funcargs
        metafunc.addcall(funcargs=funcargs)


class TestClass:
    """ Runs various tests on files """

    #parameters to the test function
    params = {

    	'test_annulus_ly_geo' : [dict(curr_file=x) for x in glob.glob(pwd +"/output/annulus_LY/*.geo")],
        'test_annulus_ly_msh': [dict(curr_file=x) for x in glob.glob(pwd +"/output/annulus_LY/*.msh")],
    }


    def test_annulus_ly_geo(self, curr_file):

		assert geo_files_test(curr_file),"%s does not match the model answer" % (ntpath.basename(a).rstrip())



    # Tests whether nodes of the file being are similar to the nodes in the
    # model answer. Throws an AssertionError if the files don't match
    def test_annulus_ly_msh(self, curr_file):

        assert mesh_file_test(curr_file),"%s does not match the model answer" % (ntpath.basename(curr_file).rstrip())
