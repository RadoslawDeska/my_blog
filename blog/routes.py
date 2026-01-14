from flask import flash, redirect, render_template, request

from blog import app
from blog.forms import EntryForm
from blog.models import Entry, db


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(
        Entry.pub_date.desc()
    )
    return render_template("homepage.html", all_posts=all_posts)


@app.route("/new-post/", methods=["GET", "POST"])
def create_entry():
    return handle_entry_form(mode="create")


@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    return handle_entry_form(entry, mode="edit")

def handle_entry_form(entry=None, mode="create"):
    form = EntryForm(obj=entry)
    errors = None

    if request.method == "POST":
        if form.validate_on_submit():
            if entry is None:
                entry = Entry()
                db.session.add(entry)

            form.populate_obj(entry)
            db.session.commit()

            flash("Post saved successfully!")
            return redirect(request.url)

        errors = form.errors

    return render_template("entry_form.html", form=form, errors=errors, mode=mode)
