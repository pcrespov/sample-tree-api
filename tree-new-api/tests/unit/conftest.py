# pylint:disable=unused-variable
# pylint:disable=unused-argument
# pylint:disable=redefined-outer-name

import sys
from pathlib import Path

import pytest

from servicelib.utils import search_osparc_repo_dir

import simcore_service_tree_new_api


current_dir = Path(sys.argv[0] if __name__ == "__main__" else __file__).resolve().parent


@pytest.fixture(scope='session')
def project_slug_dir():
    folder = current_dir.parent.parent
    assert folder.exists()
    assert any( folder.glob("src/simcore_service_tree_new_api") )
    return folder

@pytest.fixture(scope='session')
def package_dir():
    dirpath = Path(simcore_service_tree_new_api.__file__).resolve().parent
    assert dirpath.exists()
    return dirpath


@pytest.fixture(scope='session')
def osparc_simcore_root_dir():
    root_dir = search_osparc_repo_dir(current_dir) or here.parent.parent / "_osparc-simcore-stub"
    assert root_dir and root_dir.exists(), "Did you renamed or moved the integration folder under tree-new-api??"
    assert any(root_dir.glob("services/tree-new-api")), "%s not look like rootdir" % root_dir
    return root_dir


@pytest.fixture(scope='session')
def api_specs_dir(osparc_simcore_root_dir):
    specs_dir = osparc_simcore_root_dir/ "api" / "specs" / "tree-new-api"
    assert specs_dir.exists()
    return specs_dir