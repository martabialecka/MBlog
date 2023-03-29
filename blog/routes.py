from flask import render_template, request, flash
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm

@app.route('/')
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template('homepage.html', all_posts=all_posts)

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

@app.route("/new-post/", methods=["GET", "POST"])
def create_entry():
    return entry()

@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    return entry(entry_id)
