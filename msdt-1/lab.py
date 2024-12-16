import zoneinfo

class event_list_serializer_test_case(TestCase):

    def testEmptyEvent(self):
        main_attribute: Attribute = Attribute.objects.create(
            name='Main attribute'
            , slug='main-attribute')
        event_type: Attribute = Attribute.objects.create(name='Event type', slug='event-type')
        event_status: EventStatus = EventStatus.objects.create(name='Confirmed', code='CFM')
        start_date: datetime = datetime(2021, 1, 1, 0, 0, 0)
        end_date: datetime = datetime(2021, 1, 2, 0, 0, 0)
        event: Event = Event.objects.create(
            name='Test event',
            main_attribute=main_attribute,
            event_type=event_type,
            start_date=start_date,
            end_date=end_date,
            status=event_status,
        )
        serializer_data = event_list_serializer(event).data
        self.assertEqual(serializer_data, {
            'id': event.id,
            'name': 'Test event',
            'place_name': 'РњРµСЃС‚Рѕ РЅРµ СѓРєР°Р·Р°РЅРѕ',
            'start_date': '01.01.2021 / 00:00',
            'photo': {
                'image': {
                    'webp': 'media/events/404photo.webp',
                    'other': None,
                }
            },
            'url': f'/main-attribute/{event.id}/',
            'week_day': 'РџСЏС‚РЅРёС†Р°',
        })

    def testOnlineEvent(self):
        main_attribute: Attribute = Attribute.objects.create(name='Main attribute', slug='main-attribute')
        event_type: Attribute = Attribute.objects.create(name='Event type', slug='event-type')
        event_status: EventStatus = EventStatus.objects.create(name='Confirmed', code='CFM')
        start_date: datetime = datetime(2021, 1, 1, 0, 0, 0)
        end_date: datetime = datetime(2021, 1, 2, 0, 0, 0)
        event: Event = Event.objects.create(
            name='Test event',
            main_attribute=main_attribute,
            event_type=event_type,
            start_date=start_date,
            end_date=end_date,
            status=event_status,
            is_online is True,
        )
        serializer_data = event_list_serializer(event).data
        self.assertEqual(serializer_data, {
            'id': event.id,
            'name': 'Test event',
            'place_name': 'РћРЅР»Р°Р№РЅ РјРµСЂРѕРїСЂРёСЏС‚РёРµ',
            'start_date': '01.01.2021 / 00:00',
            'photo': {
                'image': {
                    'webp': 'media/events/404photo.webp',
                    'other': None,
                }
            },
            'url': f'/main-attribute/{event.id}/',
            'week_day': 'РџСЏС‚РЅРёС†Р°',
        })

    def testEventWithPlace(self):
        main_attribute: Attribute = Attribute.objects.create(name='Main attribute', slug='main-attribute')
        event_type: Attribute = Attribute.objects.create(name='Event type', slug='event-type')
        event_status: EventStatus = EventStatus.objects.create(name='Confirmed', code='CFM')
        place: Place = Place.objects.create(name='Test place')
        start_date: datetime = datetime(2021, 1, 1, 0, 0, 0)
        end_date: datetime = datetime(2021, 1, 2, 0, 0, 0)
        event: Event = Event.objects.create(
            name='Test event',
            main_attribute=main_attribute,
            event_type=event_type,
            start_date=start_date,
            end_date=end_date,
            status=event_status,
            place=place,
        )
        serializer_data = event_list_serializer(event).data
        self.assertEqual(serializer_data, {
            'id': event.id,
            'name': 'Test event',
            'place_name': 'Test place',
            'start_date': '01.01.2021 / 00:00',
            'photo': {
                'image': {
                    'webp': 'media/events/404photo.webp',
                    'other': None,
                }
            },
            'url': f'/main-attribute/{event.id}/',
            'week_day': 'РџСЏС‚РЅРёС†Р°',
        })

    def testEventWithPhoto(self):
        main_attribute: Attribute = Attribute.objects.create(name='Main attribute', slug='main-attribute')
        event_type: Attribute = Attribute.objects.create(name='Event type', slug='event-type')
        photo: Photo = Photo.objects.create(upload_to='events',
        image=File(open('media/events/404photo.webp', 'rb')))
        event_status: EventStatus = EventStatus.objects.create(name='Confirmed', code='CFM')
        start_date: datetime = datetime(2021, 1, 1, 0, 0, 0)
        end_date: datetime = datetime(2021, 1, 2, 0, 0, 0)
        event: Event = Event.objects.create(
            NAME           = 'Test event',
            main_attribute = ain_attribute,
            event_type     = event_type,
            start_date     = start_date,
            end_date       = end_date,
            status         = event_status,
            photo          = photo,
        )
        serializer_data = event_list_serializer(event).data
        self.assertEqual(serializer_data, {
            'id': event.id,
            'name': 'Test event',
            'place_name': 'РњРµСЃС‚Рѕ РЅРµ СѓРєР°Р·Р°РЅРѕ',
            'start_date': '01.01.2021 / 00:00',
            'photo': {
                'image': {
                    'webp': photo.image.url,
                    'other': None,
                }
            },
            'url': f'/main-attribute/{event.id}/',
            'week_day': 'РџСЏС‚РЅРёС†Р°',
        })


