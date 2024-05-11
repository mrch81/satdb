#!/usr/bin/env python

"""GraphQL schema for satapp."""

import datetime
import logging
from typing import Any, Dict, List, Optional

# Imports
import graphene
from channels_graphql_ws import Subscription
from django.db.models.query import QuerySet
from graphene_django.types import DjangoObjectType

from satapp.models import Launcher, Owner, Payload, Satellite

logger = logging.getLogger(__name__)


# ### Map the Django models to GraphQL ObjectTypes ###

class OwnerType(DjangoObjectType):
    """Owner type.

    Args:
        DjangoObjectType (DjangoObjectType): generic DjangoObjectType
    """

    class Meta:
        """Meta class."""

        model = Owner
        fields = ('id',
                  'name',
                  'country')


class SatelliteType(DjangoObjectType):
    """Satellite type.

    Args:
        DjangoObjectType (DjangoObjectType): generic DjangoObjectType
    """

    class Meta:
        """Meta class."""

        model = Satellite
        fields = ('id',
                  'name',
                  'sat_id',
                  'owner',
                  'tle_date',
                  'line1',
                  'line2')


class LauncherType(DjangoObjectType):
    """Launcher type.

    Args:
        DjangoObjectType (DjangoObjectType): generic DjangoObjectType
    """

    class Meta:
        """Meta class."""

        model = Launcher
        fields = ('id',
                  'satellites',
                  'launcher_type',
                  'launch_date')


class PayloadType(DjangoObjectType):
    """Payload type.

    Args:
        DjangoObjectType (DjangoObjectType): generic DjangoObjectType
    """

    class Meta:
        """Meta class."""

        model = Payload
        fields = ('id',
                  'provider',
                  'satellite',
                  'type',
                  'description')


# ### GraphQL queries allowing data fetching operations for our models. ###
class Query(graphene.ObjectType):
    """Graphql Query class to fetch data.

    Args:
        ObjectType (ObjectType): graphene ObjectType
    """

    all_satellites = graphene.List(SatelliteType)
    all_owners = graphene.List(OwnerType)
    all_launchers = graphene.List(LauncherType)
    all_payloads = graphene.List(PayloadType)

    # Resolver methods to fetch data from the database.
    def resolve_all_satellites(self,
                               info: graphene.ResolveInfo,
                               **kwargs) -> QuerySet:
        """Retrieve all satellites.

        Args:
            info (ResolveInfo): info

        Returns:
            Queryset: a queryset containing all satellites
        """
        return Satellite.objects.all()

    def resolve_all_owners(self,
                           info: graphene.ResolveInfo,
                           **kwargs) -> QuerySet:
        """Retrieve all owners.

        Args:
            info (ResolveInfo): info

        Returns:
            Queryset: a queryset containing all owners
        """
        return Owner.objects.all()

    def resolve_all_launchers(self,
                              info: graphene.ResolveInfo,
                              **kwargs) -> QuerySet:
        """Retrieve all launchers.

        Args:
            info (ResolveInfo): info

        Returns:
            Queryset: a queryset containing all launchers
        """
        return Launcher.objects.all()

    def resolve_all_payloads(self,
                             info: graphene.ResolveInfo,
                             **kwargs) -> QuerySet:
        """Retrieve all payloads.

        Args:
            info (ResolveInfo): info

        Returns:
            Queryset: a queryset containing all payloads
        """
        return Payload.objects.all()


# ### GraphQL Mutation allowing clients to modify data ###

