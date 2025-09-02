from suds.client import Client
from model.project import ProjectData
from suds import WebFault
import re


def clear(s):
    return re.sub(" ", "", s)

class SoapHelper:

    def __init__(self, app):
        self.app = app


    def can_login(self,username, password):
        client = Client("http://localhost:8080/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username,password)
            return True
        except WebFault:
            return False

    def projects_get_user_accessible (self,username, password):
        client = Client("http://localhost:8080/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            soap_projects = client.service.mc_projects_get_user_accessible(username, password)
            project_list = []
            for p in soap_projects:
                project_data = ProjectData(id=str(p.id),  name=clear(str(p.name)),  description=clear(str(p.description)))
                project_list.append(project_data)
            return project_list
        except WebFault:
            return False

