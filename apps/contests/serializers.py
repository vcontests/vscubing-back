from rest_framework import serializers

from .models import ContestModel, DisciplineModel, SolveModel, RoundSessionModel, ScrambleModel
from apps.accounts.models import User


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class DisciplineSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=False)


class ContestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    contest_number = serializers.IntegerField(required=False)
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)
    ongoing = serializers.BooleanField(required=False)


class ScrambleSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    position = serializers.CharField(max_length=10, required=False)
    scramble = serializers.CharField(max_length=512, required=False)
    extra = serializers.BooleanField(required=False)
    contest = serializers.IntegerField(source='contest__contest_number', required=False)
    discipline = serializers.CharField(source='discipline__name', required=False)


class RoundSessionSerializer(DynamicFieldsModelSerializer):
    id = serializers.IntegerField()
    submitted = serializers.BooleanField(required=False)
    contest = serializers.IntegerField(source='contest__contest_number', required=False)
    discipline = serializers.CharField(source='discipline__name', required=False)

    class Meta:
        model = RoundSessionModel
        fields = ['id', 'submitted', 'contest', 'discipline']


class SolveSerializer(DynamicFieldsModelSerializer):

    id = serializers.IntegerField()
    time_ms = serializers.IntegerField(required=False)
    dnf = serializers.BooleanField(required=False)
    extra_id = serializers.IntegerField(required=False)
    state = serializers.CharField(max_length=96, required=False)
    reconstruction = serializers.CharField(max_length=15048, required=False)

    discipline = serializers.CharField(source='discipline.name')
    round_session_id = serializers.IntegerField(source='round_session.id', required=False)
    scramble_scramble = serializers.CharField(source='scramble.scramble')
    scramble = ScrambleSerializer(required=False)

    class Meta:
        model = SolveModel
        fields = ['id', 'time_ms', 'dnf', 'extra_id', 'state', 'reconstruction', 'discipline', 'round_session_id', 'scramble', 'scramble_scramble']

