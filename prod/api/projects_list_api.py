from flask import request
from flask_restx import Namespace, Resource, fields
from prod.db_models.project_db_model import ProjectDBModel
from prod.schemas.project_required_body import project_required_body
from prod.schemas.project_representation import project_representation
from prod.schemas.missing_values import missing_values, MISSING_VALUES_ERROR
from prod.schemas.constants import PROJECT_FIELDS

ns = Namespace(
    'projects',
    description='All projects related operations'
)


@ns.route('')
class ProjectsListResource(Resource):
    body_swg = ns.model(project_required_body.name, project_required_body)
    code_20x_swg = ns.model(project_representation.name,
                            project_representation)
    code_400_swg = ns.model(missing_values.name, missing_values)

    @ns.response(200, 'Success', fields.List(fields.Nested(code_20x_swg)))
    def get(self):
        response_object =\
            [project.serialize() for project in ProjectDBModel.query.all()]
        return response_object, 200

    @ns.expect(body_swg)
    @ns.response(201, 'Success', code_20x_swg)
    @ns.response(400, MISSING_VALUES_ERROR, code_400_swg)
    def post(self):
        json = request.get_json()
        if not self.check_values(json, PROJECT_FIELDS):
            ns.abort(400, status=MISSING_VALUES_ERROR)
        project_model = ProjectDBModel.create(
            name=json['name'],
            description=json['description'],
            hashtags=json['hashtags'],
            type=json['type'],
            goal=json['goal'],
            endDate=json['endDate'],
            location=json['location'],
            image=json['image']
        )
        response_object = project_model.serialize()
        return response_object, 201

    @staticmethod
    def check_values(json, list):
        for value in list:
            if value not in json:
                return False
        return True