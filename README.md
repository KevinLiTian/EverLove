# EverLove - An Online Dating Application

This is [CS50W](https://cs50.harvard.edu/web/2020/)'s final capstone project, utilizes Django in the back-end and JavaScript in the front-end

## What is EverLove?

We aim to help those who willing to slowly get to know each other and find deep, natural like affinity to find other like-minded individuals

## Distinctiveness and Complexity

EverLove is an dating app where users each has their own profile, regarding personal information to better match a "soulmate". In addition, users can filter by gender, age, etc. to find the one they like, they can also hit the match button to use the matching algorithm to find who is most likely the "soulmate"

EverLove isn't like the Network app where users can post and like posts, or follow other users to see their posts; in EverLove, users only customize their profile to have a better chance of finding the one for them, and cannot post nor follow others

EverLove isn't like the Commerce app where users bid on listings and can post, follow or close listings; in EverLove, there's no "listing", users can only match up with other users

EverLove's website utilizes Django as back-end which handles `GET`, `POST`, and `PUT` requests, and also comes with an authentication system. Moreover, the back-end provides both filter and matching APIs that respond JSON reponses for the front-end to fetch user information with AJAX. EverLove's website utilizes JavaScript in the front-end to control CSS animations, HTML element properties and also fetch JSON responses from APIs. Bootstrap is used as the CSS framework for the website too

## Understanding the File Structure

The `EverLove` directory contains the configuration and settings of the project. The `web` directory contains the app itself

Inside of the `web` directory:

- `admin.py`: Register all models for Django Admin
- `models.py`: The database has four models, `User`, `Job`, `Hobby` and `UserWithHobby` where the first three works as the name implies, `UserWithHobby` records which `User` has which `Hobby`
- `urls.py`: All relevant URLs including `index`, `profile`, etc. and also two APIs
- `views.py`: All back-end operations including the authentication system, APIs, algorithms, etc.
- `templates`: All HTML files for views to render using common Django template language such as `{% extends %}`, `{% url %}`, `{% for %}`, `{% if %}`, etc.
- `static`:
  - `styles.css`: Style sheet that all HTML templates uses, written in `styles.scss` and compiled into CSS
  - `app.js`: All JavaScript code to control user interaction, API fetching and CSS animation

## How to Run?

Clone this repository by running the following command:

```sh
git clone https://github.com/KevinLiTian/EverLove.git
```

In the root directory, run the following command to start a Django local server:

```sh
python manage.py runserver
```

Open up the server address given in the terminal with the browser of your choice (Chrome is recommanded)