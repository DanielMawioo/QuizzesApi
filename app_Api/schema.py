from graphene_django import DjangoObjectType
from graphene import relay, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
import graphene
from .models import Quizzes, Category,Question, Answer
from graphene import ObjectType, Schema


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")

class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        filter_fields = ["id", "title", "category"]
        interfaces = (relay.Node, )
    

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        filter_fields = ["title", "quiz"]
        interfaces = (relay.Node, )

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        filter_fields = ["question", "answer_text"]
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    quizzes = relay.Node.Field(QuizzesType)
    all_quizzes = DjangoFilterConnectionField(QuizzesType)
    all_questions = graphene.Field(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnswerType, id=graphene.Int())

    def resolve_quizzes(self, info):
        return Quizzes.objects.all()

    
    def resolve_all_questions(self, info, id):
        return Question.objects.get(pk=id)

    def resolve_all_answers(self, info ,id):
        return Answer.objects.filter(question=id)

class CategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls,root, info, name):
        category= Category(name=name)
        category.save()
        return CategoryMutation(category=category)

class Mutation(graphene.ObjectType):
    update_category = CategoryMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)