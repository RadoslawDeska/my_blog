from flask import flash, redirect, render_template, request, url_for

from blog.forms import EntryForm
from blog.models import Entry, db


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

            flash("Post saved successfully!")  # USUNĄĆ I SPRAWDZIĆ czy
            return redirect(url_for("index"))

        errors = form.errors

    return render_template(
        "entry_form.html", form=form, errors=errors, mode=mode
    )


def handle_remove(entry):
    db.session.delete(entry)
    db.session.commit()

    flash("Post removed successfully")
    if "drafts" in request.referrer:
        return redirect(request.referrer)
    else:
        return redirect(url_for("index"))
