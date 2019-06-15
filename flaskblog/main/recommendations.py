from flaskblog import db
from flaskblog.models import User, PerfumeInfo, Scents
from flaskblog.users.forms import QuestionnaireForm
from collections import Counter


class MyMapper():
    mgroups = [('1', 'Przyprawowa'),
     ('2', 'Kwiatowa'), ('3', 'Drzewna'), ('4', 'Deserowa'),
     ('5', 'Ziołowa'), ('6', 'Animalna'), ('7', 'Orientalna'),
     ('8', 'Owocowa'), ('9', 'Cytrusowa'), ('10', 'Morska')]

    mtypes = [('1', 'Świeży'),
        ('2', 'Słodki'), ('3', 'Ciepły'), ('4', 'Gorzki'),
        ('5', 'Wytrawny'), ('6', 'Zimny')]


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


def get_perfumes_by_criteria(list_of_scents, type_name, gender):
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
          PerfumeInfo.base.like((str(each_scent)+',%')))).filter(
              PerfumeInfo.group.like(type_name)).filter(
                  PerfumeInfo.gender.like(gender)).all()
        print(query)
        if query != []:
            #print('======= kazdy z query ========')
            for each_match in query:
                #print(each_match)
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
    chosen_group = key[1:-1]
    chosen_type = key[-1:]

    group_name = match_group_name(chosen_group)
    type_name = match_type_name(chosen_type)


    list_of_scents = get_scents_id(group_name)

    matching_results = get_perfumes_by_criteria(
                   list_of_scents, type_name, chosen_gender)

    perfume_occurences = count_occurence(matching_results)
    sorted_occurences = sorted(perfume_occurences.items(), key=lambda kv: kv[1])

    list_of_ids = get_list_of_ids(sorted_occurences)
    list_of_ids.reverse()
    final_list = get_list_of_perfumes(list_of_ids)

    return final_list


def make_one_string(list_of_scents):
    scent_proper_list = []
    for scent in list_of_scents:
        if type(scent) == str:
            tmp = scent.split(',')
            for t in tmp:
                scent_proper_list.append(int(t))
        else:
            scent_proper_list.append(scent)
    return scent_proper_list


def get_max_key_val(dict_):
    """Przyjmuje POJEDYNCZY histogram jako parametr i zwraca krotke z kluczem i
    najwieksza wartoscia jaka sie w nim znajduje.
    """

    max_key_val = [None, 0]
    for key, val in dict_.items():
        if val > max_key_val[1]:
            max_key_val[0] = key
            max_key_val[1] = val
    return max_key_val


def get_most_popular_scents(histogram, min_freq, max_freq):
    """Przyjmuje histogram jako parametr i:
    min_freq : Dolny zakres czestotliwosci wystapien zapachu
    max_freq : Gorny zakres czestotliwosci wystapien zapachu
    Gdzie te wartosci powinny byc w zakresie od 0 do 1. Czyli np.
    Zakres od 80% do 100% czestotliwosci to min_freq=0.8, max_freq=1.0

    Jezeli najwieksza wartosc w histogramie to 10 to dolny zakres bedzie rowny
    8 a gorny 10, wtedy wszystkie zapachy spelniajace zaleznosc:
    8 <= czestotliwosc wystepowania zapachu <= 10 zostana zwrocone jako lista.
    (Po nazwach)
    """

    max_key_val = get_max_key_val(dict_=histogram)
    min_real_val = min_freq * max_key_val[1]
    max_real_val = max_freq * max_key_val[1]
    choosen_scents = list()
    for scent, freq in histogram.items():
        if min_real_val <= freq <= max_real_val:
            choosen_scents.append(scent)
    return choosen_scents


