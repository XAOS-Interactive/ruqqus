from urllib.parse import urlparse
from time import time

from teedee.helpers.wrappers import *
from teedee.helpers.base36 import *
from teedee.helpers.sanitize import *
from teedee.classes import *
from flask import *
from teedee.__main__ import app, db

@app.route("/api/vote/post/<post_id>/<x>", methods=["POST"])
@is_not_banned
@validate_formkey
def vote_post(post_id, x, v):

    
    if x not in ["-1", "0","1"]:
        abort(400)

    x=int(x)
    post_id=base36decode(post_id)

    post = db.query(Submission).filter_by(id=post_id).first()
    if not post:
        abort(404)

    if post.is_banned:
        abort(403)

    #check for existing vote
    existing = db.query(Vote).filter_by(user_id=v.id, submission_id=post_id).first()
    if existing:
        print(f"existing vote {existing.is_up}")
        existing.change_to(x)
        return redirect(post.permalink)
    
    print('new vote')
    print(v.id, x, post_id)
    vote=Vote(user_id=v.id,
              vote_type=x,
              submission_id=post_id
              )

    print(vote.user_id)

    db.add(vote)
    db.commit()

    return redirect(post.permalink)
                    
                    
