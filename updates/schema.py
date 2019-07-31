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
    has_next_version = graphene.Boolean()
    next_version = graphene.Int()

    def resolve_all_sets(self, info, **kwargs):
        return Set.objects.all()

    def resolve_has_next_version(self, info, **kwargs):
        return bool(self.next_version)

    def resolve_next_version(self, info, **kwargs):
        if self.next_version:
            return self.next_version.pk
        return 0

    class Meta:
        model = Version
        fields = ['version', 'id']


class Query(graphene.ObjectType):
    all_versions = graphene.List(VersionType)
    latest_version = graphene.Field(VersionType)

    version = graphene.Field(VersionType, version_id=graphene.Int())

    def resolve_all_versions(self, info, **kwargs):
        return Version.objects.all()

    def resolve_latest_version(self, info, **kwargs):
        return Version.objects.latest('id')

    def resolve_version(self, info, version_id):
        return Version.objects.get(pk=version_id)
