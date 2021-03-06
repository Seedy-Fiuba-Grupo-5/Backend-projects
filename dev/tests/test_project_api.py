import json
from prod.db_models.project_db_model import ProjectDBModel
from dev.aux_test import recreate_db


def test_db_with_only_project_id_1_name_Project_X_GET_id_1_should_return_just_that(test_app, test_database):
    session = recreate_db(test_database)
    session.add(ProjectDBModel(name='Project X', description='description', hashtags='#prueba',
                               type='art', goal=1000, endDate='12/02/2021', location='Buenos Aires',
                               image='www.an_image_url.com',
                               createdOn='12/02/2021', path='a', lat=50, lon=20.5))
    session.commit()
    client = test_app.test_client()
    response = client.get("/projects/1")
    assert response.status_code == 200
    project = json.loads(response.data.decode())
    assert project['name'] == 'Project X'
    assert project['image'] == 'www.an_image_url.com'


def test_patch_project_id_cambiar_todos_los_contenidos_del_proyecto(
        test_app,
        test_database):
    """
    Dada una base de datos.
    Y un proyecto registrado:
        'id': <id>,
        'name': 'a name',
        'description': 'a description',
        'hashtags': '#someHashtags,
        'type': 'Art',
        'goal': 111,
        'endDate': '2022/06/07',
        'location': 'a location',
        'image': 'www.an-image-url.com'
    Cuando patch 'projects/1'
    Con cuerpo:
        'id': <id>,
        'name': 'another name',
        'description': 'another description',
        'hashtags': '#otherHashtags,
        'type': 'Comics',
        'goal': 222,
        'endDate': '2023/07/08',
        'location': 'another location'
        'image': 'www.another-image-url.com'
    Entonces los datos del proyeto se actualizan
    """
    session = recreate_db(test_database)
    old_project = {'name': 'a name', 'description': 'a description', 'hashtags': '#someHashtags',
                   'type': 'Art', 'goal': 111, 'endDate': '2022/06/07', 'location': 'a location',
                   'image': 'www.an-image-url.com', 'path': 'a', 'lat': 50, "lon": 20.5}
    client = test_app.test_client()
    post_resp = client.post("/projects", json=old_project)
    post_data = json.loads(post_resp.data.decode())
    id_project = post_data['id']
    update_project = {'id': id_project, 'name': 'another name', 'description': 'another description',
                      'hashtags': '#otherHashtags', 'type': 'Comics', 'goal': 222,
                      'endDate': '2023/07/08', 'location': 'another location',
                      'image': 'www.another-image-url.com', 'path': 'a'}
    patch_resp = client.patch(
        "/projects/{}".format(id_project),
        json=update_project
    )
    assert patch_resp.status_code == 200
    patch_data = json.loads(patch_resp.data.decode())
    for field in update_project.keys():
        assert patch_data[field] == update_project[field]


def test_patch_project_id_con_body_vacio_no_cambia_nada_del_proyecto(
        test_app,
        test_database):
    """
    Dada una base de datos.
    Y un proyecto registrado:
        'id': <id>,
        'name': 'a name',
        'description': 'a description',
        'hashtags': '#someHashtags,
        'type': 'a type',
        'goal': 111,
        'endDate': '2022/06/07',
        'location': 'a location',
        'image': 'www.an-image-url.com'
    Cuando patch 'projects/1'
    Con cuerpo:
        'id': <id>
        'name': 'another name'
    Entonces solo se actualiza el nombre del proyecto
    """
    session = recreate_db(test_database)
    old_project = {'name': 'a name', 'description': 'a description', 'hashtags': '#someHashtags',
                   'type': 'Comics', 'goal': 111, 'endDate': '2022/06/07', 'location': 'a location',
                   'image': 'www.an-image-url.com', 'path': 'a', 'lat': 50, "lon": 20.5}
    client = test_app.test_client()
    post_resp = client.post("/projects", json=old_project)
    post_data = json.loads(post_resp.data.decode())
    id_project = post_data['id']
    update_project = {'id': id_project, 'name': 'another name'}
    patch_resp = client.patch(
        "/projects/{}".format(id_project),
        json=update_project
    )
    assert patch_resp.status_code == 200
    patch_data = json.loads(patch_resp.data.decode())
    assert patch_data['name'] == update_project['name']
    for field in old_project.keys():
        if field == 'name':
            continue
        assert patch_data[field] == old_project[field]


def test_delete_project_id_elimina_el_proyecto(
        test_app,
        test_database):
    """
    Dada una base de datos.
    Y un proyecto registrado:
        'id': <id>,
    Cuando DELETE 'projects/<id>'
    Entonces obtengo status code 204
    Y el proyecto es eliminado
    """
    session = recreate_db(test_database)
    client = test_app.test_client()
    project = {'name': 'a name', 'description': 'a description', 'hashtags': '#someHashtags',
               'type': 'Comics', 'goal': 111, 'endDate': '2022/06/07', 'location': 'a location',
               'image': 'an image', 'lat': 50, "lon": 20.5, 'path': '/img'}

    post_resp = client.post("/projects", json=project)
    post_data = json.loads(post_resp.data.decode())
    id_project = post_data['id']

    with test_app.test_request_context():
        delete_resp = client.delete("/projects/{}".format(id_project))
        assert delete_resp.status_code == 204

    get_resp = client.get("/projects/{}".format(id_project))
    assert get_resp.status_code == 404


def test_delete_project_id_no_elimina_el_proyecto(
        test_app,
        test_database):
    """
    Dada una base de datos vacia.
    Cuando DELETE 'projects/<id>'
    Entonces obtengo status code 404
    Con cuerpo:
        "status": 'The project requested could not be found'
    """
    session = recreate_db(test_database)
    client = test_app.test_client()

    delete_resp = client.delete("/projects/111")
    assert delete_resp.status_code == 404
    delete_data = json.loads(delete_resp.data.decode())
    assert delete_data['status'] == 'The project requested could not be found'
