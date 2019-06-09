from flaskblog import db
from flaskblog.models import User, PerfumeInfo, Scents
from flaskblog.users.forms import QuestionnaireForm


class MyMapper():
    mgroups = [('1', 'Przyprawowa'),
     ('2', 'Kwiatowa'), ('3', 'Drzewna'), ('4', 'Deserowa'),
     ('5', 'Ziołowa'), ('6', 'Animalna'), ('7', 'Orientalna'),
     ('8', 'Owocowa'), ('9', 'Cytrusowa'), ('10', 'Morskia')]
    


def QuestionnaireRecommendation(key):
    q_gender = key[0]
    q_scent = key[1]
    tmp = QuestionnaireForm.groups
    print(tmp)
    tmp_groups = MyMapper.mgroups[int(q_scent)-1][1]
    print(tmp_groups)
    #zwraca mi obiekt klasy z Scents
    id_zapachow_z_bazy = Scents.query.filter_by(group=str(tmp_groups)).all()
    print(type(id_zapachow_z_bazy))
    #wywołuje metode get_info zeby dostac krotki
    
    q_group = key[2]
    db_scent = Scents.query.filter_by(group=str(q_scent)).all() #wyciągam id konkretnego zapachu z bazy
    print(db_scent)
    gender_results = PerfumeInfo.query.filter_by(gender=str(q_gender)).all()
    scent_results = PerfumeInfo.query.filter(PerfumeInfo.top.like('%'+str(q_scent)+'%')).all()
    glista = list(elem.get_info() for elem in gender_results)
    #lista = eval(gender_results)
    #print(lista)
    print(scent_results)

    return gender_results
