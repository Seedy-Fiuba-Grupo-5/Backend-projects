from prod import db


class ProjectDBModel(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(128),
                     nullable=False)
    description = db.Column(db.String(128),
                            nullable=False)
    hashtags = db.Column(db.String(1000),
                         nullable=False)
    type = db.Column(db.String(128),
                     nullable=False)
    goal = db.Column(db.Integer,
                     nullable=False)
    endDate = db.Column(db.String(128),
                        nullable=False)
    location = db.Column(db.String(128),
                         nullable=False)
    image = db.Column(db.Text,
                      nullable=False,
                      default='')

    def __init__(self,
                 name, description, hashtags, type, goal,
                 endDate, location, image):
        self.name = name
        self.description = description
        self.hashtags = hashtags
        self.type = type
        self.goal = goal
        self.endDate = endDate
        self.location = location
        self.image = image

    @classmethod
    def create(cls,
               name, description, hashtags, type, goal,
               endDate, location, image):
        project_model = ProjectDBModel(name, description, hashtags, type,
                                       goal, endDate, location, image)
        db.session.add(project_model)
        db.session.commit()
        db.session.refresh(project_model)
        return project_model

    def update(self,
               name, description, hashtags, type, goal,
               endDate, location, image):
        self.__init__(name, description, hashtags, type, goal,
                      endDate, location, image)
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'hashtags': self.hashtags,
            'type': self.type,
            'goal': self.goal,
            'endDate': self.endDate,
            'location': self.location,
            'image': self.image
        }