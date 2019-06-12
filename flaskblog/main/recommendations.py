from flaskblog import db
from flaskblog.models import User, PerfumeInfo, Scents
from flaskblog.users.forms import QuestionnaireForm
from collections import Counter


class MyMapper():
    mgroups = [('1', 'Przyprawowa'),
     ('2', 'Kwiatowa'), ('3', 'Drzewna'), ('4', 'Deserowa'),
     ('5', 'Ziołowa'), ('6', 'Animalna'), ('7', 'Orientalna'),
     ('8', 'Owocowa'), ('9', 'Cytrusowa'), ('10', 'Morskia')]

    mtypes = [('1', 'Świeży'),
        ('2', 'Słodki'), ('3', 'Ciepły'), ('4', 'Gorzki'),
        ('5', 'Wytrawny'), ('6', 'Zimny')]


def get_by_gender(gender_key):
    '''
    Zwraca rekordy z bazy w formie listy trzyelementowych krotek* NOPE
    to są obiekty uformowane w ten sposób
    [(1,Perfume,Brand),(2,Perf,Br)] etc
    DOD: zwraca listę ID pasujących perfum
    '''
    list_of_tuples = PerfumeInfo.query.filter_by(gender=gender_key).all()
    result_ids = []
    for p_id in list_of_tuples:
        result_ids.append(p_id.id)
    print(result_ids)
    return result_ids


def match_group_name(group_key):
    '''
    Dobieram odpowiednią nazwę do id nazwy w ankiecie, na podstawie MyMapper
    '''
    group_name = MyMapper.mgroups[int(group_key)-1][1]
    print("group name below")
    print(group_name)

    return group_name


def match_type_name(type_key):
    type_name = MyMapper.mtypes[int(type_key)-1][1]
    print('type name below')
    print(type_name)

    return type_name


def get_scents_id(scent_name):
    '''
    Dobranie odpowiedniego id grupy zapachowej z bazy z tabeli Scents
    Zwracam listę idków zapachów pasujących do danej grupy
    '''
    scent_query = Scents.query.filter_by(group=scent_name).all()
    scents_id = []
    for scent in scent_query:
        scents_id.append(scent.id)
    return scents_id


def get_perfumes_by_scents(list_of_scents, type_name, gender):
    '''
    Zaciąga listę z id zapachów, które chcemy mieć w perfumach
    DOD: zwraca listę z id perfum z pożądanymi zapachami

    1) biorę id i sprawdzam czy występuje w ktorejkolwiek z nut
        jeśli tak -> dodaję dany rekord do listy wyników
    2) w prypadku gdy kilka zapachów z listy występuje to w liscie wynikowej
        rekord z danymi perfumami będzie powielony - im bardziej tym
        więcej zapachów pokrywa
    '''
    matching_results = []
    for each_scent in list_of_scents:
        query = PerfumeInfo.query.filter(
         (PerfumeInfo.top.like('%,'+str(each_scent)+',%') |
          PerfumeInfo.top.like('%,'+str(each_scent)) |
          PerfumeInfo.heart.like('%,'+str(each_scent)+',%') |
          PerfumeInfo.top.like((str(each_scent)+',%')) |
          PerfumeInfo.heart.like('%,'+str(each_scent)) |
          PerfumeInfo.heart.like((str(each_scent)+',%')) |
          PerfumeInfo.base.like('%,'+str(each_scent)+',%') |
          PerfumeInfo.base.like('%,'+str(each_scent)) |
          PerfumeInfo.base.like((str(each_scent)+',%')))).filter(PerfumeInfo.group.like(type_name)).filter(PerfumeInfo.gender.like(gender)).all()
        print(query)
        if query != []:
            print('======= kazdy z query ========')
            for each_match in query:
                print(each_match)
                matching_results.append(each_match.id)

    return matching_results


def count_occurence(list_of_id_occurences):
    '''
    Przyjmuję listę wystąpień perfum podczasp przeszukiwania bazy
    im więcej razy wystąpił dany id perfum tym więcej zapachów pokryły

    Zwraca dict?(ilosc_wyst_id, id_p)
    '''
    return dict(Counter(list_of_id_occurences)) 


def get_list_of_ids(sorted_list):
    list_of_ids = []
    for elem in sorted_list:
        list_of_ids.append(elem[0])

    return list_of_ids


def get_list_of_perfumes(list_of_ids):
    perfumes = []
    for p_id in list_of_ids:
        query = PerfumeInfo.query.filter_by(id=p_id).all()
        print('print query i jej type')
        print(query[0])
        print(type(query[0]))
        perfumes.append(query[0])
    
    return perfumes


def QuestionnaireRecommendation(key):
    '''
    Na podstawie wygenerowanego klucza rozbijam jego poszczególne elementy na
    zmienne, aby łatwiej było wyciągnąć informacje z bazy
    '''
    chosen_gender = key[0]
    chosen_group = key[1]
    chosen_type = key[2]

    # lista krotek, zawierająca wszystkie rekordy odpowiadające danej płci
    records_matching_by_gender = get_by_gender(chosen_gender)

    print(records_matching_by_gender)
    #group_name_results = Scents.query.filter_by(group=str(group_name)).all()
    #print(type(group_name_results))
    print("000000000000000000000000")
    list_of_scents = get_scents_id(match_group_name(chosen_group))
    print(list_of_scents)

    type_name = match_type_name(chosen_type)

    matching_res = get_perfumes_by_scents(list_of_scents, type_name, chosen_gender)
    print('~~~~~~~~~~~~~~~~wszystkie id~~~~~~~~~~~~~~~~~~')
    print(matching_res)
    print('############ COUNTER ################')
    cnt = count_occurence(matching_res)
    sorted_asc = sorted(cnt.items(), key=lambda kv: kv[1])
    print(sorted_asc)

    list_of_ids = get_list_of_ids(sorted_asc)
    list_of_ids.reverse()
    print('@@@@@@@@@@@ AJDIKI @@@@@@@')
    print(list_of_ids)

    final_list = get_list_of_perfumes(list_of_ids)

    return final_list
