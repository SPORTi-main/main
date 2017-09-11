from django.core.exceptions import ValidationError

def validate_choice(value):
	choice = value
	if choice == "Fuck":
		raise ValidationError('Do Not Swear!')

