from suds.client import Client
from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def get_all_projects_accessible_to_user(self, username, password):
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        list_of_projects = []
        for row in client.service.mc_projects_get_user_accessible(username, password):
            list_of_projects.append(Project(name=row.name, id=row.id))
        return list_of_projects
