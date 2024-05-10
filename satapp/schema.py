#!/usr/bin/env python

""" GraphQL schema for satapp """

# Imports
import graphene
import logging

from channels_graphql_ws import Subscription
from graphene_django.types import DjangoObjectType
from typing import Any, Dict, Optional

from satapp.models import Launcher, Owner, Payload, Satellite

logger = logging.getLogger(__name__)


# ### Map the Django models to GraphQL ObjectTypes ###

class OwnerType(DjangoObjectType):
    class Meta:
        model = Owner
        fields = ('id',
                  'name',
                  'country')


class SatelliteType(DjangoObjectType):
    class Meta:
        model = Satellite
        fields = ('id',
                  'name',
                  'sat_id',
                  'owner',
                  'tle_date',
                  'line1',
                  'line2')


class LauncherType(DjangoObjectType):
    class Meta:
        model = Launcher
        fields = ('id',
                  'satellites',
                  'launcher_type',
                  'launch_date')


class PayloadType(DjangoObjectType):
    class Meta:
        model = Payload
        fields = ('id',
                  'provider',
                  'satellite',
                  'type',
                  'description')


# ### GraphQL queries allowing data fetching operations for our models. ###
class Query(graphene.ObjectType):
    all_satellites = graphene.List(SatelliteType)
    all_owners = graphene.List(OwnerType)
    all_launchers = graphene.List(LauncherType)
    all_payloads = graphene.List(PayloadType)

    # Resolver methods to fetch data from the database.
    def resolve_all_satellites(self,
                               info: graphene.ResolveInfo,
                               **kwargs) -> QuerySet:

        return Satellite.objects.all()

    def resolve_all_owners(self,
                           info: graphene.ResolveInfo,
                           **kwargs) -> QuerySet:

        return Owner.objects.all()

    def resolve_all_launchers(self,
                              info: graphene.ResolveInfo,
                              **kwargs) -> QuerySet:

        return Launcher.objects.all()

    def resolve_all_payloads(self,
                             info: graphene.ResolveInfo,
                             **kwargs) -> QuerySet:

        return Payload.objects.all()


# ### GraphQL Mutation allowing clients to modify data ###

class CreateSatellite(graphene.Mutation):
    """Create mutation for Satellite model"""

    class Arguments:
        name = graphene.String(required=True)
        owner_id = graphene.Int(required=True)

    satellite: graphene.Field(SatelliteType)

    def mutate(self,
               info: graphene.ResolveInfo,
               name: str, owner_id: int) -> "CreateSatellite":

        owner = Owner.objects.get(pk=owner_id)
        satellite = Satellite(name=name, owner=owner)
        satellite.save()
        return CreateSatellite(satellite=satellite)


class UpdateSatellite(graphene.Mutation):
    """Update mutation for Satellite model"""

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    satellite: graphene.Field(SatelliteType)

    def mutate(self,
               info: graphene.ResolveInfo,
               id: int, name: str) -> "UpdateSatellite":

        satellite = Satellite.objects.get(pk=id)
        satellite.name = name
        satellite.save()
        return UpdateSatellite(satellite=satellite)


# Mutations for Owner model

class CreateOwner(graphene.Mutation):
   """Create mutation for Owner model"""

    class Arguments:
        name = graphene.String(required=True)
        country = graphene.String(required=True)

    owner: graphene.Field(OwnerType)

    def mutate(self,
               info: graphene.ResolveInfo,
               name: str,
               country: str) -> "CreateOwner":

        owner = Owner(name=name, country=country)
        owner.save()
        return CreateOwner(owner=owner)


class UpdateOwner(graphene.Mutation):
    """Update mutation for Owner model"""

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        country = graphene.String()

    owner: graphene.Field(OwnerType)

    def mutate(self,
               info: graphene.ResolveInfo,
               id: int,
               name: str = None,
               country: str = None) -> "UpdateOwner":

        owner = Owner.objects.get(pk=id)
        if name is not None:
            owner.name = name
        if country is not None:
            owner.country = country
        owner.save()
        return UpdateOwner(owner=owner)


