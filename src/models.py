from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class User(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=50)
    gender = fields.CharField(max_length=50)
    status = fields.CharField(max_length=50)


class Post(models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    title = fields.TextField()
    body = fields.TextField()


Post_Pydantic = pydantic_queryset_creator(Post, name="Post")
User_Pydantic = pydantic_model_creator(User, name="User")
