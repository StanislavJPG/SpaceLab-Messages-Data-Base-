from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=50)
    gender = fields.CharField(max_length=50)
    status = fields.CharField(max_length=50)


class Comment(models.Model):

    id = fields.IntField(pk=True)
    post_id = fields.IntField()
    name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=100)
    body = fields.TextField()


Comment_Pydantic = pydantic_model_creator(Comment, name="Comment")
User_Pydantic = pydantic_model_creator(User, name="User")