class CreateLauncher(graphene.Mutation):
    """Create mutation for Launcher model"""

    class Arguments:
        satellite_ids = graphene.List(graphene.ID, required=True)
        launcher_type = graphene.String(required=True)
        launch_date = graphene.Date(required=True)

    launcher: graphene.Field(LauncherType)

    def mutate(self,
               info: graphene.ResolveInfo,
               satellite_ids: List[int],
               launcher_type: str,
               launch_date: date) -> "CreateLauncher":

        satellites = Satellite.objects.filter(id__in=satellite_ids)
        launcher = Launcher(launcher_type=launcher_type,
                            launch_date=launch_date)
        launcher.save()
        launcher.satellites.set(satellites)
        return CreateLauncher(launcher=launcher)

class UpdateLauncher(graphene.Mutation):
    """Update mutation for Launcher model"""

    class Arguments:
        id = graphene.ID(required=True)
        launcher_type = graphene.String()
        launch_date = graphene.Date()
        satellite_ids = graphene.List(graphene.ID)

    launcher: graphene.Field(LauncherType)

    def mutate(self,
               info: graphene.ResolveInfo,
               id: int,
               launcher_type: str = None,
               launch_date: date = None,
               satellite_ids: List[int] = None) -> "UpdateLauncher":

        launcher = Launcher.objects.get(pk=id)
        if launcher_type is not None:
            launcher.launcher_type = launcher_type
        if launch_date is not None:
            launcher.launch_date = launch_date
        if satellite_ids is not None:
            satellites = Satellite.objects.filter(id__in=satellite_ids)
            launcher.satellites.set(satellites)
        launcher.save()
        return UpdateLauncher(launcher=launcher)


class CreatePayload(graphene.Mutation):
    """Create mutation for Payload model"""

    class Arguments:
        provider = graphene.String(required=True)
        satellite_id = graphene.Int(required=True)
        type = graphene.String(required=True)
        description = graphene.String()

    payload: graphene.Field(PayloadType)

    def mutate(self,
               info: graphene.ResolveInfo,
               provider: str,
               satellite_id: int,
               type: str,
               description: str = None) -> "CreatePayload":

        satellite = Satellite.objects.get(pk=satellite_id)
        payload = Payload(provider=provider, 
                          satellite=satellite,
                          type=type, 
                          description=description)
        payload.save()
        return CreatePayload(payload=payload)


class UpdatePayload(graphene.Mutation):
    """Upload mutation for Payload model"""

    class Arguments:
        id = graphene.ID(required=True)
        provider = graphene.String()
        satellite_id = graphene.Int()
        type = graphene.String()
        description = graphene.String()

    payload: graphene.Field(PayloadType)

    def mutate(self,
               info: graphene.ResolveInfo,
               id: int,
               provider: str = None,
               satellite_id: int = None,
               type: str = None,
               description: str = None) -> "UpdatePayload":

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


# GraphQL Mutation root
class Mutation(graphene.ObjectType):
    create_satellite = CreateSatellite.Field()
    update_satellite = UpdateSatellite.Field()
    create_owner = CreateOwner.Field()
    update_owner = UpdateOwner.Field()
    create_launcher = CreateLauncher.Field()
    update_launcher = UpdateLauncher.Field()
    create_payload = CreatePayload.Field()
    update_payload = UpdatePayload.Field()


# GraphQL Subscription allowing a real-time subscription for satellite updates

class SatelliteSubscription(Subscription):
    """
    Sets up the subscription to handle satellite_updated event
    """
    
    # Subscribers will receive satellite_updated.
    satellite_updated: graphene.Field = graphene.Field(SatelliteType)

    async def subscribe_satellite_updated(root: Any, 
                                          info: graphene.ResolveInfo) -> Any:
        """ Subscribing to a channel named 'satellite_updated'."""
        return root.subscribe_to_channel("satellite_updated")

    async def publish(self, 
                      info: graphene.ResolveInfo,
                      payload: Any,
                      **kwargs: Dict[str, Any]) -> Any:
        """ Handle the data that needs to be sent to the subscribers. """
        logger.debug("Publishing payload: %r", payload)
        return payload


# Define schema
schema = graphene.Schema(query=Query,
                         mutation=Mutation,
                         subscription=SatelliteSubscription)
