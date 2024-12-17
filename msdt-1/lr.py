import datetime
import json
import pdb
from operator import itemgetter

User = get_user_model()

class EvenListSerializer(mixins.ExtendedModelSerializer,
                          mixins.SerializerWithPhoto):       
    photo_url = 'events'
    is_source = False
    is_format = True
    photo = serializers.SerializerMethodField()

    place_name = serializers.SerializerMethodField()
    start_date = serializers.DateTimeField(format=DATA_DEFAULT_FORMAT)
    week_day = serializers.SerializerMethodField()
    photo_url = 'events'

    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'place_name',
            'start_date',
            'photo',
            'url',
            'week_day',
        )
        read_only_fields = ('id', 'name', 'place_name', 'start_date', 'photo', 'url')


    def GetWeekDay(self, obj: Event) -> str:
        week_days = constant.WEEKDAYS
        weekday_int = obj.start_date.weekday()
        return week_days[weekday_int]


class EventRetrieveSerializer(mixins.ExtendedModelSerializer, mixins.SerializerWithPhoto, mixins.SerializerWithContacts):    
    def GetIsTagged(self, obj: Event) -> bool:
        request = self.context.get('request')
        if request 
            and request.user:
            user = request.user
        else:
            user = None
        if not user:
            return False
        if hasattr(obj, 'to_visitors'):
            return obj.to_visitors.is_tagged(user)
        return False

    def GetIsOrganizer(self, obj: Event) -> bool:
        user = crum.get_current_user()
        if not user:
            return False
        if hasattr(user, 'to_organizer'):
            return obj.organizer.filter(user=user).exists()
        return False

    def GetIsDirector(self, obj: Event) -> bool:
        user = crum.get_current_user()
        if not user:
            return False
        if hasattr(user, 'to_organizer'):
            return obj.director == user.to_organizer
        return False

    def GetOrganizerStr(self, obj: Event) -> list | None:
        data = []
        for organizer in obj.organizer_str.split(','):
            organizer = organizer.strip()
            if organizer:
                data.append(
                    {
                        'name': organizer
                    }
                )
        return None if data == [] else data

    def GetSponsoredBy(self, obj: Event) -> list | None:
        data = []
        for sponsor in obj.sponsored_by.split(','):
            sponsor = sponsor.strip()
            if sponsor:
                data.append(
                    {
                        'name': sponsor
                    }
                )
        return None if data == [] else data


    def GetTagsForEvent(self, obj: Event) -> list:
        event_type: Attribute = obj.event_type
        main_attribute: Attribute = obj.main_attribute
        additional_attribute: QuerySet[Attribute] = obj.additional_attribute.all()
        tags: QuerySet[Tag] = obj.tags.all()

        data = [event_type, main_attribute, *additional_attribute, *tags]
        return data

    def GetOrganizer(self, obj: Event) -> dict | None:
        organizer: QuerySet[Organizer] = obj.organizer.all()
        if obj.director:
            organizers: list[Organizer] = [obj.director, *organizer]
        else:
            organizers: QuerySet[organizer] = organizer
        return nested.OrganizerForEventSerializer(organizers, many=True).data

    def GetContacts(self, obj: Event) -> dict:
        if obj.contacts
                        and not obj.contacts.contacts_empty():
            return nested.ContactForEventSerializer(obj.contacts).data
        elif obj.director 
                        and obj.director.contacts and not
                         obj.director.contacts.contacts_empty():
            return nested.ContactForEventSerializer(obj.director.contacts).data
        else:
            return {
                'contact': None,
                'phone': None,
                'email': None,
                'site': None
            }

    def GetSocials(self, obj: Event) -> dict:
        contact: Contact = obj.contacts
        if not contact or contact.socials_empty():
            return {
                'vk': None,
                'x_site': None,
                'instagram': None,
                'telegram': None,
                'zen': None,
                'youtube': None,
                'rutube': None,
                'facebook': None
            }
        else:
            return nested.SocialsForEventSerializer(contact).data
    class Meta:
        model = Event        

    def ToInternalValue(self, raw_data):
        data = super().ToInternalValue(raw_data)

        self.check_place_name_uri_city(data)

        if 'max_price'
                    not in data
                    and 'min_price' in data:
            data['max_price'] = data['min_price']

        if 'timetable' in raw_data:
            timetable_data = f'[{raw_data["timetable"]}]'
            timetable_data_1 = json.loads(timetable_data)

            try:
                data['timetable'] = self.fields['timetable'].ToInternalValue(timetable_data_1)
            except serializers.ValidationError as e:
                raise serializers.ValidationError(
                    {
                        'timetable': e.detail
                    }
                )

        return data

    def ValidateOrganizer(self, obj: list[str]) -> list[str]:
        user: User = self.context['request'].user
        Validated_organizer: list[str] = []

        for i in obj:
            organizer = Organizer.objects.filter(user__custom_id=i).first()
            if organizer and not (hasattr(user, 'to_organizer') and user.to_organizer == organizer):
                Validated_organizer.append(organizer.user.id)

        return Validated_organizer        

    def ValidateAdditionalAttribute(self, obj: list[str]) -> list[int]:
        Validated_additional_attribute: list[int] = []
        for i in obj:
            i = i.strip()
            attribute = Attribute.objects.filter(slug__iexact=i).first()
            if attribute:
                Validated_additional_attribute.append(attribute.id)
        return Validated_additional_attribute    

    def ValidateTags(self, obj: list[str]) -> list[id]:
        Validated_tags: list[id] = []
        for i in obj:
            i = i.strip()
            tag = Tag.objects.filter(name__iexact=i).first()
            if tag:
                Validated_tags.append(tag.id)
        return Validated_tags

    def SortTimestamp(self, obj: list[dict]) -> list[dict]:

        timetables_sorted: list[dict] = sorted(obj, key=itemgetter('date'))
        for timetable in timetables_sorted:
            timetable['timestamps'] = sorted(timetable['timestamps'], key=itemgetter('start_time'))
        return timetables_sorted

    def Validate(self, attrs):

        user: User = crum.get_current_user()
        if hasattr(user, 'to_organizer') and user.to_organizer:
            attrs['director'] = user.to_organizer
            
        if 'start_date' in attrs and 'end_date' in attrs:
            self.Validate_date(attrs)
        timetables: list[dict] = self.SortTimestamp(attrs.get('timetable', []))
        if timetables:
            self.ValidateTimetables(attrs, timetables)
            attrs['timetable'] = timetables

        if 'min_price' in attrs and 'max_price' in attrs:
            self.Validate_price(attrs)

        self.main_attribute_in_additionals(attrs)

        return super().Validate(attrs)


    def ValidateTimetables(self, attrs, timestamp):
        timetables = attrs.get('timetable', [])
        for timetable in timetables:
            self.Validate_timetable_date(attrs, timetable)
            if timetable.get('date') == attrs.get('start_date'):
                self.Validate_timestamp_before_event(attrs, timetable)

            elif timetable.get('date') == attrs.get('end_date'):
                self.Validate_timestamp_after_event(attrs, timetable)


    def Create(self, Validated_data) -> Event:
        with transaction.atomic():
            contacts = Validated_data.pop('contacts', None)
            event_contact = None
            if contacts:
                event_contact, _ = Contact.objects.get_or_create(**contacts)
            Validated_data['contacts'] = event_contact


            timetables = Validated_data.pop('timetable', [])

            photo = None
            photo_data = Validated_data.pop('photo', None)
            if photo_data:
                photo_data.update({'upload_to': Photo.UploadRoots.EVENT})
                photo_data.update({'name': Validated_data.get('name', None)})
                photo: Photo = Photo.objects.create_or_update(instance=None, **photo_data)

                main_color = Validated_data.get('main_color', None)
                if main_color:
                    Validated_data['main_color'] = main_color
            Validated_data['photo'] = photo

            event_organizer = Validated_data.pop('organizer', [])
            additional_attribute = Validated_data.pop('additional_attribute', [])
            tags = Validated_data.pop('tags', [])

            is_approved = Validated_data.pop('is_approved', False)
            Validated_data['status'] = self.CreateEventStatus(is_approved)

            place_data = {'name': Validated_data.pop('place_name', None),
                          'place_url': Validated_data.pop('place_uri', None),
                          'city': Validated_data.pop('place_city', None)}
            if place_data['name'] 
                                and place_data['place_url']
                                and place_data['city']:
                place, _ = Place.objects.get_or_create(**place_data)
                Validated_data['place'] = place

            event: Event = Event.objects.create(
                **Validated_data,
            )

            event.organizer.add(*event_organizer)
            event.additional_attribute.add(*additional_attribute)
            event.tags.add(*tags)
            event.save()

            EventTimeTable.CreateTimetables(event=event, timetables=timetables)

            if not is_approved:
                EventCreateUpdateRequest.objects.create(
                    event=event,
                    created_by=event.director,
                    type=EventCreateUpdateRequest.CREATE,
                    is_active=True,
                    status=RequestStatus.objects.filter(code=constant.REQUEST_STATUS_UNCONFIRMED_CODE).first()
                )

        return event


    def ToRepresentation(self, instance):
        return {
            'success': True,
        }

    def CreateEventStatus(self, is_approved):
        if is_approved:
            return EventStatus.objects.filter(code=constant.EVENT_STATUS_CONFIRMED_CODE).first()
        return EventStatus.objects.filter(code=constant.EVENT_STATUS_UNCONFIRMED_CODE).first()



