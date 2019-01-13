from flask import Blueprint, request, render_template, url_for, flash, redirect, session, abort

from .. import db, is_logged_in
from ..forms import RecipeForm
from ..models import Recipe

recipes = Blueprint('recipes', __name__)

# READ ALL RECIPES
@recipes.route("/", methods=['GET'])
def all_recipes():
  recipes = Recipe.query.order_by(Recipe.name).all()
  return render_template('recipes/recipe-book.html', title="My Recipes", recipes=recipes)

# READ ONE RECIPE
@recipes.route("/<string:name>")
def single_recipe(name):
  recipe = Recipe.query.filter_by(name=name).first_or_404()
  return render_template('recipes/recipe-r.html', title=recipe.name, recipe=recipe)

# ADD NEW RECIPE
@recipes.route("/new", methods=['GET', 'POST'])
@is_logged_in
def new_recipe():
  recipes = Recipe.query.order_by(Recipe.name).all()
  form = RecipeForm()
  curr_user = session['username']
  if request.method =='POST':
    if form.validate_on_submit():
      recipe = Recipe(name=form.name.data, ingredients=form.ingredients.data, 
      steps=form.steps.data, stars=form.stars.data, user_name=curr_user)
      db.session.add(recipe)
      db.session.commit()
      flash(f'{form.name.data} recipe created!', 'success')
      return redirect(url_for('.all_recipes'))
    else:
        flash('Invalid Coordintes! Please try again', 'error')
  return render_template('recipes/recipe-cu.html', title="Create Recipe", form=form, curr_user=curr_user, recipes=recipes)

# UPDATE RECIPE
@recipes.route("/<string:name>/update", methods=['GET', 'POST'])
@is_logged_in
def update_recipe(name):
  recipes = Recipe.query.order_by(Recipe.name).all()
  recipe = Recipe.query.filter_by(name=name).first_or_404()
  if recipe.user_name != session['username']:
    abort(403)
  form = RecipeForm()
  if request.method =='POST' and form.validate_on_submit():
    recipe.name = form.name.data
    recipe.ingredients = form.ingredients.data
    recipe.steps = form.steps.data
    recipe.stars = form.stars.data
    db.session.commit()
    flash(f'{form.name.data} recipe updated!','success')
    return redirect(url_for('.all_recipes'))
  elif request.method == 'GET':
    form.name.data = recipe.name
    form.ingredients.data = recipe.ingredients
    form.steps.data = recipe.steps
    form.stars.data = recipe.stars
  return render_template('recipes/recipe-cu.html', title="Update Recipe", form=form, recipes=recipes)

# DELETE RECIPE
@recipes.route("/<string:name>/delete", methods=['POST'])
@is_logged_in
def delete_recipe(name):
  recipe = Recipe.query.filter_by(name=name).first_or_404()
  if recipe.user_name != session['username']:
    abort(403)
  db.session.delete(recipe)
  db.session.commit()
  flash(f'{recipe.name} recipe deleted!','success')
  return redirect(url_for('.all_recipes'))