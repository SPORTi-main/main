from django.http import JsonResponse

class AjaxFormMixin(object):
	def form_invalid(self,form):
		response =super(AjaxFormMixin,self).form_invalid(form)
		if self.request.is_ajax():
			return JsonResponse(form.errors, status=400)
		else:
			return response

	def form_valid(self,form):
		response =super(AjaxFormMixin,self).form_valid(form)
		if self.request.is_ajax():
			print("sucessfully Ajaxed Form Data:", form.cleaned_data)
			data = {
				'message': "sucessfully Ajaxed Form Data"
			}
			return JsonResponse(data)
		else:
			return response