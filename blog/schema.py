import graphene
from graphene_django import DjangoObjectType
from .models import *

# FORMATTING MODELS INTO OBJECT TYPE
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = '__all__'

class TopicType(DjangoObjectType):
    class Meta:
        model = Topic
        fields = '__all__'

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = '__all__'

# FOR QUERY - LIST, DETAILED
class Query(graphene.ObjectType):
    # LIST VIEW
    category_list = graphene.List(CategoryType)
    topic_list = graphene.List(TopicType)
    post_list = graphene.List(PostType)

    def resolve_category_list(root, info):
        return Category.objects.all()

    def resolve_topic_list(root, info):
        return Topic.objects.all()

    def resolve_post_list(root, info):
        return Post.objects.all()

    # DETAILED VIEW
    category_detailed = graphene.Field(CategoryType, id=graphene.ID())
    topic_detailed = graphene.Field(TopicType, id=graphene.ID())
    post_detailed = graphene.Field(PostType, id=graphene.ID())

    def resolve_category_detailed(root, info, id):
        return Category.objects.get(id=id)

    def resolve_topic_detailed(root, info, id):
        return Topic.objects.get(id=id)

    def resolve_post_detailed(root, info, id):
        return Post.objects.get(id=id)
    
    # ONE TO MANY
    category_to_topic = graphene.List(TopicType, id=graphene.ID())
    category_to_post = graphene.List(PostType, id=graphene.ID())
    topic_to_post = graphene.List(PostType, id=graphene.ID())

    def resolve_category_to_topic(root, info, id):
        return Topic.objects.filter(category=id)

    def resolve_category_to_post(root, info, id):
        return Post.objects.filter(category=id)

    def resolve_topic_to_post(root, info, id):
        return Post.objects.filter(topic=id)


# FOR CATEGORY CREATE & UPDATE & DELETE
class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CreateCategory(category=category)

class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id, name):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return UpdateCategory(category=category)

class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(id=id)
        category.delete()
        return

# FOR TOPIC CREATE & UPDATE & DELETE
class CreateTopic(graphene.Mutation):
    class Arguments:
        category_id = graphene.Int(required=True)
        name = graphene.String(required=True)

    topic = graphene.Field(TopicType)

    @classmethod
    def mutate(cls, root, info, category_id, name):
        category = Category.objects.get(id=category_id)
        topic = Topic(category=category, name=name)
        topic.save()
        return CreateTopic(topic=topic)

class UpdateTopic(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    topic = graphene.Field(TopicType)

    @classmethod
    def mutate(cls, root, info, id, name):
        topic = Topic.objects.get(id=id)
        topic.name = name
        topic.save()
        return UpdateTopic(topic=topic)

class DeleteTopic(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    topic = graphene.Field(TopicType)

    @classmethod
    def mutate(cls, root, info, id):
        topic = Topic.objects.get(id=id)
        topic.delete()
        return

# FOR POST CREATE & UPDATE & DELETE
class CreatePost(graphene.Mutation):
    class Arguments:
        category_id = graphene.ID(required=True)
        topic_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        snippet = graphene.String(required=True)
        description = graphene.String(required=True)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, category_id, topic_id, title, snippet, description):
        category = Category.objects.get(id=category_id)
        topic = Topic.objects.get(id=topic_id)
        post = Post(category=category,
                    topic=topic,
                    title=title,
                    snippet=snippet,
                    description=description)
        post.save()
        return CreatePost(post=post)

class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String(required=True)
        snippet = graphene.String(required=True)
        description = graphene.String(required=True)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, id, title, snippet, description):
        post = Post.objects.get(id=id)
        post.title = title
        post.snippet = snippet
        post.description = description
        post.save()
        return UpdatePost(post=post)

class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    post = graphene.Field(PostType)

    @classmethod
    def mutate(cls, root, info, id):
        post = Post.objects.get(id=id)
        post.delete()
        return

class Mutation(graphene.ObjectType):
    # FOR CATEGORY
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()

    # FOR TOPIC
    create_topic = CreateTopic.Field()
    update_topic = UpdateTopic.Field()
    delete_topic = DeleteTopic.Field()

    # FOR POST
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()

# SCHEMA FOR QUERY AND MUTATION
schema = graphene.Schema(query=Query, mutation=Mutation)