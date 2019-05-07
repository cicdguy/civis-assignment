#!/usr/bin/env python

import os
import sys
from flask import Flask, flash, render_template, redirect, request
from flask_wtf import FlaskForm
from flask_env import MetaFlaskEnv
from pymongo import MongoClient
from wtforms import TextField, IntegerField, SubmitField

# Classes
class CreateTask(FlaskForm):
    title = TextField('Task Title')
    shortdesc = TextField('Short Description')
    priority = IntegerField('Priority')
    create = SubmitField('Create')

class DeleteTask(FlaskForm):
    key = TextField('Task ID')
    title = TextField('Task Title')
    delete = SubmitField('Delete')

class UpdateTask(FlaskForm):
    key = TextField('Task Key')
    shortdesc = TextField('Short Description')
    update = SubmitField('Update')

class ResetTask(FlaskForm):
    reset = SubmitField('Reset')


# Configuration
class Configuration(metaclass=MetaFlaskEnv):
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = 80
    SECRET_KEY = "yoursecretkey"

app = Flask(__name__)
app.config.from_object(Configuration)
app.config.update(dict(SECRET_KEY=app.config["SECRET_KEY"]))

# Init client/dbh. Uses DB env var
if "DB" in os.environ:
    client = MongoClient(os.environ.get('DB'))
    db = client.TaskManager
else:
    print("Please set the `DB` environment var. Ex. mongodb://localhost:27017")
    sys.exit(1)

# Set task_id
if db.settings.find({'name': 'task_id'}).count() <= 0:
    print("task_id not found, creating....")
    # Task IDs will start at 0
    db.settings.insert_one({'name': 'task_id', 'value': 0})

# Update task func
def updateTaskID(value):
    task_id = db.settings.find_one()['value']
    task_id += value
    db.settings.update_one(
        {'name': 'task_id'},
        {'$set':
            {'value': task_id}
        })

# Create task func
def createTask(form):
    title = form.title.data
    priority = form.priority.data
    shortdesc = form.shortdesc.data
    task_id = db.settings.find_one()['value']
    task = {'id': task_id,
            'title': title,
            'shortdesc': shortdesc,
            'priority': priority}
    db.tasks.insert_one(task)
    updateTaskID(1)
    return redirect('/')

# Delete task func
def deleteTask(form):
    key = form.key.data
    if(key):
        db.tasks.delete_many({'id': int(key)})
    return redirect('/')

# Update task func
def updateTask(form):
    key = form.key.data
    shortdesc = form.shortdesc.data
    db.tasks.update_one(
        {"id": int(key)},
        {"$set":
            {"shortdesc": shortdesc}
         }
    )
    return redirect('/')

# Reset all tasks
def resetTask(form):
    db.tasks.drop()
    db.settings.drop()
    db.settings.insert_one({'name': 'task_id', 'value': 0})
    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def main():
    # create form
    cform = CreateTask(prefix='cform')
    dform = DeleteTask(prefix='dform')
    uform = UpdateTask(prefix='uform')
    reset = ResetTask(prefix='reset')

    # response
    if cform.validate_on_submit() and cform.create.data:
        return createTask(cform)
    if dform.validate_on_submit() and dform.delete.data:
        return deleteTask(dform)
    if uform.validate_on_submit() and uform.update.data:
        return updateTask(uform)
    if reset.validate_on_submit() and reset.reset.data:
        return resetTask(reset)

    # read all data
    docs = db.tasks.find()
    data = []
    for i in docs:
        data.append(i)

    return render_template('index.html', cform=cform, dform=dform, uform=uform,
                           data=data, reset=reset)


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"],
            host=app.config["HOST"],
            port=app.config["PORT"])
