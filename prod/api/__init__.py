from flask import Blueprint
from flask_restx import Api
from .project_api import ns as project_ns
from .projects_list_api import ns as projects_list_ns
from .project_metrics_api import ns as metrics_ns
from .commentary_api import ns as commentary_ns
from .one_project_favorites_api import ns as favorites_ns
from .project_rate_api import ns as rate_ns

# Base API

api_base_bp = Blueprint('api_base', __name__)
api_base = Api(
    api_base_bp,
    title='Backend Projects: API base',
    version=1.0,
    description='Backend projects service operations'
)

api_base.add_namespace(project_ns)
api_base.add_namespace(projects_list_ns)
api_base.add_namespace(metrics_ns)
api_base.add_namespace(commentary_ns)
api_base.add_namespace(favorites_ns)
api_base.add_namespace(rate_ns)

# API v1
V1_PREFIX = '/v1/'
api_v1_bp = Blueprint('api_v1', __name__, url_prefix=V1_PREFIX)
api_v1 = Api(
    api_v1_bp,
    title='Backend Projects: API v1',
    version=1.0,
    description='Backend projects service operations'
)

api_v1.add_namespace(project_ns)
api_v1.add_namespace(projects_list_ns)
api_v1.add_namespace(metrics_ns)
api_v1.add_namespace(commentary_ns)
