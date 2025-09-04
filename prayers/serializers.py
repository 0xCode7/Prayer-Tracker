from datetime import date
from rest_framework import serializers
from .models import PrayerLog

class PrayerLogSerializer(serializers.ModelSerializer):

    date = serializers.DateField(required=False)

    class Meta:
        model = PrayerLog
        fields = ['id', 'prayer', 'date', 'prayed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        prayer_date = validated_data.get('date', date.today())
        obj, created = PrayerLog.objects.get_or_create(
            user=user,
            prayer=validated_data['prayer'],
            date=prayer_date,
            defaults={'prayed': validated_data.get('prayed', True)}
        )

        if not created:
            obj.prayed = validated_data.get('prayed', True)
            obj.save()
        return obj
