from rest_framework import serializers
from ProgrammingCategory.models import *


class DeveloperSerializers(serializers.ModelSerializer):
  class Meta:
    model = Developer
    fields = "__all__"