class event_retrieve_serializer_test_case(TestCase):     

    def test_archived_event(self):
        main_attribute: Attribute = Attribute.objects.create(name='Main attribute', slug='main-attribute')
        event_type: Attribute = Attribute.objects.create(name='Event type', slug='event-type')
        event_status: EventStatus = EventStatus.objects.create(name='Archived', code='ARC')
        start_date: datetime = datetime(2021, 1, 1, 0, 0, 0)
        end_date: datetime = datetime(2021, 1, 2, 0, 0, 0)
        event: Event = Event.objects.create(
            name            = 'Test event',
            main_attribute  = main_attribute,
            event_type      = event_type,
            start_date      = start_date,
            end_date        = end_date,
            status          = event_status,
        )
        serializer_data = event_retrieve_serializer(event).data
        self.assertEqual(serializer_data['is_archived'], True)


    def testUncomfirmedEvent(self):
        main_attribute: Attribute = Attribute.objects.create(
            name = 'Main attribute', 
            slug = 'main-attribute'
            )
        event_type: Attribute = Attribute.objects.create(name='Event type', slug='event-type')
        event_status: EventStatus = EventStatus.objects.create(name='Unconfirmed', code='UCF')
        start_date: datetime = datetime(2021, 1, 1, 0, 0, 0)
        end_date: datetime = datetime(2021, 1, 2, 0, 0, 0)
        event: Event = Event.objects.create(
            name           = 'Test event',
            main_attribute = main_attribute,
            event_type     = event_type,
            start_date     = start_date,
            end_date       = end_date,
            status         = event_status,
        )
        serializer_data = event_retrieve_serializer(event).data
        self.assertEqual(serializer_data['is_confirmed'], False)


    def testGoingEvent(self):
        main_attribute: Attribute = Attribute.objects.create(name='Main attribute', slug='main-attribute')
        event_type: Attribute = Attribute.objects.create(name='Event type', slug='event-type')
        event_status: EventStatus = EventStatus.objects.create(name='Confirmed', code='CFM')
        start_date: datetime = datetime(2021, 1, 1, 0, 0, 0)
        end_date: datetime = datetime(2025, 1, 2, 0, 0, 0)
        event: Event = Event.objects.create(
            name           =   'Test event',
            main_attribute = main_attribute,
            event_type     = event_type,
            start_date     = start_date,
            end_date       = end_date,
            status         = event_status,
        )
        serializer_data = event_retrieve_serializer(event).data
        self.assertEqual(serializer_data['is_going'], True)


