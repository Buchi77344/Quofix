from django.contrib import admin
from  .models import AdminUser, MarchantPendingTransaction ,MarchantApproveTransaction ,RejectedTransaction

admin.site.register(AdminUser)
admin.site.register(MarchantPendingTransaction)
admin.site.register(MarchantApproveTransaction)
admin.site.register(RejectedTransaction)

