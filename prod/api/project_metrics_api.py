from datetime import datetime
from flask_restx import Namespace, Resource, fields
from flask_restx import Model, fields

from prod.db_models.project_db_model import ProjectDBModel
from prod.schemas.project_options import ProjectTypeEnum

ns = Namespace(
    'projects/metrics',
    description='All projects metrics'
)

@ns.route('')
class ProjectsListResource(Resource):
    metrics_representation = Model('ProjectMetrics', {
        'most_popular_type': fields.Integer(description='Most popular type of project'),
        'avg_duration': fields.Integer(description='Average project duration'),
        'avg_goal': fields.Integer(description='Average project goal')
    })
    code_20x_swg = ns.model(metrics_representation.name,
                            metrics_representation)

    @ns.response(200, 'Success', fields.List(fields.Nested(code_20x_swg)))
    def get(self):
        response_body = {}
        response_body["most_popular_type"] = self.get_most_popular_type()
        response_body["avg_duration"] = self.calculate_avg_duration()
        response_body["avg_goal"] = self.calculate_avg_goal()
        return response_body, 200

    def get_most_popular_type(self):
        max = 0
        current_type = "None"
        for item in ProjectTypeEnum:
            total = len([project.id for project in ProjectDBModel.query.filter_by(type=item)])
            if total > max:
                max = total
                current_type = item.value
        return current_type

    def calculate_avg_duration(self):
        total = len([project.id for project in ProjectDBModel.query.all()])
        if total <= 0:
            return 0
        durations_sum = 0
        for project in ProjectDBModel.query.all():
            diff = datetime.strptime(project.endDate, '%d/%m/%Y') - project.creation_date
            durations_sum += diff.days/30
        return durations_sum/total

    def calculate_avg_goal(self):
        total = len([project.id for project in ProjectDBModel.query.all()])
        if total <= 0:
            return 0
        goal_sum = 0
        for project in ProjectDBModel.query.all():
            goal_sum += project.goal
        return goal_sum / total