class CreateSatellite(graphene.Mutation):
    """Create mutation for Satellite model."""

    class Arguments:  # noqa: D106
        name = graphene.String(required=True)
        owner_id = graphene.Int()
        sat_id = graphene.Int(required=True)
        line1 = graphene.String()
        line2 = graphene.String()
        tle_date = graphene.Date()

    satellite: graphene.Field = graphene.Field(SatelliteType)

    def mutate(self,
               info: graphene.ResolveInfo,
               name: str,
               sat_id: Optional[int] = None,
               line1: Optional[str] = None,
               line2: Optional[str] = None,
               tle_date: Optional[datetime.date] = None,
               owner_id: Optional[int] = None) -> graphene.Mutation:
        """Mutation method to create Satellite.

        Args:
            info (ResolveInfo): info
            name (str): name of satellite
            sat_id (int): Satellite ID
            tle_date (date): most recent date when TLE was updated
            line1 (str): line1 of TLE
            line2 (str): line2 of TLE
            owner_id (int): id of linked owner

        Returns:
            Mutation: created satellite
        """
        owner = None
        if owner_id is not None:
            owner = Owner.objects.get(pk=owner_id)
        satellite = Satellite(name=name,
                              owner=owner,
                              line1=line1,
                              line2=line2,
                              tle_date=tle_date,
                              sat_id=sat_id)
        satellite.save()
        return CreateSatellite(satellite=satellite)


class UpdateSatellite(graphene.Mutation):
    """Update mutation for Satellite model."""

    class Arguments:  # noqa: D106
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    satellite: graphene.Field = graphene.Field(SatelliteType)

    def mutate(self,
               info: graphene.ResolveInfo,
               id: int,
               name: str) -> graphene.Mutation:
        """Mutation method to update Satellite.

        Args:
            info (ResolveInfo): info
            id (int): id of satellite to update
            name (str): name of satellite

        Returns:
            Mutation: updated satellite
        """
        satellite = Satellite.objects.get(pk=id)
        satellite.name = name
        satellite.save()
        return UpdateSatellite(satellite=satellite)


class CreateOwner(graphene.Mutation):
    """Create mutation for Owner model."""

    class Arguments:  # noqa: D106
        name = graphene.String(required=True)
        country = graphene.String(required=True)

    owner: graphene.Field = graphene.Field(OwnerType)

    def mutate(self,
               info: graphene.ResolveInfo,
               name: str,
               country: str) -> graphene.Mutation:
        """Mutation method to create Owner.

        Args:
            info (ResolveInfo): info
            name (str):  name of the owner
            country (str): country of the owner

        Returns:
            Mutation: created owner
        """
        owner = Owner(name=name, country=country)
        owner.save()
        return CreateOwner(owner=owner)


class UpdateOwner(graphene.Mutation):
    """Update mutation for Owner model."""

    class Arguments:  # noqa: D106
        id = graphene.ID(required=True)
        name = graphene.String()
        country = graphene.String()

    owner: graphene.Field = graphene.Field(OwnerType)

    def mutate(self,
               info: graphene.ResolveInfo,
               id: int,
               name: Optional[str] = None,
               country: Optional[str] = None) -> graphene.Mutation:
        """Mutation method to update Owner.

        Args:
            info (ResolveInfo): info
            id (int): id of owner
            name (str):  name of the owner
            country (str): country of the owner

        Returns:
            Mutation: updated owner
        """
        owner = Owner.objects.get(pk=id)
        if name is not None:
            owner.name = name
        if country is not None:
            owner.country = country
        owner.save()
        return UpdateOwner(owner=owner)


class CreateLauncher(graphene.Mutation):
    """Create mutation for Launcher model."""

    class Arguments:  # noqa: D106
        satellite_ids = graphene.List(graphene.ID, required=True)
        launcher_type = graphene.String(required=True)
        launch_date = graphene.Date(required=True)

    launcher: graphene.Field = graphene.Field(LauncherType)

    def mutate(self,
               info: graphene.ResolveInfo,
               satellite_ids: List[int],
               launcher_type: str,
               launch_date: datetime.date) -> graphene.Mutation:
        """Mutation method to create Launcher.

        Args:
            info (ResolveInfo): info
            launcher_type (str):  type of launcher
            launch_date (date): date of launch
            satellite_ids (list) : list of satellites linked

        Returns:
            Mutation: created launcher
        """
        satellites = Satellite.objects.filter(id__in=satellite_ids)
        launcher = Launcher(launcher_type=launcher_type,
                            launch_date=launch_date)
        launcher.save()
        launcher.satellites.set(satellites)
        return CreateLauncher(launcher=launcher)