def get_scents_sets(top_scents, heart_scents, base_scents):
    """Przyjmuje liste zapachow dla glowy, serca oraz bazy i robi wszystkie
    mozliwe permutacje bez powtorzen i zwraca zbior krotek ID-kow zapachow, czy
    tam nazw, zalezy co podasz
    """

    # !!! To zakomentowane robi dokladnie to samo co to nizej !!!
    # !!!         Wybierz to ktore bardziej rozumiesz         !!!

    # temp_list = list()
    # for base_scent in base_scents:
    #     scents = (base_scent, )
    #     for top_scent in top_scents:
    #         scents += (top_scent, )
    #         for heart_scent in heart_scents:
    #             scents += (heart_scent, )
    #             temp_list.append(scents)
    #             scents = scents[:-1]
    #         scents = scents[:-1]
    # return set(temp_list)

    double_combinations = list()
    for top_scent in top_scents:
        scent = (top_scent, )
        for heart_scent in heart_scents:
            scent += (heart_scent, )
            double_combinations.append(scent)
            scent = scent[:-1]

    triple_combinations = list()
    for double_scent in double_combinations:
        scent = double_scent
        for base_scent in base_scents:
            scent += (base_scent, )
            triple_combinations.append(scent)
            scent = scent[:-1]

    return set(triple_combinations)


def get_scents_combinations_for_user(user_histogram, min_freq, max_freq):
    """Tutaj masz jak to możesz wykorzystac. Ja po prostu oczekuje ze podasz mi
    liste krotek reprezentujaca rekordy ktore Ci zwrocil select. Zwracam Ci
    liste kombinacji zapachow.
    """

    most_popular_user_base = get_most_popular_scents(
        histogram=user_histogram["BASE"], min_freq=min_freq, max_freq=max_freq
    )
    most_popular_user_top = get_most_popular_scents(
        histogram=user_histogram["TOP"], min_freq=min_freq, max_freq=max_freq
    )
    most_popular_user_heart = get_most_popular_scents(
        histogram=user_histogram["HEART"], min_freq=min_freq, max_freq=max_freq
    )

    scents_sets = get_scents_sets(
        top_scents=most_popular_user_top,
        heart_scents=most_popular_user_heart,
        base_scents=most_popular_user_base
    )

    print("User histograms")
    for k, v in user_histogram.items():
        print(k, v)
    # print("\nMost populart top scents")
    # print(most_popular_user_top)
    # print("\nMost populart HEART scents")
    # print(most_popular_user_heart)
    # print("\nMost populart BASE scents")
    # print(most_popular_user_base)
    # print("\nScents combinations (TOP, HEART, BASE)")
    # for item in scents_sets:
    #     print(item)

    return scents_sets


def UserRecommendation(p_ids):
    '''
    Gets list of perfume ids and returns list made of 3 lists,
    each containing best matching fragrances
    '''
    all_tops = []
    all_hearts = []
    all_bases = []
    for p_id in p_ids:
        query = PerfumeInfo.query.filter_by(id=p_id).first()
        all_tops.append(query.top)
        all_hearts.append(query.heart)
        all_bases.append(query.base)
    formatted_tops = make_one_string(all_tops)
    formatted_hearts = make_one_string(all_hearts)
    formatted_bases = make_one_string(all_bases)

    counted_tops = dict(Counter(formatted_tops))
    counted_hearts = dict(Counter(formatted_hearts))
    counted_bases = dict(Counter(formatted_bases))

    histograms = {
        "TOP": counted_tops,
        "HEART": counted_hearts,
        "BASE": counted_bases,
    }

    scents_combinations = get_scents_combinations_for_user(histograms, 0.9, 1)

    for combination in scents_combinations:
        query = PerfumeInfo.query.filter(
         ((PerfumeInfo.top.like('%,'+str(combination[0])+',%') |
          PerfumeInfo.top.like('%,'+str(combination[0])) |
          PerfumeInfo.top.like((str(combination[0])+',%'))) &
          (PerfumeInfo.heart.like('%,'+str(combination[1])+',%') |
          PerfumeInfo.heart.like('%,'+str(combination[1])) |
          PerfumeInfo.heart.like((str(combination[1])+',%'))) &
          (PerfumeInfo.base.like('%,'+str(combination[2])+',%') |
          PerfumeInfo.base.like('%,'+str(combination[2])) |
          PerfumeInfo.base.like((str(combination[2])+',%'))))).all()
        #print(query)
        tmp = []
        for q in query:
            #print(q)
            tmp.append(q)
    print('TEMPE\n\n')
    #print(type(tmp))

    print(len(scents_combinations))
    #print(counted_hearts)
    #print(counted_bases)

    return tmp
