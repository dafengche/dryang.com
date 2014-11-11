from django.test import TestCase

from badminton.models import CostType, Cost, Player, Game


class CostTypeTestCase(TestCase):
    def setUp(self):
        CostType.objects.create(name = 'shuttles')
        CostType.objects.create(name = 'court')

    def test_costtype_has_name(self):
        self.assertEqual(len(CostType.objects.all()), 2)
