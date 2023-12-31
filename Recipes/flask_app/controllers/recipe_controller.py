from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import recipe_model, user_model


@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        flash('Please login!', 'user')
        return redirect('/')
    user = user_model.Users.get_one(session['id'])
    all_recipes = recipe_model.Recipes.get_all_recipe_info()
    return render_template('dashboard.html', user=user, recipes=all_recipes)

# create new recipe route


@app.route('/recipes/new')
def create_recipe_form():
    if 'id' not in session:
        flash('Please login!', 'user')
        return redirect('/')
    return render_template('recipe_new.html')

# create process


@app.route('/recipe/new/submit', methods=['post'])
def create_recipe():
    if 'id' not in session:
        flash('Please login!', 'user')
        return redirect('/')
    if not recipe_model.Recipes.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        **request.form,
        'user_id': session['id']
    }
    recipe_model.Recipes.save(data)
    return redirect('/dashboard')

# view recipe


@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    if 'id' not in session:
        flash('Please login!', 'user')
        return redirect('/')
    # current user information
    user = user_model.Users.get_one(session['id'])
    # recipe information
    # recipe = recipe_model.Recipes.get_one_recipe_info(recipe_id)
    recipe = recipe_model.Recipes.get_one_recipe_info2(recipe_id)
    return render_template('recipe_read.html', user=user, recipe=recipe)

# edit recipe route


@app.route('/recipe/edit/<int:recipe_id>')
def edit_recipe_form(recipe_id):
    if 'id' not in session:
        flash('Please login!', 'user')
        return redirect('/')
    recipe = recipe_model.Recipes.get_one(recipe_id)
    if not session['id'] == recipe.user_id:
        flash("Cannot edit other peoples recipes", 'dashboard')
        return redirect('/dashboard')
    return render_template('recipe_edit.html', recipe=recipe)

# edit process


@app.route('/recipe/edit/form/<int:recipe_id>', methods=['post'])
def edit_recipe(recipe_id):
    if 'id' not in session:
        flash('Please login!', 'user')
        return redirect('/')
    if not recipe_model.Recipes.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{recipe_id}')
    data = {
        **request.form,
        'id': recipe_id
    }
    recipe_model.Recipes.update(data)
    return redirect('/dashboard')

# delete recipe route


@app.route('/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    if 'id' not in session:
        flash('Please login!', 'user')
        return redirect('/')
    recipe = recipe_model.Recipes.get_one(recipe_id)
    if not session['id'] == recipe.user_id:
        flash("Please do not attempt to delete other peoples recipes", 'dashboard')
        return redirect('/dashboard')
    recipe_model.Recipes.delete(recipe_id)
    return redirect('/dashboard')
