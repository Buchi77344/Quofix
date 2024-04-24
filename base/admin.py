from django.contrib import admin
from. models import User ,UserProfile ,Notification ,Available_Balance, Ledger_Balance ,Transactions,NairaWallet,UserTimestamp ,GPBWallet,EURWallet , Kyc
from  marchant.models import MarchantUser ,Transaction 

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Notification)
admin.site.register(Available_Balance)
admin.site.register(Ledger_Balance)
admin.site.register(MarchantUser)
admin.site.register(Transaction)
admin.site.register(Transactions)
admin.site.register(NairaWallet)
admin.site.register(UserTimestamp)
admin.site.register(EURWallet)
admin.site.register(GPBWallet)
admin.site.register(Kyc)


# Register your models here.

