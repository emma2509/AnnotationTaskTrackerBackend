from pybuilder.core import use_plugin, init, task
import os

# These are the plugins we want to use in our project.
# Projects provide tasks which are blocks of logic executed by PyBuilder.

use_plugin("python.core")
# this plugin allows installing project dependencies with pip
use_plugin("python.install_dependencies")
# pytest plug in
use_plugin("pypi:pybuilder_pytest")


# The project name
name = "annotationTaskTrackerBackend"

# What PyBuilder should run when no tasks are given.
# Calling "pyb" amounts to calling "pyb publish" here.
# We could run several tasks by assigning a list to `default_task`.
default_task = ["install_dependencies", "run_ruff", "publish"]


@task
def run_ruff():
    if os.system("ruff check") != 0:
        raise Exception("ruff check failed")
    if os.system("ruff format --check") != 0:
        raise Exception("ruff format failed")


# This is an initializer, a block of logic that runs before the project is built.
@init
def initialize(project):
    project.depends_on_requirements("requirements.txt")
    project.set_property("dir_source_main_python", "src")
    project.set_property("dir_source_pytest_python", "test/modules")
    project.get_property("pytest_extra_args").append("-x")