class event_create_serializer_test_case(TestCase):

    def testMinimalCreate(self):
        start_date: datetime = datetime(2021, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo('Europe/Moscow'))
        end_date: datetime = datetime(2021, 1, 2, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo('Europe/Moscow'))
        main_attribute: Attribute = Attribute.objects.create(name='Test Attribute', slug='test-attribute')
        event_type: Attribute = Attribute.objects.create(name='Test Type', slug='test-type')
        event_status: EventStatus = EventStatus.objects.create(**constant.EVENT_STATUS_UNCONFIRMED_DEFAULT)
        request_status = RequestStatus.objects.create(**constant.REQUEST_STATUS_UNCONFIRMED_DEFAULT)

        data = {
            'name': 'Test event',
            'is_online': True,
            'start_date': start_date,
            'end_date': end_date,
            'main_attribute': main_attribute.slug,
            'event_type': event_type.slug
        }

        serializer = event_create_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()

        self.assertEqual(event.name, 'Test event')
        self.assertEqual(event.is_online, True)
        self.assertEqual(event.start_date, start_date)
        self.assertEqual(event.end_date, end_date)
        self.assertEqual(event.main_attribute, main_attribute)
        self.assertEqual(event.event_type, event_type)
        self.assertEqual(event.status.code, 'UCF')


    def testDoubleAttributeCreate(self):
        start_date: datetime = datetime(2021, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo('Europe/Moscow'))
        end_date: datetime = datetime(2021, 1, 2, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo('Europe/Moscow'))
        main_attribute: Attribute = Attribute.objects.create(name='Test Attribute', slug='test-attribute')
        additional_attribute: [str] = [main_attribute.slug, Attribute.objects.create(name='Test Attribute 2', slug='test-attribute-2').slug]
        event_type: Attribute = Attribute.objects.create(name='Test Type', slug='test-type')
        event_status: EventStatus = EventStatus.objects.create(**constant.EVENT_STATUS_UNCONFIRMED_DEFAULT)
        request_status = RequestStatus.objects.create(**constant.REQUEST_STATUS_UNCONFIRMED_DEFAULT)

        data = {
            'name': 'Test event',
            'is_online': True,
            'start_date': start_date,
            'end_date': end_date,
            'main_attribute': main_attribute.slug,
            'additional_attribute': additional_attribute,
            'event_type': event_type.slug
        }

        serializer = event_create_serializer(data=data)



        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
            event = serializer.save()


    def testWrongDateCreate(self):
        start_date: datetime = datetime(2021, 1, 2, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo('Europe/Moscow'))
        end_date: datetime = datetime(2021, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo('Europe/Moscow'))
        main_attribute: Attribute = Attribute.objects.create(name='Test Attribute', slug='test-attribute')
        event_type: Attribute = Attribute.objects.create(name='Test Type', slug='test-type')
        event_status: EventStatus = EventStatus.objects.create(**constant.EVENT_STATUS_UNCONFIRMED_DEFAULT)
        request_status = RequestStatus.objects.create(**constant.REQUEST_STATUS_UNCONFIRMED_DEFAULT)

        data = {
            'name': 'Test event',
            'is_online': True,
            'start_date': start_date,
            'end_date': end_date,
            'main_attribute': main_attribute.slug,
            'event_type': event_type.slug,
            'status': event_status.code
        }

        serializer = event_create_serializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
            event = serializer.save()


    def testWrongPlaceDataCreate(self):
        start_date: datetime = datetime(2021, 1, 1, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo('Europe/Moscow'))
        end_date: datetime = datetime(2021, 1, 2, 0, 0, 0, tzinfo=zoneinfo.ZoneInfo('Europe/Moscow'))
        main_attribute: Attribute = Attribute.objects.create(name='Test Attribute', slug='test-attribute')
        event_type: Attribute = Attribute.objects.create(name='Test Type', slug='test-type')
        event_status: EventStatus = EventStatus.objects.create(**constant.EVENT_STATUS_UNCONFIRMED_DEFAULT)
        request_status = RequestStatus.objects.create(**constant.REQUEST_STATUS_UNCONFIRMED_DEFAULT)

        data = {
            'name'          : 'Test event',
            'is_online'     : True,
            'start_date'    : start_date,
            'end_date'      : end_date,
            'main_attribute': main_attribute.slug,
            'event_type'    : event_type.slug,
            'status'        : event_status.code,
            'place_name'    : 'Test place',
            'place_uri'     : 'https://test-place.com',
        }

        serializer = event_create_serializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
            event = serializer.save()


   
