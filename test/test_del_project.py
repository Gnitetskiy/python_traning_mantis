import pytest
from generator.project import testdata
from model.project import ProjectData
import random

@pytest.mark.parametrize("project", testdata, ids=[repr(x) for x in testdata])
def test_add_project(app,project):
    username = app.username
    password = app.password
    app.session.ensure_login(username, password)
    old_projects =app.project.get_project_list()
    if len(old_projects ) == 0:
        app.project.open_manage_proj_create_page()
        app.project.fill_project_data(project)
        app.project.add_project()
    project=random.choice(old_projects)
    app.project.delete_project_by_id(project.id)
    new_projects = app.project.get_project_list()
    project_list_soap = app.soap.projects_get_user_accessible(username, password)
    assert len(old_projects) - 1 == len(new_projects)
    old_projects.remove(project)
    assert sorted(old_projects, key=ProjectData.id_or_max) == sorted(new_projects, key=ProjectData.id_or_max)
    assert sorted(new_projects, key=ProjectData.id_or_max) == sorted(project_list_soap, key=ProjectData.id_or_max)
