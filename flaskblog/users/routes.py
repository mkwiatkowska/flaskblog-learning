from flask import (
    render_template, url_for, flash, redirect, request, Blueprint, abort)
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post, PerfumeInfo, Scents, UserPreferences
from flaskblog.users.forms import (
    RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm,
    ResetPasswordForm, QuestionnaireForm, AddToFavourites)
from flaskblog.users.utils import save_picture, send_reset_email
from flaskblog.main.recommendations import (
    QuestionnaireRecommendation as qr, UserRecommendation as us)
from flaskblog.main.utils import is_valid


users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
                        form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Ur account has been created! U can now log in!', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Registration', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                    user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                    url_for('main.home'))
        else:
            flash('couldnt log u in, sorry, check email and/or password',
                  'danger')
    return render_template('login.html', title='Login Page', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.img_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('ur account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.img_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('an email has been sent with instructions to reset ur password',
              'info')
        return redirect(url_for('users.login'))
    return render_template(
        'reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Ur token is invalid or has expired', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
                        form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'UUr password has been updated! U r now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template(
        'reset_token.html', title='Reset Password', form=form)


@users.route("/questionnaire", methods=['GET', 'POST'])
def fill_questionnaire():
    form = QuestionnaireForm()
    if form.validate_on_submit():
        gender = form.genders.data
        group = form.groups.data
        scent = form.scents.data
        key = str(gender+group+scent)
        return redirect(url_for('users.questionnaire_results', key=key))

    return render_template('questionnaire.html', title='Scents Questionnaire', form=form)


@users.route("/questionnaire/results/<string:key>", methods=['GET'])
def questionnaire_results(key):
    if is_valid(key):
        results = qr(key)
    else:
        abort(403)

    return render_template(
        'questionnaire_results.html', title='Ur Results', results=results)


def record_exists(user_id, perfume_id):
    query = UserPreferences.query.filter(
        (UserPreferences.user_id.like(user_id)) &
        (UserPreferences.perfume_id.like(perfume_id))).all()
    print(query)
    if query:
        return True
    else:
        return False

@users.route("/add_favourites", methods=['GET', 'POST'])
@login_required
def favourites():
    form = AddToFavourites()
    form.perfume.choices = [(str(p.id), str(p.name+' by '+p.brand)) for p in PerfumeInfo.query.order_by('name')]
    username = current_user.username
    user_id = (User.query.filter_by(username=username).first()).id
    choices = UserPreferences.query.filter(UserPreferences.user_id.like(user_id)).all()
    print('CZOJSES\n\n')
    print(choices)
    tmp_choices = get_perfume_names(choices)
    print('\n\n\n TU PACZ \n\n')
    print(tmp_choices)
    your_choices = []
    for tmp in tmp_choices:
        your_choices.append(str(tmp[0].name+' by '+tmp[0].brand))
    if form.validate_on_submit():
        perfume = form.perfume.data
        user_preference = UserPreferences(user_id=user_id, perfume_id=perfume)
        if not record_exists(user_id, perfume):
            db.session.add(user_preference)
            db.session.commit()
        else:
            flash('record already exists in database', 'danger')
        return redirect(url_for('users.favourites'))

    return render_template('add_favourite_perfumes.html', title='Favs', form=form, tmp_choices=tmp_choices)


def get_perfume_names(id_list):
    perfumes = []
    for p_id in id_list:
        print(p_id.perfume_id)
        query = PerfumeInfo.query.filter(PerfumeInfo.id.like(p_id.perfume_id)).all()
        perfumes.append(query)
    return perfumes


@users.route("/delete_preference/", methods=['POST'])
@login_required
def delete_preference():
    user = current_user.id
    query = UserPreferences.query.filter(UserPreferences.user_id.like(user)).all()
    preference = query
    if preference:
        for each_one in preference:
            db.session.delete(each_one)
            db.session.commit()
        flash('Perfumes has been removed', 'success')
    else:
        flash('No such record in db, please reload the page')
    return redirect(url_for('users.favourites'))


@users.route("/recommendations", methods=['GET', 'POST'])
@login_required
def recommend_perfumes():
    user = current_user.id
    query = UserPreferences.query.filter(UserPreferences.user_id.like(user)).all()
    print('\n\n\ CHUJAAAAAA \n')
    print(query)
    print(len(query))
    user_perfumes = []
    if len(query) < 3:
        flash('You have to have added at least 3 perfumes to your favourites', 'info')
        return redirect(url_for('users.favourites'))

    for p in query:
        user_perfumes.append(p.perfume_id)
    #print(user_perfumes)
    recommendations = us(user_perfumes)
    return render_template('recommended.html', title='Scents Recommended Just For You', recommendations=recommendations)
