from flask import render_template, request, redirect, url_for

from . import app 
from .database import session, Entry


@app.route("/")
@app.route("/page/<int:page>")
def entries(page=1):
    entries_per_page = 10
    
    if (request.args.get("limit")):
        entries_per_page = int(request.args.get("limit"))
    
    if (type(entries_per_page) == int and entries_per_page > 0 and entries_per_page <= 50):
        PAGINATE_BY = entries_per_page
    
    PAGINATE_BY = entries_per_page
        
    # Zero-indexed page
    page_index = page - 1
    
    count = session.query(Entry).count()
    
    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY
    
    total_pages = (count - 1) // PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0
    
    entries = session.query(Entry); 
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]
    
    return render_template("entries.html", 
                entries=entries, 
                has_next=has_next, 
                has_prev=has_prev, 
                page=page, 
                total_pages=total_pages)
                
@app.route("/entry/<id>")
def single_entry(id):
    entry = session.query(Entry).filter(Entry.id==id).first()
    return render_template("single_entry.html", entry=entry)
                
@app.route("/entry/add", methods = ["GET"])
def add_entry_get(): 
    return render_template("add_entry.html")
    
@app.route("/entry/add", methods=["POST"])
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
    )
    session.add(entry)
    session.commit()
    return redirect("https://anne-jones-thinkful-annejones817.c9users.io/page/1")

@app.route("/entry/<id>/edit", methods = ["GET"])
def edit_entry_get(id): 
    entry = session.query(Entry).filter(Entry.id==id).first()
    return render_template("edit_entry.html", entry=entry)
    
@app.route("/entry/<id>/edit", methods = ["POST"])
def edit_entry_PUT(id): 
    entry = session.query(Entry).filter(Entry.id==id).first()
    entry.title=request.form["title"]
    entry.content=request.form["content"]
    session.commit()
    return redirect("https://anne-jones-thinkful-annejones817.c9users.io/page/1")

@app.route("/entry/<id>/delete", methods = ["GET"])
def delete_entry_get(id): 
    entry = session.query(Entry).filter(Entry.id==id).first()
    return render_template("delete_entry.html", entry=entry)
    
@app.route("/entry/<id>/delete", methods = ["POST"])
def delete_entry_post(id): 
    entry = session.query(Entry).filter(Entry.id==id).first()
    session.delete(entry)
    session.commit()
    return redirect("https://anne-jones-thinkful-annejones817.c9users.io/page/1")    
    

    