from django.contrib import admin

# Register your models here.




from store.models import Tag,Brand,Colour,memory,Product,OrderSummary

# Register your models here.

admin.site.register(Tag)
admin.site.register(Brand)
admin.site.register(memory)
admin.site.register(Colour)
admin.site.register(Product)
admin.site.register(OrderSummary)


