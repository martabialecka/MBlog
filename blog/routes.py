from flask import render_template, request, flash, session, redirect, url_for
import functools
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm, LoginForm

def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get('logged_in'):
            return view_func(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return check_permissions

@app.route('/')
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template('homepage.html', all_posts=all_posts, logged_in=session.get('logged_in'))

def entry(entry_id = None):
    '''
    entry_id == None means a new entry
    entry_id != None means edit the entry at entry_id
    '''
    if entry_id is not None:
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
        flash_message = 'Wpis zmieniony!'
    else:
        entry = None
        form = EntryForm()
        flash_message = 'Dodano nowy wpis!'
    errors = None

    if request.method == 'POST':
        if form.validate_on_submit():
            if entry is not None:
                form.populate_obj(entry)
            else:
                entry = Entry(
                    title=form.title.data,
                    body=form.body.data,
                    is_published=form.is_published.data
                )
                db.session.add(entry)
            db.session.commit()
            flash(flash_message)
        else:
            errors = form.errors

    return render_template('entry_form.html', form=form, errors=errors)

@app.route('/new-post/', methods=['GET', 'POST'])
@login_required
def create_entry():
    return entry()

@app.route('/edit-post/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    return entry(entry_id)

@app.route('/delete-post/<int:entry_id>', methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get(entry_id)
    if entry is not None:
        db.session.delete(entry)
        db.session.commit()
        flash('Wpis usunięty.')
    return redirect('/')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('Jesteś zalogowana.', 'success')
            return redirect(next_url or url_for('index'))
        else:
            errors = form.errors
    return render_template('login_form.html', form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('Zostałaś wylogowana.', 'success')
    return redirect(url_for('index'))

@app.route('/drafts/', methods=['GET'])
@login_required
def list_drafts():
    drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
    return render_template('drafts.html', drafts=drafts)
