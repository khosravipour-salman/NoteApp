def get_queryset_fields(field_name, field_value):
	res = {}

	if field_name == 'all':
		res.update(
			{
				field_value: 'title__icontains',
				field_value: 'content__icontains',
				field_value: 'categories__name__icontains',
			}
		)
	
	elif field_name == 'title':
		res.update({field_value: 'title__icontains'})
	
	elif field_name == 'content':
		res.update({field_value: 'content__icontains'})

	elif field_name == 'categories':
		res.update({field_value: 'categories__name__icontains'})

	return res
