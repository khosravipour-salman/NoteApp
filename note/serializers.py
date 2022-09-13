from restframework import serializers

from note.models import Note

class NoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Note
		fields = '__all__'