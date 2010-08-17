# -*- coding: utf-8 -*-
from django.test import TestCase
from website.adventure.models import Adventure, Graph


class GraphTests(TestCase):
    fixtures = ['auth', 'adventure']

    def test_graph_deletion(self):
        adventure = Adventure.objects.get(pk=1)

        self.assertEqual(Graph.objects.filter(adventure__pk=1).count(), 1)
        adventure.delete()
        self.assertEqual(Graph.objects.filter(adventure__pk=1).count(), 0)
