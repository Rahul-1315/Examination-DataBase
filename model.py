from peewee import *

db = SqliteDatabase("Online_exam.db")

class User(Model):
	username = CharField()
	email = CharField()
	password = CharField()

	class Meta:
		database = db


class Subject(Model):
	subject_name=CharField()
	subject_code=CharField()		
	subject_outcomes=CharField()

	class Meta:
		database = db


class Question(Model):
	statement = TextField()
	option1 = CharField()
	option2 = CharField()
	option3 = CharField()
	option4 = CharField()
	right_option = IntegerField()
	subject_code = ForeignKeyField(Subject)

	class Meta:
		database = db

class Response(Model):
	qid=ForeignKeyField(Question)
	response=IntegerField()
	subject_code=IntegerField(Subject)
	user = ForeignKeyField(User)

	class Meta:
		database = db


class Result(Model):
	username=ForeignKeyField(User)
	subject_code=ForeignKeyField(Subject)
	max_marks=IntegerField(default=20)
	min_marks=IntegerField(default=0)
	marks_obtained=IntegerField(default=0)
	grade=CharField(default="D")
	state=CharField(default="Average")
	is_taken = BooleanField(default=False)

	class Meta:
		database = db


if __name__ == '__main__': 
	db.connect()
	db.create_tables([User,Question,Subject,Response,Result])

