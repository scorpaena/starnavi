Abstract
--------
This is a test task for Starnavi.
It is made using Django/DRF framework and represents simple social network, where the authorized users can create posts and like/unlike them.
For data storage the Python standard SQLite database is used (to make it simpler to run during the check).

Requirements
------------
1. Install all the required modules:
  `pip install -r requirements`
2. Install Postman (follow the URL provided):
  https://www.tecmint.com/install-postman-on-linux-desktop/
3. Run the migration:
  `python manage.py migrate`
4. The project uses default insecure SECRET_KEY. To make it secure, create `.env` file according to the `.env.example`. Also refer to [this link](https://www.youtube.com/watch?v=5iWhQWVXosU&t=0s) for detailed information (note: for Ubuntu use `.bashrc` instead of `.bash_profile`)

Instructions
------------
1. Create superuser:
  `python manage.py createsuperuser`
2. Run the server:
  `python manage.py runserver`
3. To create a user, go to <http://127.0.0.1:8000/user/signup/> and fill in all the required fields.
4. To login the user, go to <http://127.0.0.1:8000/user/login/>. Obtain and copy the "access" token from the response body.
5. To create a post, open Postman, go to <http://127.0.0.1:8000/post/>, choose method POST, fill the KEYs "title", "content" in request 'Body' and put in 'Header' KEY 'Authorization', VALUE 'Bearer <Ctrl+V to past copied token>'.
6. To like/unlike the post, go to <http://127.0.0.1:8000/post/1/>, choose method PUT,  fill the KEY "like_unlike", VALUE "like" or "unlike" in request 'Body'.
7. To see stats of the 'post vs likes' ratio in certain dates range, go to <http://127.0.0.1:8000/post/date_from/date_to>, where 'date_from' and 'date_to' are in 'YYYY-MM-DD' format.
8. To see users 'last_login' information, go to <http://127.0.0.1:8000/user/lastlogin/> (note: this url is visible for superuser only).
9. Go to <http://127.0.0.1:8000/user/logout>, choose method GET to logout the current user.
