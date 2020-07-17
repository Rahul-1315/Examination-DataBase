# runserver.py
from bottle import get, run, jinja2_view, post, request, redirect, route, response
from model import User, Subject, Question, Response, Result, db
db.connect()


@get("/")
@jinja2_view("login.html")
def home():
    return


@get("/login")
@jinja2_view("login.html")
def log():
    return


@post("/login")
def signin():
    username = request.forms.get('username')
    password = request.forms.get('password')
    print(username)
    print(password)
    try:
        user = User.get(User.username == username)
        print(user)
    except:
        return "User does not exist!"

    if user.password == password:
        response.set_cookie("username", str(user.id))
        return redirect("/choosesub")
    else:

        return "Invalid Credentials!!"


@get("/signup")
@jinja2_view("signup.html")
def signup():
    return


@post("/signup")
def signup():
    username = request.forms.get('username')

    email = request.forms.get('email')
    password = request.forms.get('password')

    users = User.select().where(User.username == username)

    if len(users) != 0:
        return "User already exists!"
    else:
        User.create(username=username, email=email, password=password)
    return redirect("/signup")


@get("/choosesub")
@jinja2_view("choosesub.html")
def choosesub():
    subject = Subject.select()[0]
    return {"subject": subject}


@post("/choosesub")
@jinja2_view("choosesub.html")
def choosesub():
    return


@get("/sub/<subject_id>")
@jinja2_view("sub2.html")
def sub2(subject_id):
    subject = Subject.get(Subject.id == subject_id)
    questions = Question.filter(Question.subject_code == subject)
    return {"subject": subject, "questions": questions}


@post("/sub/<subject_id>")
@jinja2_view("sub2.html")
def sub2(subject_id):

    username = request.get_cookie("username")
    subject = Subject.get(Subject.id == subject_id)
    user = User.get(User.id == int(username))
    print(user)

    result = Result.select().where(Result.username == int(username))
    if (len(result) != 0) and (result[0].is_taken == True):
        return redirect("/result")

    for question in Question.filter(Question.subject_code == subject):
        res = request.forms.get(f"question-{question.id}")
        response = Response(qid=question.id,
                            subject_code=subject_id,
                            user=user, response=res)
        response.save()

        try:
            result = Result.get(Result.username == user,
                                Result.subject_code == subject)
        except:
            result = Result(username=user, subject_code=subject, is_taken=True)

        if int(res) == question.right_option:
            result.marks_obtained += 1

            if result.marks_obtained == 20:
                result.grade = "A"
                result.state = "Outstanding!"

            elif result.marks_obtained > 13:
                result.grade = "B"
                result.state = "Good!"

            elif result.marks_obtained > 7:
                result.grade = "C"
                result.state = "Average!"

            else:
                result.grade = "D"
                result.state = "Poor!"
        else:
            result.marks_obtained += 0

        result.save()
        subject = subject.select()[0]

    return redirect("/choosesub")


# @get("/choosesub")
# @jinja2_view("choosesub.html")
# def choosesub():
# 	return

@get("/result")
@jinja2_view("result.html")
def result():
    username = request.get_cookie("username")
    user = User.get(User.id == int(username))
    subjects = Subject.select()
    # result = Result.select().where(Result.username==user,
    # 								Result.subject_code==subject)
    # print(result)
    return {"subjects": subjects}


@get("/result/<subject_id:int>")
@jinja2_view("result_details.html")
def result(subject_id):
    username = request.get_cookie("username")
    print(username)
    subject = Subject.get(Subject.id == subject_id)
    user = User.get(User.id == int(username))
    responses = Response.select().where(Response.user == user,
                                        Response.subject_code == subject)
    result = Result.get(Result.username == user,
                        Result.subject_code == subject)
    return {"result": result, "subject": subject, "responses": responses}


run(host="localhost",
    port="8080",
    debug=True)
