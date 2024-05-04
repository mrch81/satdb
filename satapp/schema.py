#!/usr/bin/env python

import logging

# Imports
import graphene
from graphene_django.types import DjangoObjectType
from satapp.models import Launcher, Owner, Payload, Satellite

logger = logging.getLogger(__name__)


# ObjectTypes

class OwnerType(DjangoObjectType):
    class Meta:
        model = Owner
        fields = ('id', 'name', 'country')


class SatelliteType(DjangoObjectType):
    class Meta:
        model = Satellite
        fields = ('id', 'name', 'owner')


class LauncherType(DjangoObjectType):
    class Meta:
        model = Launcher
        fields = ('id', 'satellites', 'launcher_type', 'launch_date')


class PayloadType(DjangoObjectType):
    class Meta:
        model = Payload
        fields = ('id', 'provider', 'satellite', 'type', 'description')


# Query

class Query(graphene.ObjectType):
    all_satellites = graphene.List(SatelliteType)
    all_owners = graphene.List(OwnerType)
    all_launchers = graphene.List(LauncherType)
    all_payloads = graphene.List(PayloadType)

    def resolve_all_satellites(self, info, **kwargs):
        return Satellite.objects.all()

    def resolve_all_owners(self, info, **kwargs):
        return Owner.objects.all()

    def resolve_all_launchers(self, info, **kwargs):
        return Launcher.objects.all()

    def resolve_all_payloads(self, info, **kwargs):
        return Payload.objects.all()


# Mutation

# Satellite mutations
class CreateSatellite(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        owner_id = graphene.Int(required=True)

    satellite = graphene.Field(SatelliteType)

    def mutate(self, info, name, owner_id):
        owner = Owner.objects.get(pk=owner_id)
        satellite = Satellite(name=name, owner=owner)
        satellite.save()
        return CreateSatellite(satellite=satellite)


class UpdateSatellite(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    satellite = graphene.Field(SatelliteType)

    def mutate(self, info, id, name):
        satellite = Satellite.objects.get(pk=id)
        satellite.name = name
        satellite.save()
        return UpdateSatellite(satellite=satellite)


# Owner mutations
class CreateOwner(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        country = graphene.String(required=True)

    owner = graphene.Field(OwnerType)

    def mutate(self, info, name, country):
        owner = Owner(name=name, country=country)
        owner.save()
        return CreateOwner(owner=owner)


class UpdateOwner(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        country = graphene.String()

    owner = graphene.Field(OwnerType)

    def mutate(self, info, id, name=None, country=None):
        owner = Owner.objects.get(pk=id)
        if name is not None:
            owner.name = name
        if country is not None:
            owner.country = country
        owner.save()
        return UpdateOwner(owner=owner)


# Launcher mutations
class CreateLauncher(graphene.Mutation):
    class Arguments:
        satellite_ids = graphene.List(graphene.ID, required=True)
        launcher_type = graphene.String(required=True)
        launch_date = graphene.Date(required=True)

    launcher = graphene.Field(LauncherType)

    def mutate(self,
               info,
               satellite_ids,
               launcher_type,
               launch_date):
        logger.info("Creating launcher")
        if satellite_ids:
            satellites = Satellite.objects.filter(id__in=satellite_ids)

        launcher = Launcher(launcher_type=launcher_type,
                            launch_date=launch_date)
        launcher.save()
        if satellites:
            launcher.satellites.clear()
            launcher.satellites.set(satellites)
            launcher.save()
        return CreateLauncher(launcher=launcher)


class UpdateLauncher(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        launcher_type = graphene.String()
        launch_date = graphene.Date()
        satellite_ids = graphene.List(graphene.ID)

    launcher = graphene.Field(LauncherType)

    def mutate(self,
               info,
               id,
               launcher_type=None,
               launch_date=None,
               satellite_ids=None):

        launcher = Launcher.objects.get(pk=id)
        if launcher_type is not None:
            launcher.launcher_type = launcher_type
        if launch_date is not None:
            launcher.launch_date = launch_date

        if satellite_ids:
            satellites = Satellite.objects.filter(id__in=satellite_ids)
            launcher.satellites.clear()
            launcher.satellites.set(satellites)

        launcher.save()

        return UpdateLauncher(launcher=launcher)


# Payload mutations
class CreatePayload(graphene.Mutation):
    class Arguments:
        provider = graphene.String(required=True)
        satellite_id = graphene.Int(required=True)
        type = graphene.String(required=True)
        description = graphene.String()

    # Define the PayloadType to be returned after mutation
    payload = graphene.Field(PayloadType)

    def mutate(self, info, provider, satellite_id, type, description):
        satellite = Satellite.objects.get(pk=satellite_id)
        payload = Payload(provider=provider,
                          satellite=satellite,
                          type=type,
                          description=description)
        payload.save()

        return CreatePayload(payload=payload)


class UpdatePayload(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        provider = graphene.String()
        satellite_id = graphene.Int()
        type = graphene.String()
        description = graphene.String()

    # Define the PayloadType to be returned after mutation
    payload = graphene.Field(PayloadType)

    def mutate(self,
               info,
               id,
               provider=None,
               satellite_id=None,
               type=None,
               description=None):

        payload = Payload.objects.get(pk=id)
        if provider is not None:
            payload.provider = provider
        if satellite_id is not None:
            payload.satellite_id = satellite_id
        if type is not None:
            payload.type = type
        if description is not None:
            payload.description = description

        payload.save()

        return UpdatePayload(payload=payload)


class Mutation(graphene.ObjectType):
    create_satellite = CreateSatellite.Field()
    update_satellite = UpdateSatellite.Field()
    create_owner = CreateOwner.Field()
    update_owner = UpdateOwner.Field()
    create_launcher = CreateLauncher.Field()
    update_launcher = UpdateLauncher.Field()
    create_payload = CreatePayload.Field()
    update_payload = UpdatePayload.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
