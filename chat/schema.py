from inspect import Arguments
import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.auth.models import User

from .models import Category, Profile,Message


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class UserNode(DjangoObjectType):
    class Meta:
        model = User

class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        interfaces = (relay.Node, )
        filter_fields = ['id',]

class MessageNode(DjangoObjectType):
    class Meta:
        model = Message
        interfaces = (relay.Node, )
        filter_fields = ['id','msg','created_at']

class CreateCategoryMutation(graphene.Mutation):
    
    class Arguments:
        name = graphene.String(required=True)
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls,root,info,name):
        category = Category(name=name)
        category.save()
        return CreateCategoryMutation(category=category)

class UpdateCategoryMutation(graphene.Mutation):
    
    class Arguments:
        name = graphene.String(required=True)
        newName = graphene.String(required=True)
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls,root,info,name,newName):
        category = Category.objects.get(name=name)
        category.name = newName
        category.save()
        return UpdateCategoryMutation(category=category)

class DeleteCategoryMutation(graphene.Mutation):
    
    class Arguments:
        name = graphene.String(required=True)
    category = graphene.Field(CategoryType)
    
    @classmethod
    def mutate(cls,root,info,name):
        category = Category.objects.get(name=name)
        category.delete()
        return UpdateCategoryMutation(category=category)


class Query(ObjectType):
    user = graphene.Field(UserNode,username=graphene.String(required=True))
    all_user = graphene.List(UserNode)
    profile = relay.Node.Field(ProfileNode)
    all_profile = DjangoFilterConnectionField(ProfileNode)
    message = relay.Node.Field(MessageNode)
    all_message = DjangoFilterConnectionField(MessageNode)
    category = graphene.Field(CategoryType,name=graphene.String(required=True))

    def resolve_category(root,info,name):
        return Category.objects.get(name=name)

    def resolve_user(root,info,username):
        return User.objects.get(username=username)

    def resolve_all_user(self, info):
        return User.objects.all()


class Mutation(ObjectType):
    create_category = CreateCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()


schema = graphene.Schema(query=Query,mutation=Mutation)