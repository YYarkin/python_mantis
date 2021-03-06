import random

from model.project import Project
from generator import random as generator


def test_delete_random_project(app, config):
    if len(app.project.get_project_list()) == 0:
        app.project.create(Project(name=generator.random_string("bobr", 5)))

    old_projects = app.soap.get_all_projects_accessible_to_user(
        config['webadmin']['login'], config['webadmin']['password'])
    project = random.choice(old_projects)
    app.project.delete_project_by_id(project.id)
    new_projects = app.soap.get_all_projects_accessible_to_user(
        config['webadmin']['login'], config['webadmin']['password'])
    assert len(old_projects) - 1 == len(new_projects)
    old_projects.remove(project)
    assert sorted(new_projects, key=Project.id_or_max) == sorted(old_projects, key=Project.id_or_max)
