from graphene_django import DjangoObjectType
import graphene

from updates.models import Version, Set, History, Level


class LevelType(DjangoObjectType):
    class Meta:
        model = Level


class HistoryType(DjangoObjectType):
    class Meta:
        model = History


class SetType(DjangoObjectType):
    class Meta:
        model = Set


class VersionType(DjangoObjectType):
    all_sets = graphene.List(SetType)

    def resolve_all_sets(self, info, **kwargs):
        return Set.objects.all()

    class Meta:
        model = Version


class Query(graphene.ObjectType):
    all_versions = graphene.List(VersionType)
    latest_version = graphene.Field(VersionType)

    def resolve_all_versions(self, info, **kwargs):
        return Version.objects.all()

    def resolve_latest_version(self, info, **kwargs):
        return Version.objects.latest('id')
