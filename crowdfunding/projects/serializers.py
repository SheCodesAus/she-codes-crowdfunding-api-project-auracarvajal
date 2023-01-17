from rest_framework import serializers
from .models import Project, Pledge

class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=None)
    goal = serializers.IntegerField()
    image = serializers.URLField()
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.id')
   

    def create(self, validated_data):
        return Project.objects.create(**validated_data)


class PledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pledge
        fields = ['id', 'amount', 'comment', 'anonymous', 'project', 'supporter']
        read_only_fields = ['id', 'supporter']
   

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)

class ProjectDetailsSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)