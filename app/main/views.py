from flask import render_template, request, redirect, url_for, abort
from . import  main
from .forms import CommentsForm, UpdateProfile,PitchForm,UpvoteForm
from ..models import Comment,Pitch,User
from flask_login import login_required, current_user
from .. import db,photos
import markdown2

@main.route('/')
def index():
   '''
   View root page function that return the index page and its data
   '''
   title = 'Home - Welcome to the best Pitching website online'
   
   search_pitch = request.args.get('pitch_query')
   pitches= Pitch.get_all_pitches()

   return render_template('index.html', title = title, pitches=pitches)

@main.route('/interview/pitches/')
def interview():
    '''
    View root page function that returns the index page and its data
    '''

    pitches= Pitch.get_all_pitches()
    title = 'Home - Welcome to the best Pitching Website Online'
    return render_template('interview.html', title= title, pitches=pitches)

@main.route('/pick_up_lines/pitches/')
def pick_up_lines():
    '''
    View root page function that returns the index page and its data
    '''

    title ='Pick Up Lines'

    pitches= Pitch.get_all_pitches()
    return render_template('pick_up_lines.html', title = title, pitches= pitches)

@main.route('/promotion/pitches/')
def promotion():
   '''
   View root page function that returns the index page and its data
   '''
   title = 'Promotion Pitches'

   pitches= Pitch.get_all_pitches()

   return render_template('promotion.html', title=title,pitches= pitches)

@main.route('/product/pitches/')
def product():
    '''
    View root page function that returns the index page and its data 
    '''
    
    title = 'Production Pitches'
    pitches= Pitch.get_all_pitches()
    return render_template('product.html', title=title, pitches=pitches)

@main.route('/pitch/<int:pitch_id>')
def pitch(pitch_id):
    '''
    View pitch page function that returns the pitch details page and its data
    '''
    found_pitch= get_pitch(pitch_id)
    title = pitch_id
    pitch_comments =Comment.get_comments(pitch_id)

    return render_template('pitch.html',title= title, found_pitch, pitch_comments= pitch_comments)

@main.route('/search/<pitch_name>')
def search(pitch_name):
    '''
    View function to display the search results
    '''

    searched_pitches = search_pitch(pitch_name)
    title = f'search results for {pitch_name}'

    return render_template('search.html', pitches = searched_pitches) 

@main.routre('/pitch/new/', methods = ['GET','POST'])
def new_pitch():
    '''
    Function that creates new pitches
    '''

    form = PitchForm()

    if category is None:
       abort(404)

    if form.validate_on_submit():
        pitch= form.content.data
        category_id= from.category_id.data
        new_pitch=Pitch(pitch=pitch,category_id=category_id)

        new_pitch.save_pitch()
        return redirect(url_for('main.index'))

    return render_template('new_pitch.html', new_pitch_form=form, category=category)

@main.route('/category/<int: id>')
def category(id):
    '''
    function that returns pitches based on the entered category id
    '''
    category =PitchCategory.query.get(id)
    if category is None:
       abort(404)

    pitches_in_category = Pitches.get-pitch(id)
    return render_template('category.html', category=category, pitches= pitches_in_category)

@main.route('/pitch/comments/new/<int:id>', methods =['GET','POST'])
@login_required
def new_comment(id):
    form = CommentsForm()
    vote_form = UpvoteForm()
    if form.validate_on_submit():
      new_comment =Comment(pitch_id= id,comment=form.comment.data,username=current-user.username,votes=form.vote.data)
      new_comment.save_comment()
      return redirect(url_for('main.index'))
    return render_template('new_comment.html', comment_form=form, vote_form= vote_form)
    
@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter-by(username =uname).first()
    if 'photo' in request.filter:
      filename = photos.save(request.files['photo'])
      path = f'photos/{filename}'
      user.profile_pic_path= path
      db.session.commit()
    return redirect(url_for('main.profile', uname=uname))

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
         abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
       user.bio = from.bio.data

       db.session.add(user)
       dd.session.commit()

       return redirect(url_for('.profile', uname=user.username))
    return render_template('profile/update.html', form =form)

@main.route('/view/comment/<int: id>')
def view_comments(id):
    '''
    Function that returns the comments belonging to a particular pitch
    '''
    comments = Comment.get_comments(id)
    return render_template('view_comments.html',comments=comments, id=id)

@main.route('/test/<int:id>')
def test(id):
    '''
    this is route for basic testing
    '''

    pitch =Pitch.query.filter_by(id=1).first()
    return render_template('test.html',pitch=pitch)