class UpdateLauncher(graphene.Mutation):
    """Update mutation for Launcher model."""

    class Arguments:  # noqa: D106
        id = graphene.ID(required=True)
        launcher_type = graphene.String()
        launch_date = graphene.Date()
        satellite_ids = graphene.List(graphene.ID)

    launcher: graphene.Field = graphene.Field(LauncherType)

    def mutate(self,
               info: graphene.ResolveInfo,
               id: int,
               launcher_type: Optional[str] = None,
               launch_date: Optional[datetime.date] = None,
               satellite_ids: Optional[List[int]] = None) -> graphene.Mutation:
        """Mutation method to update Launcher.

        Args:
            info (ResolveInfo): info
            id (int): id of launcher
            launcher_type (str):  type of launcher
            launch_date (date): date of launch
            satellite_ids (list) : list of satellites linked

        Returns:
            Mutation: updated launcher
        """
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
    """Create mutation for Payload model."""

    class Arguments:  # noqa: D106
        provider = graphene.String(required=True)
        satellite_id = graphene.Int(required=True)
        type = graphene.String(required=True)
        description = graphene.String()

    payload: graphene.Field = graphene.Field(PayloadType)

    def mutate(self,
               info: graphene.ResolveInfo,
               provider: str,
               satellite_id: int,
               type: str,
               description: Optional[str] = None) -> graphene.Mutation:
        """Mutation method to create payload.

        Args:
            info (ResolveInfo): info
            provider (str):  provider
            satellite_id (int): satellite linked to it
            type (str) : payload type
            description (str): payload description

        Returns:
            Mutation: created payload
        """
        satellite = Satellite.objects.get(pk=satellite_id)
        payload = Payload(provider=provider,
                          satellite=satellite,
                          type=type,
                          description=description)
        payload.save()
        return CreatePayload(payload=payload)


class UpdatePayload(graphene.Mutation):
    """Update mutation for Payload model."""

    class Arguments:  # noqa: D106
        id = graphene.ID(required=True)
        provider = graphene.String()
        satellite_id = graphene.Int()
        type = graphene.String()
        description = graphene.String()

    payload: graphene.Field = graphene.Field(PayloadType)

    def mutate(self,
               info: graphene.ResolveInfo,
               id: int,
               provider: Optional[str] = None,
               satellite_id: Optional[int] = None,
               type: Optional[str] = None,
               description: Optional[str] = None) -> graphene.Mutation:
        """Mutation method to update payload.

        Args:
            info (ResolveInfo): info
            id (int): id of payload
            provider (str):  provider
            satellite_id (int): satellite linked to it
            type (str) : payload type
            description (str): payload description

        Returns:
            Mutation: updated payload
        """
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
    """Mutation Root class."""

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
    """Set up the subscription to handle satellite_updated event."""

    # Subscribers will receive satellite_updated.
    satellite_updated: graphene.Field = graphene.Field(SatelliteType)

    async def subscribe_satellite_updated(root: Any,
                                          info: graphene.ResolveInfo) -> Any:
        """Subscribe to a channel named 'satellite_updated'."""
        return root.subscribe_to_channel("satellite_updated")

    async def publish(self,
                      info: graphene.ResolveInfo,
                      payload: Any,
                      **kwargs: Dict[str, Any]) -> Any:
        """Handle the data that needs to be sent to the subscribers."""
        logger.debug("Publishing payload: %r", payload)
        return payload


# Define schema
schema = graphene.Schema(query=Query,
                         mutation=Mutation,
                         subscription=SatelliteSubscription)
