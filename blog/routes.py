import functools
from urllib.parse import urljoin, urlparse

from flask import flash, redirect, render_template, request, session, url_for

from blog import app
from blog.forms import EmptyForm, LoginForm
from blog.handlers import handle_entry_form, handle_remove
from blog.models import Entry


def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get("logged_in"):
            return view_func(*args, **kwargs)
        return redirect(url_for("login", next=request.path))

    return check_permissions


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return (
        test_url.scheme in ("http", "https")
        and ref_url.netloc == test_url.netloc
    )


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(
        Entry.pub_date.desc()
    )
    delete_form = EmptyForm()
    return render_template("homepage.html", all_posts=all_posts, delete_form=delete_form)


@app.route("/new-post/", methods=["GET", "POST"])
@login_required
def create_entry():
    return handle_entry_form(mode="create")


@app.route("/drafts")
@login_required
def list_drafts():
    drafts = Entry.query.filter_by(is_published=False).order_by(
        Entry.pub_date.desc()
    )
    delete_form = EmptyForm()
    return render_template("drafts.html", drafts=drafts, delete_form=delete_form)


@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    return handle_entry_form(entry, mode="edit")


@app.route("/delete/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    form = EmptyForm() # Create the form
    
    # This validates the CSRF token in the POST data
    if form.validate_on_submit():
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        return handle_remove(entry)
    
    # If the token is missing/invalid, prevent deletion
    flash("Invalid CSRF token.", "danger")
    return redirect(url_for("index"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get("next")

    # VALIDATE THE URL
    if not next_url or not is_safe_url(next_url):
        next_url = url_for("index")
    
    if request.method == "POST":
        if form.validate_on_submit():
            session["logged_in"] = True
            session.permanent = True  # Use cookie to store session.
            flash("You are now logged in.", "success")
            return redirect(next_url)
        else:
            errors = form.errors
    return render_template("login_form.html", form=form, errors=errors)


@app.route("/logout/", methods=["GET", "POST"])
def logout():
    if request.method == "POST":
        session.clear()
        flash("You are now logged out.", "success")
    return redirect(url_for("index"))
