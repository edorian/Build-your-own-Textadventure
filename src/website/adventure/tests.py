# -*- coding: utf-8 -*-
from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from website.adventure.models import Adventure, Location, Graph


class GraphTests(TestCase):
    fixtures = ['adventure']

    def test_graph_deletion(self):
        adventure = Adventure.objects.get(pk=1)

        self.assertTrue(Graph.objects.filter(adventure__pk=1).exists())
        adventure.delete()
        self.assertFalse(Graph.objects.filter(adventure__pk=1).exists())
