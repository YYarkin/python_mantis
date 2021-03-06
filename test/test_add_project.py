from random import choice
from model.project import Project
from generator import random as generator


def test_add_project(app, config):
    statuses = ['development', 'release', 'stable', 'obsolete']
    status_view = ['public', 'private']
    project = Project(name=generator.random_string("bobr", 5), status=choice(statuses),
                      status_view=choice(status_view), description=generator.random_string("description", 25))

    old_projects = app.soap.get_all_projects_accessible_to_user(
        config['webadmin']['login'], config['webadmin']['password'])
    app.project.create(project)
    new_projects = app.soap.get_all_projects_accessible_to_user(
        config['webadmin']['login'], config['webadmin']['password'])
    assert len(old_projects) + 1 == len(new_projects)
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
